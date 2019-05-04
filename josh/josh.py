
import random, threading 
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask, current_app, Response
)
from werkzeug.exceptions import abort
from werkzeug.contrib.cache import SimpleCache

from josh.auth import login_required
from josh.db import get_db
from josh.dbaccess import *
from josh.mapper import *

from .engine2.values import *
from .engine2.helper import coord_to_index, reverse_lookup
from .engine2.match import cMatch
from .engine2.calc import calc_move

bp = Blueprint('match', __name__)
cache = SimpleCache()


def cache_set(key, value, level):
    if(level == 0):
        timeout = 10 * 60 * 60
    elif(level == 1):
        timeout = 20 * 60 * 60
    elif(level == 2):
        timeout = 30 * 60 * 60
    else:
        timeout = 60 * 60 * 60
    cache.set(key, value, timeout = timeout)


def calc_total_secs(key, secs):
    clockstart = cache.get(key)
    if(clockstart is not None):
        timediff = int(datetime.now().timestamp()) - clockstart
    else:
        timediff = 0
    return secs + timediff


@bp.route('/')
def index():
    db = get_db()
    matches = get_matches()
    return render_template('match/index.html', matches=matches)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        level = request.form['level']

        wplayer_name = request.form['wplayer_name']

        if(request.form.get('wplayer_ishuman')):
            wplayer_ishuman = 1
        else:
            wplayer_ishuman = 0

        bplayer_name = request.form['bplayer_name']

        if(request.form.get('bplayer_ishuman')):
            bplayer_ishuman = 1
        else:
            bplayer_ishuman = 0

        error = None
        if(not wplayer_name or not bplayer_name):
            error = 'White Player name and Black Player name are required.'
        elif(wplayer_ishuman == 0 and bplayer_ishuman == 0):
            error = 'At least one Player has to be human.'

        if(error is not None):
            flash(error)
        else:
            match = new_match(level, wplayer_name, wplayer_ishuman, bplayer_name, bplayer_ishuman)
            return redirect(url_for('match.show', id=match['id'],))

    return render_template('match/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    match = get_match(id)
    wplayer = get_player(id, 1)
    bplayer = get_player(id, 0)

    if request.method == 'POST':
        level = request.form['level']

        wplayer_name = request.form['wplayer_name']

        if(request.form.get('wplayer_ishuman')):
            wplayer_ishuman = 1
        else:
            wplayer_ishuman = 0

        bplayer_name = request.form['bplayer_name']

        if(request.form.get('bplayer_ishuman')):
            bplayer_ishuman = 1
        else:
            bplayer_ishuman = 0

        error = None
        if not wplayer_name or not bplayer_name:
            error = 'White Player name and Black Player name are required.'
        elif(wplayer_ishuman == 0 and bplayer_ishuman == 0):
            error = 'At least one Player has to be human.'

        if error is not None:
            flash(error)
        else:
            status = match['status']
            board = match['board']
            wsecs = wplayer['consumedsecs']
            bsecs = bplayer['consumedsecs']
            update_match(id, status, level, board, wplayer_name, \
                         wplayer_ishuman, wsecs, bplayer_name, bplayer_ishuman, bsecs)
            return redirect(url_for('match.show', id=id,))

    return render_template('match/update.html', match=match, wplayer=wplayer, bplayer=bplayer)


@bp.route('/<int:id>/show')
@login_required
def show(id):
    match = get_match(id)
    wplayer = get_player(id, 1)
    bplayer = get_player(id, 0)
    moves = get_moves(id)
    movecnt = len(moves)

    engine = cMatch()
    map_sqlmatch_to_engine(match, moves, engine)

    status = engine.evaluate_status()
    if(status == cMatch.STATUS['active']):
        status = match['status']

    mboard = match['board']
    class Cell:
        def __init__(self, cell_id, color, value): 
            self.id = cell_id
            self.color = color
            self.value = value

    board = []
    for j in range(7, -1, -1):
        for i in range(8):
            idx = j * 8 * 4 + i * 4
            cell_id = chr(i + ord('a')) + chr(j + ord('1'))
            if((j + i) % 2 == 0):
                cell_color = "black"
            else:
                cell_color = "white"
            cell = Cell(cell_id, cell_color, mboard[idx:idx+3])
            board.append(cell)

    wsecs = wplayer['consumedsecs']
    bsecs = bplayer['consumedsecs']
    if(movecnt % 2 == 0):
        wsecs = calc_total_secs(str(id) + "-clockstart", wsecs)
    else:
        bsecs = calc_total_secs(str(id) + "-clockstart", bsecs)
        
    clockstart = cache.get(str(id) + "-clockstart")
    if(clockstart is not None):
        isactive = 1
    else:
        isactive = 0

    minutes = []
    if(movecnt % 2 == 0):
        cnt = min(movecnt, 8)
    else:
        cnt = min(movecnt, 9)
    for move in moves[(movecnt - cnt):]:
        cmove = map_sql_move_to_engine(move)
        if(cmove.count % 2 == 1):
            minutes.append(str(cmove.count // 2 + 1) + ". " + cmove.format_move())
        else:
            minutes.append(cmove.format_move())

    return render_template('match/show.html', match=match, board=board, wplayer=wplayer, movecnt=movecnt, minutes=minutes, wsecs=wsecs, bplayer=bplayer, bsecs=bsecs, status=status, score=engine.score , isactive=isactive)


@bp.route('/<int:id>/domove', methods=('POST',))
def domove(id):
    match = get_match(id)
    moves = get_moves(id)
    wplayer = get_player(id, 1)
    bplayer = get_player(id, 0)

    engine = cMatch()
    map_sqlmatch_to_engine(match, moves, engine)

    if((engine.next_color() == COLORS['white'] and wplayer['ishuman'] == 0) or
       (engine.next_color() == COLORS['black'] and bplayer['ishuman'] == 0)):
        flash("Wrong Player")
        return redirect(url_for('match.show', id=id,))

    mvsrc = request.form['move_src']
    mvdst = request.form['move_dst']
    mvprompiece = request.form['prom_piece']

    srcx, srcy = coord_to_index(mvsrc) 
    dstx, dsty = coord_to_index(mvdst)
    if(mvprompiece == "" or mvprompiece == "blk"):
        mvprompiece = None
        prompiece = PIECES['blk']
    else:
        prompiece = PIECES[mvprompiece]

    isvalid, error = engine.is_move_valid(srcx, srcy, dstx, dsty, prompiece)
    if(isvalid):
        wsecs = wplayer['consumedsecs']
        bsecs = bplayer['consumedsecs']
        if(engine.next_color() == COLORS['white']):
            wsecs = calc_total_secs(str(id) + "-clockstart", wsecs)
        else:
            bsecs = calc_total_secs(str(id) + "-clockstart", bsecs)

        cmove = engine.do_move(srcx, srcy, dstx, dsty, prompiece)

        status = engine.evaluate_status()
        if(status == engine.STATUS['active']):
            status = 0

        strboard = map_cboard_to_strboard(engine.board)

        update_match(id, status, match['level'], strboard, wplayer['name'], wplayer['ishuman'], wsecs, bplayer['name'], bplayer['ishuman'], bsecs)

        move = map_engine_move_to_sql(cmove)
        new_move(move["match_id"], move["count"], move["srcfield"], move["dstfield"], \
                 move["enpassfield"], move["srcpiece"], move["captpiece"], move["prompiece"])

        cache_set(str(id) + "-clockstart", int(datetime.now().timestamp()), match['level'])

        if((engine.next_color() == COLORS['white'] and wplayer['ishuman'] == 0) or
           (engine.next_color() == COLORS['black'] and bplayer['ishuman'] == 0)):
            calc_move_for_immanuel(engine)
    else:
        flash("oje " + reverse_lookup(engine.RETURN_CODES, error))

    return redirect(url_for('match.show', id=id,))


class ImmanuelsThread(threading.Thread):
    def __init__(self, name, engine):
        threading.Thread.__init__(self)
        self.name = name
        self.engine = engine
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            print("Thread starting " + str(self.name))
            candidates = calc_move(self.engine, None)
            match = get_match(self.engine.id)
            movecnt = get_movecnt(self.engine.id)
            if(match['status'] == 0 and movecnt == self.engine.movecnt() and len(candidates) > 0):
                wplayer = get_player(self.engine.id, 1)
                bplayer = get_player(self.engine.id, 0)

                wsecs = wplayer['consumedsecs']
                bsecs = bplayer['consumedsecs']
                if(self.engine.next_color() == COLORS['white']):
                    wsecs = calc_total_secs(str(self.engine.id) + "-clockstart", wsecs)
                else:
                    bsecs = calc_total_secs(str(self.engine.id) + "-clockstart", bsecs)

                gmove = candidates[0]
                cmove = self.engine.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)

                status = self.engine.evaluate_status()
                if(status == self.engine.STATUS['active']):
                    status = 0

                strboard = map_cboard_to_strboard(self.engine.board)        

                update_match(self.engine.id, status, self.engine.level, strboard, wplayer['name'], wplayer['ishuman'], wsecs, bplayer['name'], bplayer['ishuman'], bsecs)

                move = map_engine_move_to_sql(cmove)
                new_move(move["match_id"], move["count"], move["srcfield"], move["dstfield"], \
                         move["enpassfield"], move["srcpiece"], move["captpiece"], move["prompiece"])

                cache_set(str(self.engine.id) + "-clockstart", int(datetime.now().timestamp()), self.engine.level)
            else:
                print("no move found or match is paused!")


def calc_move_for_immanuel(engine):
    status = engine.evaluate_status()
    if(status != engine.STATUS['active']):
        return False, status
    else:
        thread = ImmanuelsThread("immanuel-" + str(random.randint(0, 100000)), engine)
        thread.start()
        return True, engine.RETURN_CODES['ok']


@bp.route('/<int:id>/undomove', methods=('GET',))
def undomove(id):
    match = get_match(id)
    moves = get_moves(id)

    if(len(moves) > 0):
        engine = cMatch()
        map_sqlmatch_to_engine(match, moves, engine)

        move = engine.undo_move()

        if(move is not None):
            wplayer = get_player(id, 1)
            bplayer = get_player(id, 0)
            wsecs = wplayer['consumedsecs']
            bsecs = bplayer['consumedsecs']
            if(engine.next_color() == COLORS['white']):
                wsecs = calc_total_secs(str(id) + "-clockstart", wsecs)
            else:
                bsecs = calc_total_secs(str(id) + "-clockstart", bsecs)

            status = engine.evaluate_status()
            if(status == engine.STATUS['active']):
                status = 0

            strboard = map_cboard_to_strboard(engine.board)

            update_match(id, status, match['level'], strboard, wplayer['name'], wplayer['ishuman'], wsecs, bplayer['name'], bplayer['ishuman'], bsecs)

            delete_move(move.id)

            cache_set(str(id) + "-clockstart", int(datetime.now().timestamp()), match['level'])

    return redirect(url_for('match.show', id=id,))


@bp.route('/<int:id>/fetch', methods=('GET',))
def fetch(id):
    match = get_match(id)
    wplayer = get_player(id, 1)
    bplayer = get_player(id, 0)
    movecnt = get_movecnt(id)

    wsecs = wplayer['consumedsecs']
    bsecs = bplayer['consumedsecs']
    if(movecnt % 2 == 0):
        wsecs = calc_total_secs(str(id) + "-clockstart", wsecs)
    else:
        bsecs = calc_total_secs(str(id) + "-clockstart", bsecs)
             
    data = str(movecnt) + "|" + str(wsecs) + "|" + str(bsecs)

    return Response(data)


@bp.route('/<int:id>/pause', methods=('GET',))
def pause(id):
    match = get_match(id)

    if(match['status'] == 0):
        status = 1
        wplayer = get_player(id, 1)
        bplayer = get_player(id, 0)
        movecnt = get_movecnt(id)

        wsecs = wplayer['consumedsecs']
        bsecs = bplayer['consumedsecs']
        if(movecnt % 2 == 0):
            wsecs = calc_total_secs(str(id) + "-clockstart", wsecs)
        else:
            bsecs = calc_total_secs(str(id) + "-clockstart", bsecs)

        update_match(id, status, match['level'], match['board'], wplayer['name'], wplayer['ishuman'], wsecs, bplayer['name'], bplayer['ishuman'], bsecs)

        cache.set(str(id) + "-clockstart", int(datetime.now().timestamp()), 1)

    return redirect(url_for('match.show', id=id,))


@bp.route('/<int:id>/resume', methods=('GET',))
def resume(id):
    match = get_match(id)

    if(match['status'] == 1):
        status = 0

        wplayer = get_player(id, 1)
        bplayer = get_player(id, 0)

        update_match(id, status, match['level'], match['board'], wplayer['name'], wplayer['ishuman'], wplayer['consumedsecs'], bplayer['name'], bplayer['ishuman'], bplayer['consumedsecs'])

        cache_set(str(id) + "-clockstart", int(datetime.now().timestamp()), match['level'])

        movecnt = get_movecnt(id)
        if((movecnt % 2 == 0 and wplayer['ishuman'] == 0) or
           (movecnt % 2 == 1 and bplayer['ishuman'] == 0)):
            match = get_match(id)
            moves = get_moves(id)
            engine = cMatch()
            map_sqlmatch_to_engine(match, moves, engine)
            calc_move_for_immanuel(engine)

    return redirect(url_for('match.show', id=id,))


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    delete_match(id)
    return redirect(url_for('match.index'))

