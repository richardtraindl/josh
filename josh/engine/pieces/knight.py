
from .. values import *
from .piece import cPiece


class cKnight(cPiece):
    STEPS    = [17, 10, -6, -15, -17, -10, 6, 15]
    MV_STEPS = [[17, PIECES['blk']],  [10, PIECES['blk']],  [-6, PIECES['blk']], [-15, PIECES['blk']], 
                [-17, PIECES['blk']], [-10, PIECES['blk']], [6, PIECES['blk']],  [15, PIECES['blk']]]
    MAXCNT = 1

    def __init__(self, match, pos):
        super().__init__(match, pos)

    def is_trapped(self):
        return False # knight cannot be trapped

    def is_move_valid(self, dst, prompiece=PIECES['blk']):
        flag = False
        for step in self.STEPS:
            if((self.pos + step) == dst and 
                self.match.board.is_inbounds(self.pos, dst, step)):
                flag = True
                break
        if(flag == False):
            return False
        pin_dir = self.match.eval_pin_dir(self.pos)
        if(pin_dir != DIRS['undef']):
            return False
        dstpiece = self.match.board.getfield(dst)
        if(self.match.color_of_piece(dstpiece) == self.color):
            return False
        return True

# class end

