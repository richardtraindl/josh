
from .. values import *
from .. move import *

from .touch import cTouch
from .search_for_piece import is_field_touched, list_all_field_touches, list_field_touches_beyond


class cPiece:
    DIRS_ARY = []
    STEPS = []
    GEN_STEPS = []
    MAXCNT = 7

    def __init__(self, match, xpos, ypos):
        self.match = match
        self.xpos = xpos
        self.ypos = ypos
        self.piece = match.board.readfield(xpos, ypos)
        self.color = match.color_of_piece(self.piece)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        return DIRS['undefined']

    @classmethod
    def step_for_dir(cls, direction):
        return None, None

    def is_trapped(self):
        if(is_field_touched(self.match, self.xpos, self.ypos, REVERSED_COLORS[self.color], self.match.EVAL_MODES['only-pins-to-king']) == False):
            return False
        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                dstpiece = self.match.board.readfield(x1, y1)
                if(self.match.color_of_piece(dstpiece) == self.color):
                    continue
                else:
                    if(dstpiece != PIECES['blk'] and PIECES_RANK[self.piece] <= PIECES_RANK[dstpiece]):
                        return False
                    frdlytouches, enmytouches = list_all_field_touches(self.match, x1, y1, self.color)
                    enmy_is_lower = False
                    for enmy in enmytouches:
                        if(PIECES_RANK[enmy.piece] < PIECES_RANK[self.piece]):
                            enmy_is_lower = True
                            break
                    if(len(frdlytouches) >= len(enmytouches) and enmy_is_lower == False):
                        return False
        return True

    def is_piece_stuck(self):
        pin_dir = self.match.eval_pin_dir(self.xpos, self.ypos)
        if(pin_dir == DIRS['undefined']):
            return False
        for piecedir in self.DIRS_ARY:
            if(pin_dir == piecedir):
                return False
        return True

    def is_move_stuck(self, dstx, dsty):
        mv_dir = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        pin_dir = self.match.eval_pin_dir(self.xpos, self.ypos)
        if(pin_dir == DIRS['undefined'] or mv_dir == pin_dir or REVERSE_DIRS[mv_dir] == pin_dir):
            return False
        else:
            return True

    # version for queen, rook and bishop - other pieces override function
    def is_move_valid(self, dstx, dsty, prompiece=PIECES['blk']):
        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == DIRS['undefined']):
            return False
        stepx, stepy = self.step_for_dir(direction)
        if(stepx is not None):
            pin_dir = self.match.eval_pin_dir(self.xpos, self.ypos)
            for piecedir in self.DIRS_ARY:
                if(direction == piecedir):
                    if(pin_dir != piecedir and pin_dir != REVERSE_DIRS[piecedir] and pin_dir != DIRS['undefined']):
                        return False
        x = self.xpos + stepx
        y = self.ypos + stepy
        while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
            field = self.match.board.readfield(x, y)
            if(x == dstx and y == dsty):
                if(self.match.color_of_piece(field) == self.color):
                    return False
                else:
                    return True
            elif(field != PIECES['blk']):
                return False
            x += stepx
            y += stepy
        return False

################
    def do_move(self, dstx, dsty, prompiece=PIECES['blk']):
        board = self.match.board
        dstpiece = board.readfield(dstx, dsty)
        move = cMove(self.match, self.match.movecnt() + 1, \
                     self.xpos, self.ypos, dstx, dsty, \
                     None, None, self.piece, dstpiece, prompiece)

        board.writefield(move.srcx, move.srcy, PIECES['blk'])
        board.writefield(move.dstx, move.dsty, self.piece)
        board.decr_officer_counter(dstpiece)
        self.match.score += SCORES[dstpiece]
        return move
################

################
    def undo_move(self, move):
        board = self.match.board
        board.writefield(move.srcx, move.srcy, self.piece)
        board.writefield(move.dstx, move.dsty, move.captpiece)
        self.match.score -= SCORES[move.captpiece]
        board.incr_officer_counter(move)
        return move
