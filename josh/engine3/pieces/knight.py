
from . piece import *


class cKnight(cPiece):
    STEPS = [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]
    GEN_STEPS = [ [[1, 2, PIECES['blk']]],
                  [[2, 1, PIECES['blk']]],
                  [[2, -1, PIECES['blk']]], 
                  [[1, -2, PIECES['blk']]],
                  [[-1, -2, PIECES['blk']]],
                  [[-2, -1, PIECES['blk']]],
                  [[-2, 1, PIECES['blk']]],
                  [[-1, 2, PIECES['blk']]] ]
    MAXCNT = 1

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == 1 and step_y == 2):
            return DIRS['valid']
        elif(step_x == 2 and step_y == 1):
            return DIRS['valid']
        elif(step_x == 2 and step_y == -1):
            return DIRS['valid']
        elif(step_x == 1 and step_y == -2):
            return DIRS['valid']
        elif(step_x == -1 and step_y == -2):
            return DIRS['valid']
        elif(step_x == -2 and step_y == -1):
            return DIRS['valid']
        elif(step_x == -2 and step_y == 1):
            return DIRS['valid']
        elif(step_x == -1 and step_y == 2):
            return DIRS['valid']
        else:
            return DIRS['undefined']

    def is_trapped(self):
        return False # knight cannot be trapped

    def is_move_valid(self, dstx, dsty, prompiece=PIECES['blk']):
        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == DIRS['undefined']):
            return False

        pin_dir = self.match.eval_pin_dir(self.xpos, self.ypos)
        if(pin_dir != DIRS['undefined']):
            return False

        dstpiece = self.match.board.readfield(dstx, dsty)
        if(self.match.color_of_piece(dstpiece) == self.color):
            return False

        return True

    def move_controles_file(self, dstx, dsty):
        return False

# class end

