
from .. values import *
from .. board import cBoard
from .piece import cPiece


class cPawn(cPiece):
    def __init__(self, match, pos):
        super().__init__(match, pos)

    def is_trapped(self):
        return False # pawn cannot be trapped

    def do_move(self, dst, prompiece=PIECES['blk'], movecnt=None):
        board = self.match.board
        dstpiece_before_mv = board.getfield(dst)
        move = super().do_move(dst, prompiece)
        if(prompiece and prompiece != PIECES['blk']):
            board.setfield(dst, prompiece)
            self.match.score -= SCORES[prompiece] - SCORES[self.piece]
        elif(dstpiece_before_mv == PIECES['blk'] and self.pos % 8 != dst % 8):
            if(self.pos % 8 < dst % 8):
                enpass = self.pos + 1
            else:
                enpass = self.pos - 1
            captpiece = board.getfield(enpass)
            board.setfield(enpass, PIECES['blk'])
            self.match.score += SCORES[captpiece]
        return move

    def undo_move(self, move, movecnt=None):
        board = self.match.board
        super().undo_move(move)
        dstpiece_after_undo_mv = board.getfield(move.dst)
        if(move.prompiece and move.prompiece != PIECES['blk']):
            if(self.color == COLORS['white']):
                origin = PIECES['wPw']
            else:
                origin = PIECES['bPw']
            self.match.score += (SCORES[move.prompiece] - SCORES[origin])
        elif(dstpiece_after_undo_mv == PIECES['blk'] and move.src % 8 != move.dst % 8):
                if(self.color == COLORS['white']):
                    enemy = PIECES['bPw']
                else:
                    enemy = PIECES['wPw']
                self.match.score -= SCORES[enemy]
        return move

    def is_running(self):
        if(self.color == COLORS['white']):
            step = 8
            opp_pawn = PIECES['bPw']
        else:
            step = -8
            opp_pawn = PIECES['wPw']
        for idx in range(-1, 2, 1):
            src = self.pos + idx
            dst = self.match.board.search(src, step, 5)
            while(dst):
                piece = self.match.board.getfield(dst)
                if(piece == opp_pawn):
                    return False
                dst = self.match.board.search(dst, step, 5)
        return True

 # class end

