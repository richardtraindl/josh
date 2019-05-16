
from .piece import *


class cQueen(cPiece):
    DIRS_ARY = [DIRS['north'], DIRS['south'], DIRS['east'], DIRS['west'], DIRS['north-east'], DIRS['south-west'], DIRS['north-west'], DIRS['south-east']]
    STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]
    GEN_STEPS = [ [[0, 1, PIECES['blk']],   [0, 2, PIECES['blk']],   [0, 3, PIECES['blk']],   [0, 4, PIECES['blk']],   [0, 5, PIECES['blk']],   [0, 6, PIECES['blk']],   [0, 7, PIECES['blk']]],
                  [[0, -1, PIECES['blk']],  [0, -2, PIECES['blk']],  [0, -3, PIECES['blk']],  [0, -4, PIECES['blk']],  [0, -5, PIECES['blk']],  [0, -6, PIECES['blk']],  [0, -7, PIECES['blk']]],
                  [[1, 0, PIECES['blk']],   [2, 0, PIECES['blk']],   [3, 0, PIECES['blk']],   [4, 0, PIECES['blk']],   [5, 0, PIECES['blk']],   [6, 0, PIECES['blk']],   [7, 0, PIECES['blk']]],
                  [[-1, 0, PIECES['blk']],  [-2, 0, PIECES['blk']],  [-3, 0, PIECES['blk']],  [-4, 0, PIECES['blk']],  [-5, 0, PIECES['blk']],  [-6, 0, PIECES['blk']],  [-7, 0, PIECES['blk']]],
                  [[1, 1, PIECES['blk']],   [2, 2, PIECES['blk']],   [3, 3, PIECES['blk']],   [4, 4, PIECES['blk']],   [5, 5, PIECES['blk']],   [6, 6, PIECES['blk']],   [7, 7, PIECES['blk']]],
                  [[-1, -1, PIECES['blk']], [-2, -2, PIECES['blk']], [-3, -3, PIECES['blk']], [-4, -4, PIECES['blk']], [-5, -5, PIECES['blk']], [-6, -6, PIECES['blk']], [-7, -7, PIECES['blk']]],
                  [[1, -1, PIECES['blk']],  [2, -2, PIECES['blk']],  [3, -3, PIECES['blk']],  [4, -4, PIECES['blk']],  [5, -5, PIECES['blk']],  [6, -6, PIECES['blk']],  [7, -7, PIECES['blk']]],
                  [[-1, 1, PIECES['blk']],  [-2, 2, PIECES['blk']],  [-3, 3, PIECES['blk']],  [-4, 4, PIECES['blk']],  [-5, 5, PIECES['blk']],  [-6, 6, PIECES['blk']],  [-7, 7, PIECES['blk']]] ]

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        if( (srcx == dstx) and (srcy < dsty) ):
            return DIRS['north']
        elif( (srcx == dstx) and (srcy > dsty) ):
            return DIRS['south']
        elif( (srcx < dstx) and (srcy == dsty) ):
            return DIRS['east']
        elif( (srcx > dstx) and (srcy == dsty) ):
            return DIRS['west']
        elif( (srcx - dstx) == (srcy - dsty) and (srcy < dsty) ):
            return DIRS['north-east']
        elif( (srcx - dstx) == (srcy - dsty) and (srcy > dsty) ):
            return DIRS['south-west']
        elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy < dsty) ):
            return DIRS['north-west']
        elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy > dsty) ):
            return DIRS['south-east']
        else:
            return DIRS['undefined']

    @classmethod
    def step_for_dir(cls, direction):
        if(direction == DIRS['north']):
            return 0, 1
        elif(direction == DIRS['south']):
            return 0, -1
        elif(direction == DIRS['east']):
            return 1, 0
        elif(direction == DIRS['west']):
            return -1, 0
        elif(direction == DIRS['north-east']):
            return 1, 1
        elif(direction == DIRS['south-west']):
            return -1, -1
        elif(direction == DIRS['north-west']):
            return -1, 1
        elif(direction == DIRS['south-east']):
            return 1, -1
        else:
            return None, None

# class end

