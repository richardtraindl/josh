
from josh.db import get_db

from .engine.values import PIECES
from .engine.match import cMatch
from .engine.move import cMove
from .engine.board import cBoard
from .engine.helper import coord_to_index, index_to_coord, reverse_lookup


def map_match_from_db(match, moves, engine):
    engine.status = int(match['status'])
    engine.level = int(match['level'])
    engine.board.fields = int(match['board'], 16)

    for move in moves:
        cmove = map_move_from_db(move, engine)
        engine.minutes.append(cmove)

    engine.update_attributes()


def map_move_from_db(move, engine):
    cmove = cMove()
    cmove.prevfields = int(move['prevfields'], 16)
    cmove.src = coord_to_index(move['src'])
    cmove.dst = coord_to_index(move['dst'])
    if(move['prompiece']):
        cmove.prompiece = PIECES[move['prompiece']]
    return cmove


def map_move_from_engine(move, matchid):
    sqlmove = {
        "match_id" : None,
        "prevfields" : None,
        "src" : None,
        "dst" : None,
        "prompiece" : None
    }
    sqlmove["match_id"] = matchid
    sqlmove["prevfields"] = map_board_from_int_to_str(move.prevfields)
    sqlmove["src"] = index_to_coord(move.src)
    sqlmove["dst"] = index_to_coord(move.dst)
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
