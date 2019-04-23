
from .. values import *
from .. move import cGenMove


class cPawnField:
    def __init__(self, match, fieldx, fieldy):
        self.match = match
        self.fieldx = fieldx
        self.fieldy = fieldy

    def generate_moves_from_reverse(self, color):
        moves = []
        if(color == COLORS['white']):
            ysteps = [-1, -2]
        else:
            ysteps = [1, 2]
        for ystep in ysteps:
            if(self.match.is_move_valid(self.fieldx, self.fieldy + ystep, self.fieldx, self.fieldy, PIECES['blk'])[0]):
                moves.append(cGenMove(self.match, self.fieldx, self.fieldy + ystep, self.fieldx, self.fieldy, PIECES['blk']))
        return moves

# class end

