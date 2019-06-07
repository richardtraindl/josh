
from operator import attrgetter

from .. values import *
from .. move import cMove, cPrioMove
from .touch import cTouch
from .searchforpiece import is_field_touched, list_field_touches_beyond, list_all_field_touches

class cPiece:
    DIRS_ARY = []
    STEPS = []
    MV_STEPS = []
    MAXCNT = 7

    def __init__(self, match, pos):
        self.match = match
        self.pos = pos
        self.piece = self.match.board.getfield(pos)
        self.color = self.match.color_of_piece(self.piece)

    @classmethod
    def dir_for_move(cls, src, dst):
        return DIRS['undef']

    @classmethod
    def step_for_dir(cls, direction):
        return None

    def is_trapped(self):
        if(is_field_touched(self.match, self.pos, REVERSED_COLORS[self.color], self.match.EVAL_MODES['only-pins-to-king']) == False):
            return False
        for step in self.STEPS:
            pos1 = self.pos + step
            if(self.match.board.is_inbounds(self.pos, pos1, step)):
                dstpiece = self.match.board.getfield(pos1)
                if(self.match.color_of_piece(dstpiece) == self.color):
                    continue
                else:
                    if(dstpiece != PIECES['blk'] and PIECES_RANK[self.piece] <= PIECES_RANK[dstpiece]):
                        return False
                    frdlytouches, enmytouches = list_all_field_touches(self.match, pos1, self.color)
                    enmy_is_lower = False
                    for enmy in enmytouches:
                        if(PIECES_RANK[enmy.piece] < PIECES_RANK[self.piece]):
                            enmy_is_lower = True
                            break
                    if(len(frdlytouches) >= len(enmytouches) and enmy_is_lower == False):
                        return False
        return True

    def is_move_stuck(self, dst):
        mv_dir = self.dir_for_move(self.pos, dst)
        pin_dir = self.match.eval_pin_dir(self.pos)
        if(pin_dir == DIRS['undef'] or mv_dir == pin_dir or REVERSE_DIRS[mv_dir] == pin_dir):
            return False
        else:
            return True

    # version for queen, rook and bishop - other pieces override function
    def is_move_valid(self, dst, prompiece=PIECES['blk']):
        direction = self.dir_for_move(self.pos, dst)
        if(direction == DIRS['undef']):
            return False
        step = self.step_for_dir(direction)
        if(step is not None):
            x = self.pos % 8
            y = self.pos // 8
            pin_dir = self.match.eval_pin_dir(self.pos)
            for piecedir in self.DIRS_ARY:
                if(direction == piecedir):
                    if(pin_dir != piecedir and pin_dir != REVERSE_DIRS[piecedir] and pin_dir != DIRS['undef']):
                        return False
        pos = self.pos + step
        while(self.match.board.is_inbounds(self.pos, pos, None)):
            field = self.match.board.getfield(pos)
            if(pos == dst):
                if(self.match.color_of_piece(field) == self.color):
                    return False
                else:
                    return True
            elif(field != PIECES['blk']):
                return False
            pos += step
        return False

    def do_move(self, dst, prompiece=PIECES['blk'], movecnt=None):
        board = self.match.board
        dstpiece = board.getfield(dst)
        move = cMove(board.fields, self.pos, dst, prompiece)
        board.setfield(move.src, PIECES['blk'])
        board.setfield(move.dst, self.piece)
        self.match.score += SCORES[dstpiece]
        return move

    def undo_move(self, move, movecnt=None):
        board = self.match.board
        board.fields = move.prevfields
        dstpiece_after_undo_mv = board.getfield(move.dst)
        self.match.score -= SCORES[dstpiece_after_undo_mv]
        return move

    def find_attacks_and_supports(self, attacked, supported):
        opp_color = REVERSED_COLORS[self.color]
        for step in self.STEPS:
            dst2 = self.match.board.search(self.pos, step, self.MAXCNT)
            if(dst2 is not None):
                if(self.is_move_stuck(dst2)):
                    continue
                piece = self.match.board.getfield(dst2)
                if(self.match.color_of_piece(piece) == opp_color):
                    ctouch = cTouch(piece, dst2)
                    attacked.append(ctouch)
                    ###
                    self.match.board.setfield(dst2, PIECES['blk'])
                    list_field_touches_beyond(self.match, ctouch, opp_color)
                    self.match.board.setfield(dst2, piece)
                    ###
                elif(self.match.color_of_piece(piece) == self.color):
                    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                        continue
                    ctouch = cTouch(piece, dst2)
                    supported.append(ctouch)
                    ###
                    self.match.board.setfield(dst2, PIECES['blk'])
                    list_field_touches_beyond(self.match, ctouch, self.color)
                    self.match.board.setfield(dst2, piece)
                    ###

    def score_touches(self):
        match = self.match
        score = 0
        frdlytouches, enmytouches = list_all_field_touches(match, self.pos, self.color)
        for friend in frdlytouches:
            if(is_field_touched(match, friend.field, match.oppcolor_of_piece(friend.piece), match.EVAL_MODES['ignore-pins'])):
                score += SUPPORTED_SCORES[self.piece]
            else:
                score += SUPPORTED_SCORES[self.piece] // 2
        for enmy in enmytouches:
            if(match.is_soft_pin(enmy.field)[0]):
                score += ATTACKED_SCORES[enmy.piece] * 4
            else:
                score += ATTACKED_SCORES[enmy.piece]
        return score

    def generate_moves(self, candidate, dbggmove, search_for_mate, mode):
        from ..compute.analyze_move import add_tactics
        moves = []
        for step in self.MV_STEPS:
            count = 0
            excludes = []
            dst = self.pos + step[0]
            while(self.match.board.is_inbounds(self.pos, dst, step[0]) and count < self.MAXCNT):
                count += 1
                flag, errcode = self.match.is_move_valid(self.pos, dst, step[1])
                if(flag):
                    if(mode):
                        move = cMove(self.match.board.fields, self.pos, dst, step[1])
                        priomove = cPrioMove(move)
                        excluded = add_tactics(priomove, self.match, candidate, dbggmove, search_for_mate)
                        if(len(excluded) > 0):
                            excludes.extend(excluded)
                        moves.append(priomove)
                    else:
                        moves.append(cMove(self.match.board.fields, self.pos, dst, step[1]))
                    dst += step[0]
                else:
                    break

        if(mode and len(excludes) > 0):
            includes = []
            sorted(excludes, key=lambda x: x.tactic.weight)
            for excl in excludes:
                if(includes is None):
                    includes.append(excl)
                else:
                    for incl in includes:
                        if(incl.tactic.domain == excl.tactic.domain and 
                           incl.tactic.addition is not None and
                           incl.tactic.addition == excl.tactic.addition):
                            excl.priomove.downgrade(excl.tactic)
                            excl.priomove.evaluate_priority()
                        else:
                            includes.append(excl)

        return moves

# class end
