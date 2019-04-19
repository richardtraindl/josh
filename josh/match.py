
import random, threading 
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask, current_app, Response
)
from werkzeug.exceptions import abort

from josh.auth import login_required
from josh.db import get_db
from josh.dbaccess import *
from josh.mapper import *

from .engine2.values import *
from .engine2.helper import coord_to_index, reverse_lookup
from .engine2.match import cMatch
from .engine2.calc import calc_move

bp = Blueprint('match', __name__)


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
            new_match(level, wplayer_name, wplayer_ishuman, bplayer_name, bplayer_ishuman)
            return redirect(url_for('match.index'))

    return render_template('match/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    oldmatch = get_match(id)
    oldwplayer = get_player(id, 1)
    oldbplayer = get_player(id, 0)

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
            status = oldmatch['status']
            board = oldmatch['board']
            wplayer_consumedsecs = oldwplayer['consumedsecs']
            bplayer_consumedsecs = oldbplayer['consumedsecs']
            match = update_match(id, status, level, board, wplayer_name, \
                 wplayer_ishuman, wplayer_consumedsecs, \
                 bplayer_name, bplayer_ishuman, bplayer_consumedsecs)
            return redirect(url_for('match.index'))

    return render_template('match/update.html', match=oldmatch, wplayer=oldwplayer, bplayer=oldbplayer)


@bp.route('/<int:id>/show')
@login_required
def show(id):
    match = get_match(id)
    wplayer = get_player(id, 1)
    bplayer = get_player(id, 0)

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

    return render_template('match/show.html', match=match, board=board, wplayer=wplayer, bplayer=bplayer)


@bp.route('/<int:id>/domove', methods=('POST',))
def domove(id):
    match = get_match(id)
    moves = get_moves(id)
    wplayer = get_player(id, 1)
    bplayer = get_player(id, 0)

    engine = cMatch()
    map_sqlmatch_to_engine(match, engine)
    map_sqlmoves_to_engine(moves, engine)

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
        cmove = engine.do_move(srcx, srcy, dstx, dsty, prompiece)
        status = engine.evaluate_status()
        strboard = map_cboard_to_strboard(engine.board)        
        update_match(id, status, match['level'], strboard, None, None, None, None, None, None)

        move = map_engine_move_to_sql(cmove)
        new_move(move["match_id"], move["count"], move["iscastling"], move["srcfield"], \
                 move["dstfield"], move["enpassfield"], move["captpiece"], move["prompiece"])

        if((engine.next_color() == COLORS['white'] and wplayer['ishuman'] == 0) or
           (engine.next_color() == COLORS['black'] and bplayer['ishuman'] == 0)):
            calc_move_for_immanuel(engine)
    else:
        flash("oje " + reverse_lookup(engine.RETURN_CODES, error))

    return redirect(url_for('match.show', id=match['id'],))


class ImmanuelsThread(threading.Thread):
    def __init__(self, name, engine):
        threading.Thread.__init__(self)
        self.name = name
        self.engine = engine
        self.app = current_app._get_current_object()

    def run(self):
        #app = Flask(__name__)
        with self.app.app_context():
            print("Thread starting " + str(self.name))
            candidates = calc_move(self.engine, None)
            if(len(candidates) > 0):
                gmove = candidates[0]
                cmove = self.engine.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
                status = self.engine.evaluate_status()
                strboard = map_cboard_to_strboard(self.engine.board)        
                update_match(self.engine.id, status, self.engine.level, strboard, None, None, None, None, None, None)

                move = map_engine_move_to_sql(cmove)
                new_move(move["match_id"], move["count"], move["iscastling"], move["srcfield"], \
                         move["dstfield"], move["enpassfield"], move["captpiece"], move["prompiece"])
            else:
                print("no move found or thread outdated!")


def calc_move_for_immanuel(engine):
    status = engine.evaluate_status()
    if(status != engine.STATUS['open']):
        return False, status
    else:
        thread = ImmanuelsThread("immanuel-" + str(random.randint(0, 100000)), engine)
        thread.start()
        return True, engine.RETURN_CODES['ok']


@bp.route('/<int:id>/fetch', methods=('GET',))
def fetch(id):
    matchid = request.args.get('matchid')
    
    match = get_match(id)
    wplayer = get_player(id, 1)
    bplayer = get_player(id, 0)
    movecnt = get_movecnt(matchid)
    
    if(match['clockstart'] is not None):
        clockstart = datetime.fromtimestamp(match['clockstart'])
        timediff = datetime.datetime.now().timestamp() - clockstart
        print(timediff)
    else:
        timediff = 0

    if(movecnt % 2 == 0):
        data = str(movecnt) + "|" + str(wplayer['consumedsecs'] + timediff) + "|" + str(bplayer['consumedsecs'])
    else:
        data = str(movecnt) + "|" + str(wplayer['consumedsecs']) + "|" + str(bplayer['consumedsecs'] + timediff)

    return Response(data)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    delete_match(id)
    return redirect(url_for('match.index'))

