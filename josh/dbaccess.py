

from flask import g

from josh.db import get_db


def get_match(id):
    match = get_db().execute(
        'SELECT m.id, status, level, created, board, user_id, guest_id, username'
        ' FROM match m JOIN user u ON m.user_id = u.id'
        ' WHERE m.id = ?',
        (id,)
    ).fetchone()
    return match


def get_matches():
    db = get_db()
    matches = db.execute(
        'SELECT m.id, status, level, created, user_id, username,'
        ' (SELECT name FROM player p WHERE p.match_id = m.id and p.iswhite = 1) as wplayer_name, '
        ' (SELECT ishuman FROM player p WHERE p.match_id = m.id and p.iswhite = 1) as wplayer_ishuman, '
        ' (SELECT name FROM player p WHERE p.match_id = m.id and p.iswhite = 0) as bplayer_name, '
        ' (SELECT ishuman FROM player p WHERE p.match_id = m.id and p.iswhite = 0) as bplayer_ishuman'
        ' FROM match m JOIN user u ON m.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return matches


def get_player(match_id, iswhite):
    player = get_db().execute(
        'SELECT * FROM player p'
        ' WHERE p.match_id = ? AND p.iswhite = ?',
        (match_id, iswhite,)
    ).fetchone()
    return player


def get_moves(match_id):
    moves = get_db().execute(
        'SELECT * FROM move mv'
        ' WHERE mv.match_id = ? ORDER BY count ASC',
        (match_id,)
    ).fetchall()
    return moves


def get_movecnt(match_id):
    move = get_db().execute(
        'SELECT COUNT(*) FROM move mv'
        ' WHERE mv.match_id = ?',
        (match_id,)
    )
    return move


def get_last_move(match_id):
    move = get_db().execute(
        'SELECT * FROM move mv'
        ' WHERE mv.match_id = ? ORDER BY count DESC LIMIT 1',
        (match_id,)
    ).fetchone()
    return move


def new_match(level, wplayer_name, wplayer_ishuman, bplayer_name, bplayer_ishuman):
    db = get_db()
    cur = g.db.cursor()
    cur.execute('INSERT INTO match (level, user_id) VALUES(?, ?)', (level, g.user['id']))
    g.db.commit()
    match_id = cur.lastrowid
    cur.close()

    db.execute(
        'INSERT INTO player (match_id, name, iswhite, ishuman)'
        ' VALUES (?, ?, ?, ?)',
        (match_id, wplayer_name, 1, wplayer_ishuman)
    )
    db.commit()

    db.execute(
        'INSERT INTO player (match_id, name, iswhite, ishuman)'
        ' VALUES (?, ?, ?, ?)',
        (match_id, bplayer_name, 0, bplayer_ishuman)
    )
    db.commit()

    return get_match(match_id)


def update_match(id, status, level, board, wplayer_name, \
                 wplayer_ishuman, wplayer_consumedsecs, \
                 bplayer_name, bplayer_ishuman, bplayer_consumedsecs):

    db = get_db()
    db.execute(
        'UPDATE match SET status = ?, level = ?, board = ?'
        ' WHERE id = ?',
        (status, level, board, id)
    )
    db.commit()

    db.execute(
        'UPDATE player SET name = ?, ishuman = ?, consumedsecs = ?'
        ' WHERE match_id = ? and iswhite = 1',
        (wplayer_name, wplayer_ishuman, wplayer_consumedsecs, id)
    )
    db.commit()

    db.execute(
        'UPDATE player SET name = ?, ishuman = ?, consumedsecs = ?'
        ' WHERE match_id = ? and iswhite = 0',
        (bplayer_name, bplayer_ishuman, bplayer_consumedsecs, id)
    )
    db.commit()


def new_move(match_id, newcount, iscastling, srcfield, dstfield, enpassfield, captpiece, prompiece):
    db = get_db()
    db.execute(
        'INSERT INTO move (match_id, count, iscastling, srcfield, dstfield, '
        'enpassfield, captpiece, prompiece)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (match_id, newcount, iscastling, srcfield, dstfield, enpassfield, captpiece, prompiece,)
    )
    db.commit()


def delete_match(id):
    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute('DELETE FROM match WHERE id = ?', (id,))
    db.commit()

