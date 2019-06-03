
from .. values import *


class cTouch:
    def __init__(self, piece, field):
        self.piece = piece
        self.field = field
        self.attacker_beyond = []
        self.supporter_beyond = []


class cSearchForPiece:
    STEPS = []
    MAXCNT = 1
    TARGETS = []

    @classmethod
    def is_field_touched(cls, match, src, color, mode):
        for step in cls.STEPS:
            dst = match.board.search(src, step, cls.MAXCNT)
            if(dst is not None):
                piece = match.board.getfield(dst)
                if(match.color_of_piece(piece) != color):
                    continue
                for target in cls.TARGETS:
                    if(piece == target):
                        if(mode == match.EVAL_MODES['ignore-pins']):
                            return True
                        elif(mode == match.EVAL_MODES['only-pins-to-king']):
                            cpiece = match.obj_for_piece(piece, dst)
                            if(cpiece.is_move_stuck(src)):
                                break
                            else:
                                return True
                        else: #mode == EVAL_MODES['all-pins']
                            cpiece = match.obj_for_piece(piece, dst)
                            if(cpiece.is_move_stuck(src) or match.is_soft_pin(src)[0]):
                                break
                            else:
                                return True
        return False

    @classmethod
    def list_all_field_touches(cls, match, src, color, frdlytouches, enmytouches):
        for step in cls.STEPS:
            dst = match.board.search(src, step, cls.MAXCNT)
            if(dst is not None):
                piece = match.board.getfield(dst)
                for target in cls.TARGETS:
                    if(piece == target):
                        cpiece = match.obj_for_piece(piece, dst)
                        if(cpiece.is_move_stuck(src)):
                            break
                        if(match.color_of_piece(piece) == color):
                            frdlytouches.append(cTouch(piece, dst))
                        else:
                            enmytouches.append(cTouch(piece, dst))

    @classmethod
    def list_field_touches(cls, match, src, color):
        touches = []
        for step in cls.STEPS:
            dst = match.board.search(src, step, cls.MAXCNT)
            if(dst is not None):
                piece = match.board.getfield(dst)
                if(match.color_of_piece(piece) != color):
                    continue
                cpiece = match.obj_for_piece(piece, dst)
                if(cpiece.is_move_stuck(src)):
                    continue
                for target in cls.TARGETS:
                    if(piece == target):
                        touches.append(cTouch(piece, dst))
        return touches

class cSearchForRook(cSearchForPiece):
    STEPS = [8, -8, 1, -1]
    MAXCNT = 7
    TARGETS = [PIECES['wRk'], PIECES['bRk'], PIECES['wQu'], PIECES['bQu']]

class cSearchForBishop(cSearchForPiece):
    STEPS = [9, -9, 7, -7]
    MAXCNT = 7
    TARGETS = [PIECES['wBp'], PIECES['bBp'], PIECES['wQu'], PIECES['bQu']]

class cSearchForKing(cSearchForPiece):
    STEPS = [8, 9, 1, -7, -8, -9, -1, 7]
    MAXCNT = 1
    TARGETS = [PIECES['wKg'], PIECES['bKg']]

    @classmethod
    def is_field_touched(cls, match, src, color):
        for step in cls.STEPS:
            dst = match.board.search(src, step, cls.MAXCNT)
            if(dst is not None):
                piece = match.board.getfield(dst)
                if(match.color_of_piece(piece) != color):
                    continue
                for target in cls.TARGETS:
                    if(piece == target):
                        return True
        return False

class cSearchForKnight(cSearchForPiece):
    STEPS = [17, 10, -6, -15, -17, -10, 6, 15]
    MAXCNT = 1
    TARGETS = [PIECES['wKn'], PIECES['bKn']]

class cSearchForWhitePawn(cSearchForPiece):
    STEPS =  [-7, -9]
    MAXCNT = 1
    TARGETS = [PIECES['wPw']]

class cSearchForBlackPawn(cSearchForPiece):
    STEPS =  [9, 7]
    MAXCNT = 1
    TARGETS = [PIECES['bPw']]


def is_field_touched(match, src, color, mode):
    if(cSearchForRook.is_field_touched(match, src, color, mode)):
        return True
    if(cSearchForBishop.is_field_touched(match, src, color, mode)):
        return True
    if(cSearchForKnight.is_field_touched(match, src, color, mode)):
        return True
    if(cSearchForKing.is_field_touched(match, src, color)):
        return True
    if(cSearchForWhitePawn.is_field_touched(match, src, color, mode)):
        return True
    if(cSearchForBlackPawn.is_field_touched(match, src, color, mode)):
        return True
    return False


def list_all_field_touches(match, src, color):
    frdlytouches = []
    enmytouches = []
    cSearchForRook.list_all_field_touches(match, src, color, frdlytouches, enmytouches)
    cSearchForBishop.list_all_field_touches(match, src, color, frdlytouches, enmytouches)
    cSearchForKnight.list_all_field_touches(match, src, color, frdlytouches, enmytouches)
    cSearchForKing.list_all_field_touches(match, src, color, frdlytouches, enmytouches)
    cSearchForWhitePawn.list_all_field_touches(match, src, color, frdlytouches, enmytouches)
    cSearchForBlackPawn.list_all_field_touches(match, src, color, frdlytouches, enmytouches)
    return frdlytouches, enmytouches


def list_field_touches_beyond(match, ctouch, color):
    cSearchForRook.list_all_field_touches(match, ctouch.field, color, ctouch.supporter_beyond, ctouch.attacker_beyond)
    cSearchForBishop.list_all_field_touches(match, ctouch.field, color, ctouch.supporter_beyond, ctouch.attacker_beyond)
    cSearchForKnight.list_all_field_touches(match, ctouch.field, color, ctouch.supporter_beyond, ctouch.attacker_beyond)
    cSearchForKing.list_all_field_touches(match, ctouch.field, color, ctouch.supporter_beyond, ctouch.attacker_beyond)
    cSearchForWhitePawn.list_all_field_touches(match, ctouch.field, color, ctouch.supporter_beyond, ctouch.attacker_beyond)
    cSearchForBlackPawn.list_all_field_touches(match, ctouch.field, color, ctouch.supporter_beyond, ctouch.attacker_beyond)


def list_field_touches(match, src, color):
    touches = []
    newtouches = cSearchForRook.list_field_touches(match, src, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    newtouches = cSearchForBishop.list_field_touches(match, src, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    newtouches = cSearchForKnight.list_field_touches(match, src, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    newtouches = cSearchForKing.list_field_touches(match, src, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    newtouches = cSearchForWhitePawn.list_field_touches(match, src, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    newtouches = cSearchForBlackPawn.list_field_touches(match, src, color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)
    return touches

