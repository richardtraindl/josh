
from .. values import *
from .. board import cBoard
from .piece import cPiece


class cBishop(cPiece):
    DIRS_ARY = [DIRS['nth-est'], DIRS['sth-wst'], DIRS['nth-wst'], DIRS['sth-est']]
    STEPS = [9, -9, 7, -7]
    GEN_STEPS = [ [[9, PIECES['blk']],  [18, PIECES['blk']],  [27, PIECES['blk']],  [36, PIECES['blk']],  [45, PIECES['blk']],  [54, PIECES['blk']],  [63, PIECES['blk']]],
                  [[-9, PIECES['blk']], [-18, PIECES['blk']], [-27, PIECES['blk']], [-36, PIECES['blk']], [-45, PIECES['blk']], [-54, PIECES['blk']], [-63, PIECES['blk']]],
                  [[7, PIECES['blk']],  [14, PIECES['blk']],  [21, PIECES['blk']],  [28, PIECES['blk']],  [35, PIECES['blk']],  [42, PIECES['blk']],  [49, PIECES['blk']]],
                  [[-7, PIECES['blk']], [-14, PIECES['blk']], [-21, PIECES['blk']], [-28, PIECES['blk']], [-35, PIECES['blk']], [-42, PIECES['blk']], [-49, PIECES['blk']]] ]

    def __init__(self, match, pos):
        super().__init__(match, pos)

    @classmethod
    def dir_for_move(cls, src, dst):
        if(cBoard.is_inbounds_core(src, dst) == False):
            return DIRS['undef']
        if(cBoard.is_nth_est(src, dst)):
            return DIRS['nth-est']
        elif(cBoard.is_sth_wst(src, dst)):
            return DIRS['sth-wst']
        elif(cBoard.is_sth_est(src, dst) == True):
            return DIRS['sth-est']
        elif(cBoard.is_nth_wst(src, dst) == True):
            return DIRS['nth-wst']
        else:
            return DIRS['undef']

    @classmethod
    def step_for_dir(cls, direction):
        if(direction == DIRS['nth-est']):
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

