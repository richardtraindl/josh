
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

from .engine.values import *
from .engine.helper import coord_to_index, reverse_lookup
from .engine.match import cMatch
from .engine.debug import import_from_fields
from .engine.compute.calc import calc_move


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
    cache.set(key, value, timeout) # timeout = timeout


def clear_cache(key):
    cache.set(key, int(datetime.now().timestamp()), 1)


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
            wplayer_ishuman = True
        else:
            wplayer_ishuman = False

        bplayer_name = request.form['bplayer_name']
        if(request.form.get('bplayer_ishuman')):
            bplayer_ishuman = True
        else:
            bplayer_ishuman = False

        error = None
        if(not wplayer_name or not bplayer_name):
            error = 'White Player name and Black Player name are required.'
        elif(wplayer_ishuman == False and bplayer_ishuman == False):
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
    wplayer = get_player(id, True)
    bplayer = get_player(id, False)

    if request.method == 'POST':
        level = request.form['level']

        wplayer_name = request.form['wplayer_name']
        if(request.form.get('wplayer_ishuman')):
            wplayer_ishuman = True
        else:
            wplayer_ishuman = False

        bplayer_name = request.form['bplayer_name']
        if(request.form.get('bplayer_ishuman')):
            bplayer_ishuman = True
        else:
            bplayer_ishuman =  False

        error = None
        if not wplayer_name or not bplayer_name:
            error = 'White Player name and Black Player name are required.'
        elif(wplayer_ishuman == False and bplayer_ishuman == False):
            error = 'At least one Player has to be human.'

        if error is not None:
            flash(error)
        else:
            update_match(id, match['status'], level, match['board'], \
                         wplayer_name, wplayer_ishuman, wplayer['consumedsecs'], \
                         bplayer_name, bplayer_ishuman, bplayer['consumedsecs'])
            return redirect(url_for('match.show', id=id,))

    return render_template('match/update.html', match=match, wplayer=wplayer, bplayer=bplayer)


