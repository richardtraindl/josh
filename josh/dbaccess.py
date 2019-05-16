
from flask import g

from josh.db import get_db
from psycopg2.extras import DictCursor


def get_match(id):
    cur = get_db().cursor(cursor_factory=DictCursor)
    cur.execute(
        'SELECT m.id, status, level, created, board, auth_user_id, auth_guest_id, username'
        ' FROM match m JOIN auth_user u ON m.auth_user_id = u.id'
        ' WHERE m.id = %s',
        (id,)
    )
    match = cur.fetchone()
    cur.close()
    return match


def get_matches():
    cur = get_db().cursor(cursor_factory=DictCursor)
    cur.execute(
        'SELECT m.id, status, level, created, auth_user_id, username,'
        ' (SELECT name FROM player p WHERE p.match_id = m.id and p.iswhite = true) as wplayer_name, '
        ' (SELECT ishuman FROM player p WHERE p.match_id = m.id and p.iswhite = true) as wplayer_ishuman, '
        ' (SELECT name FROM player p WHERE p.match_id = m.id and p.iswhite = false) as bplayer_name, '
        ' (SELECT ishuman FROM player p WHERE p.match_id = m.id and p.iswhite = false) as bplayer_ishuman'
        ' FROM match m JOIN auth_user u ON m.auth_user_id = u.id'
        ' ORDER BY created DESC'
    )
    matches = cur.fetchall()
    cur.close()
    return matches


def get_player(match_id, iswhite):
    cur = get_db().cursor(cursor_factory=DictCursor)
    cur.execute(
        'SELECT * FROM player p'
        ' WHERE p.match_id = %s AND p.iswhite = %s',
        (match_id, iswhite,)
    )
    player = cur.fetchone()
    cur.close()
    return player


def get_moves(match_id):
    cur = get_db().cursor(cursor_factory=DictCursor)
    cur.execute(
        'SELECT * FROM move mv'
        ' WHERE mv.match_id = %s ORDER BY count ASC',
        (match_id,)
    )
    moves = cur.fetchall()
    cur.close()
    return moves


def get_movecnt(match_id):
    move = get_last_move(match_id)
    if(move is not None):
        return move['count']
    else:
        return 0


def get_last_move(match_id):
    cur = get_db().cursor(cursor_factory=DictCursor)
    cur.execute(
        'SELECT * FROM move mv'
        ' WHERE mv.match_id = %s ORDER BY count DESC LIMIT 1',
        (match_id,)
    )
    move = cur.fetchone()
    cur.close()
    return move


def new_match(level, wplayer_name, wplayer_ishuman, bplayer_name, bplayer_ishuman):
    dbcon = get_db()
    cur = dbcon.cursor(cursor_factory=DictCursor)
    cur.execute('INSERT INTO match (level, auth_user_id) VALUES(%s, %s)', (level, g.user['id']))
    cur.execute('SELECT LASTVAL()')
    matchid = cur.fetchone()['lastval']

    iswhite = True
    cur.execute(
        'INSERT INTO player (match_id, name, iswhite, ishuman)'
        ' VALUES (%s, %s, %s, %s)',
        (matchid, wplayer_name, iswhite, wplayer_ishuman)
    )

    iswhite = False
    cur.execute(
        'INSERT INTO player (match_id, name, iswhite, ishuman)'
        ' VALUES (%s, %s, %s, %s)',
        (matchid, bplayer_name, iswhite, bplayer_ishuman)
    )
    dbcon.commit()
    cur.close()

    return get_match(matchid)


def update_player(match_id, iswhite, name, ishuman, consumedsecs):
    dbcon = get_db()
    cur = dbcon.cursor()
    cur.execute(
        'UPDATE player SET iswhite = %s, name = %s, ishuman = %s, consumedsecs = %s'
        ' WHERE match_id = %s and iswhite = %s',
        (iswhite, name, ishuman, consumedsecs, match_id, iswhite)
    )
    dbcon.commit()
    cur.close()


def update_match(id, status, level, board, \
                 wplayer_name, wplayer_ishuman, wplayer_consumedsecs, \
                 bplayer_name, bplayer_ishuman, bplayer_consumedsecs):

    dbcon = get_db()
    cur = dbcon.cursor()
    cur.execute(
        'UPDATE match SET status = %s, level = %s, board = %s'
        ' WHERE id = %s',
        (status, level, board, id)
    )

    if(wplayer_name is not None and wplayer_ishuman is not None):
        cur.execute(
            'UPDATE player SET name = %s, ishuman = %s, consumedsecs = %s'
            ' WHERE match_id = %s and iswhite = true',
            (wplayer_name, wplayer_ishuman, wplayer_consumedsecs, id)
        )

    if(bplayer_name is not None and bplayer_ishuman is not None):
        cur.execute(
            'UPDATE player SET name = %s, ishuman = %s, consumedsecs = %s'
            ' WHERE match_id = %s and iswhite = false',
            (bplayer_name, bplayer_ishuman, bplayer_consumedsecs, id)
        )
    dbcon.commit()
    cur.close()


def new_move(match_id, prevfields, newcount, srcfield, dstfield, enpassfield, srcpiece, captpiece, prompiece):
    dbcon = get_db()
    cur = dbcon.cursor()
    cur.execute(
        'INSERT INTO move (match_id, prevfields, count, srcfield, dstfield, '
        'enpassfield, srcpiece, captpiece, prompiece)'
        ' VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)',
        (match_id, prevfields, newcount, srcfield, dstfield, enpassfield, srcpiece, captpiece, prompiece,)
    )
    dbcon.commit()
    cur.close()


def delete_match(id):
    dbcon = get_db()
    cur = dbcon.cursor()
    cur.execute('DELETE FROM match WHERE id = %s', (id,))
    dbcon.commit()
    cur.close()


def delete_move(id):
    dbcon = get_db()
    cur = dbcon.cursor()
    cur.execute('DELETE FROM move WHERE id = %s', (id,))
    dbcon.commit()
    cur.close()

