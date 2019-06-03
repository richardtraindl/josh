
from .. values import *
from .. move import cMove


class cPawnField:
    def __init__(self, match, field):
        self.match = match
        self.field = field

    def generate_moves_from_reverse(self, color):
        moves = []
        if(color == COLORS['white']):
            ysteps = [-1, -2]
        else:
            ysteps = [1, 2]
        for ystep in ysteps:
            if(self.match.is_move_valid(self.field + (self.field // 8 + ystep) * 8, self.field, PIECES['blk'])[0]):
                moves.append(cMove(self.field + (self.field // 8 + ystep) , self.field, PIECES['blk']))
        return moves

# class end

