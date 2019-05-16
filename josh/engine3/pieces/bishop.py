from . piece import *


class cBishop(cPiece):
    DIRS_ARY = [DIRS['north-east'], DIRS['south-west'], DIRS['north-west'], DIRS['south-east']]
    STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
    GEN_STEPS = [ [[1, 1, PIECES['blk']],   [2, 2, PIECES['blk']],   [3, 3, PIECES['blk']],   [4, 4, PIECES['blk']],   [5, 5, PIECES['blk']],   [6, 6, PIECES['blk']],   [7, 7, PIECES['blk']]],
                  [[-1, -1, PIECES['blk']], [-2, -2, PIECES['blk']], [-3, -3, PIECES['blk']], [-4, -4, PIECES['blk']], [-5, -5, PIECES['blk']], [-6, -6, PIECES['blk']], [-7, -7, PIECES['blk']]],
                  [[1, -1, PIECES['blk']],  [2, -2, PIECES['blk']],  [3, -3, PIECES['blk']],  [4, -4, PIECES['blk']],  [5, -5, PIECES['blk']],  [6, -6, PIECES['blk']],  [7, -7, PIECES['blk']]],
                  [[-1, 1, PIECES['blk']],  [-2, 2, PIECES['blk']],  [-3, 3, PIECES['blk']],  [-4, 4, PIECES['blk']],  [-5, 5, PIECES['blk']],  [-6, 6, PIECES['blk']],  [-7, 7, PIECES['blk']]] ]

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        if( (srcx - dstx) == (srcy - dsty) and (srcy < dsty) ):
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
        if(direction == DIRS['north-east']):
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

