
from josh.db import get_db

from .engine2.values import PIECES
from .engine2.move import cMove
from .engine2.helper import coord_to_index, index_to_coord, reverse_lookup


def map_sqlmatch_to_engine(sqlmatch, sqlmoves, ematch):
    ematch.id = sqlmatch['id']
    ematch.status = sqlmatch['status']
    ematch.level = sqlmatch['level']

    aryboard = sqlmatch['board'].split(";")
    for y in range(8):
        for x in range(8):
            ematch.board.writefield(x, y, PIECES[aryboard[y * 8 + x]])

    for sqlmove in sqlmoves:
        cmove = map_sql_move_to_engine(sqlmove)
        ematch.move_list.append(cmove)

    ematch.update_attributes()


def map_sql_move_to_engine(sqlmove):
        cmove = cMove()
        cmove.id = sqlmove['id']
        cmove.match = sqlmove['match_id']
        cmove.count = sqlmove['count']
        cmove.srcx, cmove.srcy = coord_to_index(sqlmove['srcfield'])
        cmove.dstx, cmove.dsty = coord_to_index(sqlmove['dstfield'])

        if(sqlmove['enpassfield']):
            cmove.enpassx, cmove.enpassy = coord_to_index(sqlmove['enpassfield'])

        cmove.srcpiece = PIECES[sqlmove['srcpiece']]

        if(sqlmove['captpiece']):
            cmove.captured_piece = PIECES[sqlmove['captpiece']]

        if(sqlmove['prompiece']):
            cmove.prom_piece = PIECES[sqlmove['prompiece']]

        return cmove


def map_engine_move_to_sql(emove):
    sqlmove = {
        "match_id": 0,
        "count": 0,
        "srcfield": "",
        "dstfield": "",
        "enpassfield": "",
        "srcpiece": "",
        "captpiece": "",
        "prompiece": ""
    }
    sqlmove["match_id"] = emove.match.id
    sqlmove["count"] = emove.count
    sqlmove["srcfield"] = index_to_coord(emove.srcx, emove.srcy)
    sqlmove["dstfield"] = index_to_coord(emove.dstx, emove.dsty)
    if(emove.enpassx and emove.enpassy):
        sqlmove["enpassfield"] = index_to_coord(emove.enpassx, emove.enpassy)
    else:
        sqlmove["enpassfield"] = None
    sqlmove["srcpiece"] = reverse_lookup(PIECES, emove.srcpiece)
    sqlmove["captpiece"] = reverse_lookup(PIECES, emove.captpiece)
    if(emove.prompiece):
        sqlmove["prompiece"] = reverse_lookup(PIECES, emove.prompiece)
    else:
        sqlmove["prompiece"] = None
    return sqlmove


def map_cboard_to_strboard(cboard):
    strboard = ""
    for y in range(8):
        for x in range(8):
            piece = cboard.readfield(x, y)
            strboard += reverse_lookup(PIECES, piece) + ";"
    return strboard
