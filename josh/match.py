
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from josh.auth import login_required
from josh.db import get_db


bp = Blueprint('match', __name__)


@bp.route('/')
def index():
    db = get_db()
    matches = db.execute(
        'SELECT m.id, status, level, created, white_player_name, white_player_is_human, '
        'black_player_name, black_player_is_human, user_id, username'
        ' FROM match m JOIN user u ON m.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('match/index.html', matches=matches)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        level = request.form['level']
        white_player_name = request.form['white_player_name']
        if(request.form.get('white_player_is_human')):
            white_player_is_human = 1
        else:
            white_player_is_human = 0
        black_player_name = request.form['black_player_name']
        if(request.form.get('black_player_is_human')):
            black_player_is_human = 1
        else:
            black_player_is_human = 0
        error = None

        if not white_player_name or not black_player_name:
            error = 'white_player_name and black_player_name are required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO match (level, white_player_name, white_player_is_human, black_player_name, black_player_is_human, user_id)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (level, white_player_name, white_player_is_human, black_player_name, black_player_is_human, g.user['id'])
            )
            db.commit()
            return redirect(url_for('match.index'))

    return render_template('match/create.html')


def get_match(id, check_user=True):
    match = get_db().execute(
        'SELECT m.id, status, level, created, white_player_name, white_player_is_human, '
        'black_player_name, black_player_is_human, board, user_id, username'
        ' FROM match m JOIN user u ON m.user_id = u.id'
        ' WHERE m.id = ?',
        (id,)
    ).fetchone()

    if match is None:
        abort(404, "Match id {0} doesn't exist.".format(id))

    if check_user and match['user_id'] != g.user['id']:
        abort(403)

    return match


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    match = get_match(id)

    if request.method == 'POST':
        level = request.form['level']
        white_player_name = request.form['white_player_name']
        if(request.form.get('white_player_is_human')):
            white_player_is_human = 1
        else:
            white_player_is_human = 0
        black_player_name = request.form['black_player_name']
        if(request.form.get('black_player_is_human')):
            black_player_is_human = 1
        else:
            black_player_is_human = 0
        error = None

        if not white_player_name or not black_player_name:
            error = 'white_player_name and black_player_name are required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE match SET level = ?, white_player_name = ?, white_player_is_human = ?, black_player_name = ?, black_player_is_human = ?'
                ' WHERE id = ?',
                (level, white_player_name, white_player_is_human, black_player_name, black_player_is_human, id)
            )
            db.commit()
            return redirect(url_for('match.index'))

    return render_template('match/update.html', match=match)


@bp.route('/<int:id>/show')
@login_required
def show(id):
    match = get_match(id)

    board = match['board']
    class Cell:
        def __init__(self, cell_id, color, value): 
            self.id = cell_id
            self.color = color
            self.value = value

    newboard = []
    for j in range(7, -1, -1):
        for i in range(8):
            idx = j * 8 * 4 + i * 4
            cell_id = chr(i + ord('A')) + chr(j + ord('1'))
            if((j + i) % 2 == 0):
                cell_color = "black"
            else:
                cell_color = "white"
            cell = Cell(cell_id, cell_color, board[idx:idx+3])
            newboard.append(cell)

    return render_template('match/show.html', match=match, board=newboard)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_match(id)
    db = get_db()
    db.execute('DELETE FROM match WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('match.index'))

