
from .. values import *
from .piece import cPiece
from .rook import cRook
from .bishop import cBishop


class cQueen(cPiece):
    DIRS_ARY = [DIRS['nth'], DIRS['sth'], DIRS['est'], DIRS['wst'], DIRS['nth-est'], DIRS['sth-wst'], DIRS['nth-wst'], DIRS['sth-est']]
    STEPS = [8, -8, 1, -1, 9, -9, 7, -7]  
    GEN_STEPS = [ [[8, PIECES['blk']],   [16, 0, PIECES['blk']],  [24, PIECES['blk']],  [32, PIECES['blk']],  [40, PIECES['blk']],  [48, PIECES['blk']],  [56, PIECES['blk']]],
                  [[-8, PIECES['blk']],  [-16, 0, PIECES['blk']], [-24, PIECES['blk']], [-32, PIECES['blk']], [-40, PIECES['blk']], [-48, PIECES['blk']], [-56, PIECES['blk']]],
                  [[1, PIECES['blk']],   [2, PIECES['blk']],      [3, PIECES['blk']],   [4, PIECES['blk']],   [5, PIECES['blk']],   [6, PIECES['blk']],   [7, PIECES['blk']]],
                  [[-1,  PIECES['blk']], [-2, PIECES['blk']],     [-3, PIECES['blk']],  [-4, PIECES['blk']],  [-5, PIECES['blk']],  [-6, PIECES['blk']],  [-7, PIECES['blk']]],
                  [[9, PIECES['blk']],   [18, PIECES['blk']],     [27, PIECES['blk']],  [36, PIECES['blk']],  [45, PIECES['blk']],  [54, PIECES['blk']],  [63, PIECES['blk']]],
                  [[-9, PIECES['blk']],  [-18, PIECES['blk']],    [-27, PIECES['blk']], [-36, PIECES['blk']], [-45, PIECES['blk']], [-54, PIECES['blk']], [-63, PIECES['blk']]],
                  [[7, PIECES['blk']],   [14, PIECES['blk']],     [21, PIECES['blk']],  [28, PIECES['blk']],  [35, PIECES['blk']],  [42, PIECES['blk']],  [49, PIECES['blk']]],
                  [[-7, PIECES['blk']],  [-14, PIECES['blk']],    [-21, PIECES['blk']], [-28, PIECES['blk']], [-35, PIECES['blk']], [-42, PIECES['blk']], [-49, PIECES['blk']]] ]

    def __init__(self, match, pos):
        super().__init__(match, pos)

    @classmethod
    def dir_for_move(cls, src, dst):
        direction = cRook.dir_for_move(src, dst)
        if(direction != DIRS['undef']):
            return direction
        return cBishop.dir_for_move(src, dst)

    @classmethod
    def step_for_dir(cls, direction):
        if(direction == DIRS['nth']):
            return 8
        elif(direction == DIRS['sth']):
            return -8
        elif(direction == DIRS['est']):
            return 1
        elif(direction == DIRS['wst']):
            return -1
        elif(direction == DIRS['nth-est']):
            return 9
        elif(direction == DIRS['sth-wst']):
            return -9
        elif(direction == DIRS['nth-wst']):
            return 7
        elif(direction == DIRS['sth-est']):
            return -7
        else:
            return None

# class end

