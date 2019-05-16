
from josh.db import get_db

from .engine3.values import PIECES
from .engine3.move import cMove
from .engine3.board import cBoard
from .engine3.helper import coord_to_index, index_to_coord, reverse_lookup


def map_match_from_db(match, moves, engine):
    engine.status = match['status']
    engine.level = match['level']
    engine.board.fields = int(match['board'], 16)

    for move in moves:
        cmove = map_move_from_db(move, engine)
        engine.move_list.append(cmove)

    engine.update_attributes()


def map_move_from_db(move, engine):
        cmove = cMove()
        cmove.match = engine
        cmove.prevfields = int(move['prevfields'], 16)
        cmove.count = move['count']
        cmove.srcx, cmove.srcy = coord_to_index(move['srcfield'])
        cmove.dstx, cmove.dsty = coord_to_index(move['dstfield'])

        if(move['enpassfield']):
            cmove.enpassx, cmove.enpassy = coord_to_index(move['enpassfield'])

        cmove.srcpiece = PIECES[move['srcpiece']]

        if(move['captpiece']):
            cmove.captpiece = PIECES[move['captpiece']]

        if(move['prompiece']):
            cmove.prompiece = PIECES[move['prompiece']]

        return cmove


def map_move_from_engine(move, matchid):
    sqlmove = {
        "match_id": None,
        "prevfields": None,
        "count": None,
        "srcfield": None,
        "dstfield": None,
        "enpassfield": None,
        "srcpiece": None,
        "captpiece": None,
        "prompiece": None
    }
    sqlmove["match_id"] = matchid
    sqlmove["prevfields"] = map_board_from_int_to_str(move.prevfields)
    sqlmove["count"] = move.count
    sqlmove["srcfield"] = index_to_coord(move.srcx, move.srcy)
    sqlmove["dstfield"] = index_to_coord(move.dstx, move.dsty)
    if(move.enpassx and move.enpassy):
        sqlmove["enpassfield"] = index_to_coord(move.enpassx, move.enpassy)
    else:
        sqlmove["enpassfield"] = None
    sqlmove["srcpiece"] = reverse_lookup(PIECES, move.srcpiece)
    sqlmove["captpiece"] = reverse_lookup(PIECES, move.captpiece)
    if(move.prompiece):
        sqlmove["prompiece"] = reverse_lookup(PIECES, move.prompiece)
    else:
        sqlmove["prompiece"] = None
    return sqlmove


def map_board_from_int_to_str(intboard):
    strboard = hex(intboard).upper()[2:]
    leading = ""
    if(len(strboard) < 64):
        for i in range((64 - len(strboard))):
            leading += "0"
    return leading + strboard