################

    def find_attacks_and_supports(self, attacked, supported):
        opp_color = REVERSED_COLORS[self.color]
        for step in self.STEPS:
            x1, y1 = self.match.board.search(self.xpos, self.ypos, step[0], step[1], self.MAXCNT)
            if(x1 is not None):
                if(self.is_move_stuck(x1, y1)):
                    continue
                piece = self.match.board.readfield(x1, y1)
                if(self.match.color_of_piece(piece) == opp_color):
                    ctouch = cTouch(piece, x1, y1)
                    attacked.append(ctouch)
                    ###
                    self.match.board.writefield(self.xpos, self.ypos, PIECES['blk'])
                    list_field_touches_beyond(self.match, ctouch, opp_color)
                    self.match.board.writefield(self.xpos, self.ypos, self.piece)
                    ###
                elif(self.match.color_of_piece(piece) == self.color):
                    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                        continue
                    ctouch = cTouch(piece, x1, y1)
                    supported.append(ctouch)
                    ###
                    self.match.board.writefield(self.xpos, self.ypos, PIECES['blk'])
                    list_field_touches_beyond(self.match, ctouch, self.color)
                    self.match.board.writefield(self.xpos, self.ypos, self.piece)
                    ###

    def move_controles_file(self, dstx, dsty):
        cnt = 0
        move_dir = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        move_opp_dir = REVERSE_DIRS[move_dir]
    
        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            direction = self.dir_for_move(dstx, dsty, dstx + stepx, dsty + stepy)
            if(direction == move_dir or direction == move_opp_dir):
                continue
            x1 = dstx + stepx
            y1 = dsty + stepy
            while(self.match.is_inbounds(x1, y1)):
                piece = self.match.board.readfield(x1, y1)
                if(self.match.color_of_piece(piece) == self.color):
                    break
                else:
                    cnt += 1
                    x1 += stepx
                    y1 += stepy

        if(cnt >= 5):
            return True
        else:
            return False

    def score_touches(self):
        supporter_score = 0
        attacker_score = 0
        frdlytouches, enmytouches = list_all_field_touches(self.match, self.xpos, self.ypos, self.color)
        if(len(frdlytouches) > 0):
            if(len(enmytouches) == 0):
                supporter_score += SUPPORTED_SCORES[self.piece] // 2
            else:
                supporter_score += SUPPORTED_SCORES[self.piece]
        if(len(enmytouches) > 0):
            attacker_score += ATTACKED_SCORES[self.piece]
        if(self.match.is_soft_pin(self.xpos, self.ypos)[0]):
            rank = PIECES_RANK[PIECES['wQu']]
            for enmy in enmytouches:
                if(PIECES_RANK[enmy.piece] < rank):
                    rank = PIECES_RANK[enmy.piece]
            attacker_score += attacker_score * (1 + PIECES_RANK[PIECES['wQu']] - rank) // 2
        return supporter_score + attacker_score

    def list_moves(self):
        movelist = []
        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.board.readfield(x1, y1)
                if(self.match.color_of_piece(piece) != self.color):
                    movelist.append([x1, y1])
        return movelist

    def generate_moves(self, mode=True):
        moves = []
        for direction in self.GEN_STEPS:
            for step in direction:
                dstx = self.xpos + step[0]
                dsty = self.ypos + step[1]
                if(mode):
                    flag, errcode = self.match.is_move_valid(self.xpos, self.ypos, dstx, dsty, step[2])
                else:
                    flag, errcode = self.match.is_move_after_move_valid(self.xpos, self.ypos, dstx, dsty, step[2])
                if(flag):
                    moves.append(cGenMove(self.match, self.xpos, self.ypos, dstx, dsty, step[2]))
                elif(errcode == self.match.RETURN_CODES['out-of-bounds']):
                    break
        return moves

    def generate_priomoves(self):
        moves = []
        for direction in self.GEN_STEPS:
            for step in direction:
                dstx = self.xpos + step[0]
                dsty = self.ypos + step[1]
                flag, errcode = self.match.is_move_valid(self.xpos, self.ypos, dstx, dsty, step[2])
                if(flag):
                    gmove = cGenMove(self.match, self.xpos, self.ypos, dstx, dsty, step[2])
                    moves.append(cPrioMove(gmove))
                elif(errcode == self.match.RETURN_CODES['out-of-bounds']):
                    break
        return moves

# class end
