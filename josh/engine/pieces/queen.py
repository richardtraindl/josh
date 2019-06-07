
from .. values import *
from .piece import cPiece
from .rook import cRook
from .bishop import cBishop


class cQueen(cPiece):
    DIRS_ARY = cRook.DIRS_ARY
    DIRS_ARY.extend(cBishop.DIRS_ARY)
    STEPS    = cRook.STEPS
    STEPS.extend(cBishop.STEPS)
    MV_STEPS = cRook.MV_STEPS
    MV_STEPS.extend(cBishop.MV_STEPS)

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

