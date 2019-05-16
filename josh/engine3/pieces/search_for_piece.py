
from .. values import *

from .touch import cTouch


class cSearchForPiece:
    STEPS = []
    MAXCNT = 1
    TARGETS = []

    @classmethod
    def is_field_touched(cls, match, srcx, srcy, color, mode):
        for step in cls.STEPS:
            dstx, dsty = match.board.search(srcx, srcy, step[0], step[1], cls.MAXCNT)
            if(dstx is not None):
                piece = match.board.readfield(dstx, dsty)
                if(match.color_of_piece(piece) != color):
                    continue
                for target in cls.TARGETS:
                    if(piece == target):
                        if(mode == match.EVAL_MODES['ignore-pins']):
                            return True
                        elif(mode == match.EVAL_MODES['only-pins-to-king']):
                            cpiece = match.obj_for_piece(piece, dstx, dsty)
                            if(cpiece.is_move_stuck(srcx, srcy)):
                                break
                            else:
                                return True
                        else: #mode == EVAL_MODES['all-pins']
                            cpiece = match.obj_for_piece(piece, dstx, dsty)
                            if(cpiece.is_move_stuck(srcx, srcy) or 
                               match.is_soft_pin(srcx, srcy)[0]):
                                break
                            else:
                                return True
        return False

    @classmethod
    def list_all_field_touches(cls, match, srcx, srcy, color, frdlytouches, enmytouches):
        for step in cls.STEPS:
            dstx, dsty = match.board.search(srcx, srcy, step[0], step[1], cls.MAXCNT)
            if(dstx is not None):
                piece = match.board.readfield(dstx, dsty)
                for target in cls.TARGETS:
                    if(piece == target):
                        cpiece = match.obj_for_piece(piece, dstx, dsty)
                        if(cpiece.is_move_stuck(srcx, srcy)):
                            break
                        if(match.color_of_piece(piece) == color):
                            frdlytouches.append(cTouch(piece, dstx, dsty))
                        else:
                            enmytouches.append(cTouch(piece, dstx, dsty))

    @classmethod
    def list_field_touches(cls, match, srcx, srcy, color):
        touches = []
        for step in cls.STEPS:
            dstx, dsty = match.board.search(srcx, srcy, step[0], step[1], cls.MAXCNT)
            if(dstx is not None):
                piece = match.board.readfield(dstx, dsty)
                if(match.color_of_piece(piece) != color):
                    continue
                cpiece = match.obj_for_piece(piece, dstx, dsty)
                if(cpiece.is_move_stuck(srcx, srcy)):
                    continue
                for target in cls.TARGETS:
                    if(piece == target):
                        touches.append(cTouch(piece, dstx, dsty))
        return touches

class cSearchForRook(cSearchForPiece):
    STEPS = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    MAXCNT = 7
    TARGETS = [PIECES['wRk'], PIECES['bRk'], PIECES['wQu'], PIECES['bQu']]

class cSearchForBishop(cSearchForPiece):
    STEPS = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
    MAXCNT = 7
    TARGETS = [PIECES['wBp'], PIECES['bBp'], PIECES['wQu'], PIECES['bQu']]

class cSearchForKing(cSearchForPiece):
    STEPS = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    MAXCNT = 1
    TARGETS = [PIECES['wKg'], PIECES['bKg']]

    @classmethod
    def is_field_touched(cls, match, srcx, srcy, color):
        for step in cls.STEPS:
            dstx, dsty = match.board.search(srcx, srcy, step[0], step[1], cls.MAXCNT)
            if(dstx is not None):
                piece = match.board.readfield(dstx, dsty)
                if(match.color_of_piece(piece) != color):
                    continue
                for target in cls.TARGETS:
                    if(piece == target):
                        return True
        return False

class cSearchForKnight(cSearchForPiece):
    STEPS = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]
    MAXCNT = 1
    TARGETS = [PIECES['wKn'], PIECES['bKn']]

class cSearchForWhitePawn(cSearchForPiece):
    STEPS =  [[1, -1], [-1, -1]]
    MAXCNT = 1
    TARGETS = [PIECES['wPw']]

class cSearchForBlackPawn(cSearchForPiece):
    STEPS =  [[1, 1], [-1, 1]]
    MAXCNT = 1
    TARGETS = [PIECES['bPw']]


def is_field_touched(match, srcx, srcy, color, mode):
    if(cSearchForRook.is_field_touched(match, srcx, srcy, color, mode)):
        return True
    if(cSearchForBishop.is_field_touched(match, srcx, srcy, color, mode)):
        return True
    if(cSearchForKnight.is_field_touched(match, srcx, srcy, color, mode)):
        return True
    if(cSearchForKing.is_field_touched(match, srcx, srcy, color)):
        return True
    if(cSearchForWhitePawn.is_field_touched(match, srcx, srcy, color, mode)):
        return True
    if(cSearchForBlackPawn.is_field_touched(match, srcx, srcy, color, mode)):
        return True
    return False


def list_all_field_touches(match, srcx, srcy, color):
    frdlytouches = []
    enmytouches = []
    cSearchForRook.list_all_field_touches(match, srcx, srcy, color, frdlytouches, enmytouches)
    cSearchForBishop.list_all_field_touches(match, srcx, srcy, color, frdlytouches, enmytouches)
    cSearchForKnight.list_all_field_touches(match, srcx, srcy, color, frdlytouches, enmytouches)
    cSearchForKing.list_all_field_touches(match, srcx, srcy, color, frdlytouches, enmytouches)
    cSearchForWhitePawn.list_all_field_touches(match, srcx, srcy, color, frdlytouches, enmytouches)
    cSearchForBlackPawn.list_all_field_touches(match, srcx, srcy, color, frdlytouches, enmytouches)
    return frdlytouches, enmytouches


def list_field_touches_beyond(match, ctouch, color):
    cSearchForRook.list_all_field_touches(match, ctouch.fieldx, ctouch.fieldy, color, ctouch.supporter_beyond, ctouch.attacker_beyond)
    cSearchForBishop.list_all_field_touches(match, ctouch.fieldx, ctouch.fieldy, color, ctouch.supporter_beyond, ctouch.attacker_beyond)
    cSearchForKnight.list_all_field_touches(match, ctouch.fieldx, ctouch.fieldy, color, ctouch.supporter_beyond, ctouch.attacker_beyond)
    cSearchForKing.list_all_field_touches(match, ctouch.fieldx, ctouch.fieldy, color, ctouch.supporter_beyond, ctouch.attacker_beyond)
    cSearchForWhitePawn.list_all_field_touches(match, ctouch.fieldx, ctouch.fieldy, color, ctouch.supporter_beyond, ctouch.attacker_beyond)
    cSearchForBlackPawn.list_all_field_touches(match, ctouch.fieldx, ctouch.fieldy, color, ctouch.supporter_beyond, ctouch.attacker_beyond)


def list_field_touches(match, srcx, srcy, color):
    touches = []
    newtouches = cSearchForRook.list_field_touches(match, srcx, srcy, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    newtouches = cSearchForBishop.list_field_touches(match, srcx, srcy, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    newtouches = cSearchForKnight.list_field_touches(match, srcx, srcy, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    newtouches = cSearchForKing.list_field_touches(match, srcx, srcy, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    newtouches = cSearchForWhitePawn.list_field_touches(match, srcx, srcy, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    newtouches = cSearchForBlackPawn.list_field_touches(match, srcx, srcy, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    return touches

