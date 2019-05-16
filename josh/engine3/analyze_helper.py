
from operator import attrgetter

from .values import *
from .match import *

from .pieces.white_pawn import cWhitePawn
from .pieces.black_pawn import cBlackPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .pieces import pawnfield
from .pieces.touch import cTouch
from .pieces.search_for_piece import list_field_touches


class cDirTouch:
    def __init__(self, piece, direction, fieldx, fieldy):
        self.piece = piece
        self.direction = direction
        self.fieldx = fieldx
        self.fieldy = fieldy


def search_dir(match, fieldx, fieldy, direction, exclx, excly):
    dirtouches = []
    srcx = fieldx
    srcy = fieldy
    stepx, stepy = cQueen.step_for_dir(direction)
    if(stepx is None):
        return dirtouches
    for i in range(7):
        x1, y1 = match.board.search(srcx, srcy, stepx, stepy)
        if(x1 is not None and x1 != exclx and y1 != excly):
            piece = match.board.readfield(x1, y1)
            dirtouches.append(cDirTouch(piece, direction, x1, y1))
            srcx = x1
            srcy = y1
        else:
            break
    return dirtouches


def search_lines_of_pin(match, color, fieldx, fieldy, exclx, excly):
    pinlines = []

    piece = match.board.readfield(fieldx, fieldy)

    oppcolor = REVERSED_COLORS[color]
    
    QUEENDIRS = [DIRS['north'], DIRS['south'], DIRS['east'], DIRS['west'], DIRS['north-east'], DIRS['south-west'], DIRS['north-west'], DIRS['south-east']]
 
    for i in range(len(QUEENDIRS)):
        dirtouches = search_dir(match, fieldx, fieldy, QUEENDIRS[i], exclx, excly)

        if(len(dirtouches) < 2):
            continue

        if(match.color_of_piece(dirtouches[0].piece) == color and 
           match.color_of_piece(dirtouches[1].piece) == oppcolor and
           PIECES_RANK[piece] > PIECES_RANK[dirtouches[0].piece] and 
           PIECES_RANK[piece] > PIECES_RANK[dirtouches[1].piece]):

            if(dirtouches[1].piece == PIECES['wQu'] or dirtouches[1].piece == PIECES['bQu']):
                pinlines.append([dirtouches[0], dirtouches[1]])

            elif(i < 4 and (dirtouches[1].piece == PIECES['wRk'] or dirtouches[1].piece == PIECES['bRk'])): 
                pinlines.append([dirtouches[0], dirtouches[1]])

            elif(i >= 4 and (dirtouches[1].piece == PIECES['wBp'] or dirtouches[1].piece == PIECES['bBp'])):
                pinlines.append([dirtouches[0], dirtouches[1]])

    return pinlines


def is_fork_field(match, x, y, attacker_color):
    piece = match.board.readfield(x, y)
    field_color = match.color_of_piece(piece)
    if(field_color == attacker_color):
        return False
    attackers = list_field_touches(match, x, y, attacker_color)
    for attacker in attackers:
        if(attacker.piece == PIECES['wPw'] or attacker.piece == PIECES['bPw']):
            if(piece == PIECES['blk']):
                attackers.remove(attacker)
    if(piece == PIECES['blk']):
        cpawnfield = cPawnField(match, x, y)
        gmoves = cpawnfield.generate_moves_from_reverse(attacker_color)
        for gmove in gmoves:
            ctouch = cTouch(match.board.readfield(gmove.srcx, gmove.srcy), gmove.srcx, gmove.srcy)
            attackers.append(ctouch)
    for attacker in attackers:
        match.board.writefield(attacker.fieldx, attacker.fieldy, PIECES['blk'])
        match.board.writefield(x, y, attacker.piece)
        ###
        cpiece = match.obj_for_piece(attacker.piece, x, y)
        if(cpiece):
            is_fork_field = cpiece.forks()
        else:
            is_fork_field = False
        match.board.writefield(attacker.fieldx, attacker.fieldy, attacker.piece)
        match.board.writefield(x, y, piece)
        if(is_fork_field):
            return True
    return False


def lowest_piece(touches):
    if(len(touches) == 0):
        return None
    else:
        lowest = PIECES['wKg']
        for touch in touches:
            if(PIECES_RANK[touch.piece] < PIECES_RANK[lowest]):
                lowest = touch.piece
        return lowest


def is_supporter_lower_attacker(gmove, supported):
    piece = gmove.match.board.readfield(gmove.srcx, gmove.srcy)
    for attacker in supported.attacker_beyond:
        if(PIECES_RANK[piece] >= PIECES_RANK[attacker.piece]):
            return False
    return True


def is_discl_supported_weak(discl_supported):
    for ctouch_beyond in discl_supported:
        if(len(ctouch_beyond.attacker_beyond) > len(ctouch_beyond.supporter_beyond)):
            return True
    return False


def is_discl_attacked_supported(discl_attacked):
    for ctouch_beyond in discl_attacked:
        if(len(ctouch_beyond.supporter_beyond) > 0):
            return True
    return False


def is_supported_running_pawn(match, supported):
    if(match.is_endgame() == False):
        return False
    if(supported.piece == PIECES['wPw']):
        cpawn = cWhitePawn(match, supported.fieldx, supported.fieldy)
        if(cpawn.is_running()):
            return True
    elif(supported.piece == PIECES['bPw']):
        cpawn = cBlackPawn(match, supported.fieldx, supported.fieldy)
        if(cpawn.is_running()):
            return True
    return False


def is_attacked_soft_pinned(gmove, piece, attacked):
    match = gmove.match
    if(piece != PIECES['wKg'] and piece != PIECES['bKg']):
        match.board.writefield(gmove.srcx, gmove.srcy, PIECES['blk'])
    is_soft_pinned = match.is_soft_pin(attacked.fieldx, attacked.fieldy)[0]
    match.board.writefield(gmove.srcx, gmove.srcy, piece)
    return is_soft_pinned