@bp.route('/<int:id>/show')
@login_required
def show(id):
    view = request.args.get('view')
    match = get_match(id)
    wplayer = get_player(id, True)
    bplayer = get_player(id, False)
    moves = get_moves(id)
    movecnt = len(moves)

    engine = cMatch()
    map_match_from_db(match, moves, engine)

    status = engine.evaluate_status()
    if(status == cMatch.STATUS['active']):
        status = match['status']

    class Cell:
        def __init__(self, cell_id, color, value): 
            self.id = cell_id
            self.color = color
            self.value = value

    if(view is None or int(view) == 0):
        view = 0
        start = 7
        end = -1
        step = -1
        instart = 0
        inend = 8
        instep = 1
    else:
        start = 0
        end = 8
        step = 1
        instart = 7
        inend = -1
        instep = -1
    board = []
    for j in range(start, end, step):
        for i in range(instart, inend, instep):
            idx = (j * 8 + i)
            cell_id = chr(i + ord('a')) + chr(j + ord('1'))
            if((j + i) % 2 == 0):
                cell_color = "black"
            else:
                cell_color = "white"
            piece = engine.board.getfield(idx)
            cell = Cell(cell_id, cell_color, reverse_lookup(PIECES, piece))
            board.append(cell)

    wsecs = wplayer['consumedsecs']
    bsecs = bplayer['consumedsecs']
    if(movecnt % 2 == 0):
        wsecs = calc_total_secs(str(engine.created_at) + "-clockstart", wsecs)
    else:
        bsecs = calc_total_secs(str(engine.created_at) + "-clockstart", bsecs)
        
    clockstart = cache.get(str(engine.created_at) + "-clockstart")
    if(clockstart is not None):
        isactive = 1
    else:
        isactive = 0

    minutes = []
    count = 1
    for move in moves:
        cmove = map_move_from_db(move, engine)
        if(count % 2 == 1):
            minutes.append(str(count // 2 + 1) + ". " + cmove.format())
        else:
            minutes.append(cmove.format())
        count += 1

    return render_template('match/show.html', match=match, board=board, view=view, wplayer=wplayer, movecnt=movecnt, minutes=minutes, wsecs=wsecs, bplayer=bplayer, bsecs=bsecs, status=status, score=engine.score , isactive=isactive)


@bp.route('/<int:id>/domove', methods=('POST',))
def domove(id):
    view = request.args.get('view')
    match = get_match(id)
    moves = get_moves(id)
    wplayer = get_player(id, True)
    bplayer = get_player(id, False)

    engine = cMatch()
    map_match_from_db(match, moves, engine)

    if((engine.next_color() == COLORS['white'] and wplayer['ishuman'] == False) or
       (engine.next_color() == COLORS['black'] and bplayer['ishuman'] == False)):
        flash("Wrong Player")
        return redirect(url_for('match.show', id=id,))

    mvsrc = request.form['move_src']
    mvdst = request.form['move_dst']
    mvprompiece = request.form['prom_piece']

    src = coord_to_index(mvsrc) 
    dst = coord_to_index(mvdst)
    if(mvprompiece == "" or mvprompiece == "blk"):
        mvprompiece = None
        prompiece = PIECES['blk']
    else:
        prompiece = PIECES[mvprompiece]

    isvalid, error = engine.is_move_valid(src, dst, prompiece)
    if(isvalid):
        wsecs = wplayer['consumedsecs']
        bsecs = bplayer['consumedsecs']
        if(engine.next_color() == COLORS['white']):
            wsecs = calc_total_secs(str(engine.created_at) + "-clockstart", wsecs)
        else:
            bsecs = calc_total_secs(str(engine.created_at) + "-clockstart", bsecs)

        cmove = engine.do_move(src, dst, prompiece)
        print(hex(engine.board.fields).upper())

        status = engine.evaluate_status()
        if(status == engine.STATUS['active']):
            status = 0

        strboard = map_board_from_int_to_str(engine.board.fields)

        update_match(id, status, match['level'], strboard, wplayer['name'], wplayer['ishuman'], wsecs, bplayer['name'], bplayer['ishuman'], bsecs)

        move = map_move_from_engine(cmove, id)
        new_move(id, move['prevfields'], move['src'], move['dst'], move['prompiece'])

        cache_set(str(engine.created_at) + "-clockstart", int(datetime.now().timestamp()), match['level'])

        if((engine.next_color() == COLORS['white'] and wplayer['ishuman'] == False) or
           (engine.next_color() == COLORS['black'] and bplayer['ishuman'] == False)):
            calc_move_for_immanuel(engine, id)
    else:
        flash("oje " + reverse_lookup(engine.RETURN_CODES, error))

    if(view is None):
        view = 0

    return redirect(url_for('match.show', id=id, view=view,))


class ImmanuelsThread(threading.Thread):
    def __init__(self, name, engine, matchid):
        threading.Thread.__init__(self)
        self.name = name
        self.engine = engine
        self.app = current_app._get_current_object()
        self.matchid = matchid

    def run(self):
        with self.app.app_context():
            print("Thread starting " + str(self.name))
            print("debug info: " + hex(self.engine.board.fields))
            candidates = calc_move(self.engine, None)
            match = get_match(self.matchid)
            movecnt = get_movecnt(self.matchid)
            if(match and match['status'] == 0 and movecnt == self.engine.movecnt() and len(candidates) > 0):
                wplayer = get_player(self.matchid, True)
                bplayer = get_player(self.matchid, False)

                wsecs = wplayer['consumedsecs']
                bsecs = bplayer['consumedsecs']
                if(self.engine.next_color() == COLORS['white']):
                    wsecs = calc_total_secs(str(self.engine.created_at) + "-clockstart", wsecs)
                else:
                    bsecs = calc_total_secs(str(self.engine.created_at) + "-clockstart", bsecs)

                cmove = candidates[0]
                self.engine.do_move(cmove.src, cmove.dst, cmove.prompiece)

                status = self.engine.evaluate_status()
                if(status == self.engine.STATUS['active']):
                    status = 0

                strboard = map_board_from_int_to_str(self.engine.board.fields)

                update_match(self.matchid, status, self.engine.level, strboard, wplayer['name'], wplayer['ishuman'], wsecs, bplayer['name'], bplayer['ishuman'], bsecs)

                move = map_move_from_engine(cmove, self.matchid)
                new_move(self.matchid, move['prevfields'], move['src'], move['dst'], move['prompiece'])

                cache_set(str(self.engine.created_at) + "-clockstart", int(datetime.now().timestamp()), self.engine.level)
            else:
                print("no move found or match is paused!")


def calc_move_for_immanuel(engine, matchid):
    status = engine.evaluate_status()
    if(status != engine.STATUS['active']):
        return False, status
    else:
        thread = ImmanuelsThread("immanuel-" + str(random.randint(0, 100000)), engine, matchid)
        thread.start()
        return True, engine.RETURN_CODES['ok']


@bp.route('/<int:id>/undomove', methods=('GET',))
def undomove(id):
    view = request.args.get('view')
    match = get_match(id)
    moves = get_moves(id)

    if(len(moves) > 0):
        engine = cMatch()
        map_match_from_db(match, moves, engine)

        cmove = engine.undo_move()

        if(cmove is not None):
            move = moves[-1:][0]
            wplayer = get_player(id, True)
            bplayer = get_player(id, False)
            wsecs = wplayer['consumedsecs']
            bsecs = bplayer['consumedsecs']
            if(engine.next_color() == COLORS['white']):
                wsecs = calc_total_secs(str(engine.created_at) + "-clockstart", wsecs)
            else:
                bsecs = calc_total_secs(str(engine.created_at) + "-clockstart", bsecs)
            engine.created_at

            status = engine.evaluate_status()
            if(status == engine.STATUS['active']):
                status = 0

            strboard = map_board_from_int_to_str(engine.board.fields)

            update_match(id, status, match['level'], strboard, wplayer['name'], wplayer['ishuman'], wsecs, bplayer['name'], bplayer['ishuman'], bsecs)

            delete_move(move['id'])

            cache_set(str(engine.created_at) + "-clockstart", int(datetime.now().timestamp()), match['level'])

    if(view is None):
        view = 0

    return redirect(url_for('match.show', id=id, view=view,))


@bp.route('/<int:id>/fetch', methods=('GET',))
def fetch(id):
    """match = get_match(id)
    wplayer = get_player(id, True)
    bplayer = get_player(id, False)"""
    movecnt = get_movecnt(id)

    """wsecs = wplayer['consumedsecs']
    bsecs = bplayer['consumedsecs']
    if(movecnt % 2 == 0):
        wsecs = calc_total_secs(str(match['created']) + "-clockstart", wsecs)
    else:
        bsecs = calc_total_secs(str(match['created']) + "-clockstart", bsecs)"""
             
    data = str(movecnt) + "|" #+ str(wsecs) + "|" + str(bsecs)

    return Response(data)


@bp.route('/<int:id>/pause', methods=('GET',))
def pause(id):
    view = request.args.get('view')
    match = get_match(id)

    if(match['status'] == 0):
        status = 1
        wplayer = get_player(id, True)
        bplayer = get_player(id, False)
        movecnt = get_movecnt(id)

        wsecs = wplayer['consumedsecs']
        bsecs = bplayer['consumedsecs']
        if(movecnt % 2 == 0):
            wsecs = calc_total_secs(str(match['created']) + "-clockstart", wsecs)
        else:
            bsecs = calc_total_secs(str(match['created']) + "-clockstart", bsecs)

        update_match(id, status, match['level'], match['board'], wplayer['name'], wplayer['ishuman'], wsecs, bplayer['name'], bplayer['ishuman'], bsecs)

        clear_cache(str(match['created']) + "-clockstart")

    if(view is None):
        view = 0

    return redirect(url_for('match.show', id=id, view=view,))


@bp.route('/<int:id>/resume', methods=('GET',))
def resume(id):
    view = request.args.get('view')
    match = get_match(id)

    if(match['status'] == 1):
        status = 0

        wplayer = get_player(id, True)
        bplayer = get_player(id, False)

        update_match(id, status, match['level'], match['board'], wplayer['name'], wplayer['ishuman'], wplayer['consumedsecs'], bplayer['name'], bplayer['ishuman'], bplayer['consumedsecs'])

        cache_set(str(match['created']) + "-clockstart", int(datetime.now().timestamp()), match['level'])

        movecnt = get_movecnt(id)
        if((movecnt % 2 == 0 and wplayer['ishuman'] == False) or
           (movecnt % 2 == 1 and bplayer['ishuman'] == False)):
            match = get_match(id)
            moves = get_moves(id)
            engine = cMatch()
            map_match_from_db(match, moves, engine)
            calc_move_for_immanuel(engine, id)

    if(view is None):
        view = 0
    return redirect(url_for('match.show', id=id, view=view,))


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    delete_match(id)
    return redirect(url_for('match.index'))


@bp.route('/debug', methods=('GET',))
@login_required
def debug():
    engine = import_from_fields(0x60111000000000400100000000000004000090000099e90000c0b00030)
    if(engine):
        match = new_match(cMatch.LEVELS['blitz'], "white", True, "Black", False)
        update_match(match['id'], match['status'], engine.level, map_board_from_int_to_str(engine.board.fields), \
                     "white", True, 0, "Black", False, 0)
        return redirect(url_for('match.show', id=match['id'], view=0,))
    else:
        return redirect(url_for('match.index'))

