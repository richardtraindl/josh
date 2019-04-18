
from josh.db import get_db

from .engine2.values import PIECES, COLORS
from .engine2.match import cMatch
from .engine2.move import cMove
from .engine2.helper import coord_to_index, index_to_Uppercoord, reverse_lookup


def import_to_engine(sqlmatch, sqlmoves):
    match = cMatch()
    match.id = sqlmatch['id']
    match.status = sqlmatch['status']
    match.score = 0
    match.level = sqlmatch['level']
    match.seconds_per_move = 0
    match.begin = sqlmatch['created']
    match.time_start = 0
    match.move_list = []

    aryboard = sqlmatch['board'].split(";")
    for y in range(8):
        for x in range(8):
            match.board.writefield(x, y, PIECES[aryboard[y * 8 + x]])

    for sqlmove in sqlmoves:
        move = cMove()
        move.id = sqlmove['id']
        move.match = sqlmove['match_id']
        move.count = sqlmove['count']
        move.iscastling = sqlmove['iscastling'] == 1
        move.srcx, move.srcy = coord_to_index(sqlmove['srcfield'])
        move.dstx, move.dsty = coord_to_index(sqlmove['dstfield'])
        if(sqlmove['enpassfield']):
            print("enpassfield")
            move.enpassx, move.enpassy = coord_to_index(sqlmove['enpassfield'])
        if(sqlmove['captpiece']):
            move.captured_piece = PIECES[sqlmove['captpiece']]
        if(sqlmove['prompiece']):
            print("prompiece")
            move.prom_piece = PIECES[sqlmove['prompiece']]

        match.move_list.append(move)

    match.update_attributes()
    
    return match


def domove_and_export_to_db(ematch, gmove):
    mvsrc = index_to_Uppercoord(gmove.srcx, gmove.srcy)
    mvdst = index_to_Uppercoord(gmove.dstx, gmove.dsty)

    if((ematch.board.readfield(gmove.srcx, gmove.srcy) == PIECES['wKg'] or
        ematch.board.readfield(gmove.srcx, gmove.srcy) == PIECES['bKg']) and
        abs(gmove.srcx - gmove.dstx) > 1):
        iscastling = 1
    else:
        iscastling = 0

    if((ematch.board.readfield(gmove.srcx, gmove.srcy) == PIECES['wPw'] or
        ematch.board.readfield(gmove.srcx, gmove.srcy) == PIECES['bPw']) and
        ematch.board.readfield(gmove.dstx, gmove.dsty) == PIECES['blk']):
        enpassfield = index_to_Uppercoord(gmove.dstx, gmove.srcy)
    else:
        enpassfield = None

    captpiece = reverse_lookup(PIECES, ematch.board.readfield(gmove.dstx, gmove.dsty))
    
    mvprompiece = None
    if(gmove.prompiece and gmove.prompiece == "blk"):
        mvprompiece = None
    else:
        mvprompiece = reverse_lookup(PIECES, gmove.prompiece)

    ematch.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)

    db = get_db()
    db.execute(
        'INSERT INTO move (match_id, count, iscastling, srcfield, dstfield, '
        'enpassfield, captpiece, prompiece)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (ematch.id, ematch.movecnt() + 1, iscastling, mvsrc, mvdst, enpassfield, captpiece, mvprompiece,)
    )
    db.commit()

    strboard = ""
    for y in range(8):
        for x in range(8):
            piece = ematch.board.readfield(x, y)
            strboard += reverse_lookup(PIECES, piece) + ";"
    db.execute(
        'UPDATE match SET board = ?'
        ' WHERE id = ?',
        (strboard, ematch.id,)
    )
    db.commit()
