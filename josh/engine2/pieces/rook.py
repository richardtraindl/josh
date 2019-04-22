from .piece import *


class cRook(cPiece):
    DIRS_ARY = [DIRS['north'], DIRS['south'], DIRS['east'], DIRS['west']]
    STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    GEN_STEPS = [ [[0, 1, PIECES['blk']],   [0, 2,  PIECES['blk']],  [0, 3,  PIECES['blk']],  [0, 4,  PIECES['blk']],  [0, 5,  PIECES['blk']],  [0, 6,  PIECES['blk']],  [0, 7,  PIECES['blk']]],
                  [[0, -1,  PIECES['blk']], [0, -2,  PIECES['blk']], [0, -3,  PIECES['blk']], [0, -4,  PIECES['blk']], [0, -5,  PIECES['blk']], [0, -6,  PIECES['blk']], [0, -7,  PIECES['blk']]],
                  [[1, 0,  PIECES['blk']],  [2, 0,  PIECES['blk']],  [3, 0,  PIECES['blk']],  [4, 0,  PIECES['blk']],  [5, 0,  PIECES['blk']],  [6, 0,  PIECES['blk']],  [7, 0,  PIECES['blk']]],
                  [[-1, 0,  PIECES['blk']], [-2, 0,  PIECES['blk']], [-3, 0,  PIECES['blk']], [-4, 0,  PIECES['blk']], [-5, 0,  PIECES['blk']], [-6, 0,  PIECES['blk']], [-7, 0,  PIECES['blk']]] ]

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
        else:
            return None, None

################
    def do_move(self, dstx, dsty, prompiece=PIECES['blk']):
        board = self.match.board
        dstpiece = board.readfield(dstx, dsty)
        move = super().do_move(dstx, dsty, prompiece)

        if(self.color == COLORS['white']):
            if(self.xpos == board.COLS['A'] and self.ypos == board.RANKS['1'] and board.wRkA_first_move_on is None):
                board.wRkA_first_move_on = move.count
            elif(self.xpos == board.COLS['H'] and self.ypos == board.RANKS['1'] and board.wRkH_first_move_on is None):
                board.wRkH_first_move_on = move.count
        else:
            if(self.xpos == board.COLS['A'] and self.ypos == board.RANKS['8'] and board.bRkA_first_move_on is None):
                board.bRkA_first_move_on = move.count
            elif(self.xpos == board.COLS['H'] and self.ypos == board.RANKS['8'] and board.bRkH_first_move_on is None):
                board.bRkH_first_move_on = move.count

        return move

    def undo_move(self, move):
        board = self.match.board
        super().undo_move(move)

        if(self.piece == PIECES['wRk']):
            if(board.wRkA_first_move_on is not None and board.wRkA_first_move_on == move.count):
                board.wRkA_first_move_on = None
            elif(board.wRkH_first_move_on is not None and board.wRkH_first_move_on == move.count):
                board.wRkH_first_move_on = None
        else:
            if(board.bRkA_first_move_on is not None and board.bRkA_first_move_on == move.count):
                board.bRkA_first_move_on = None
            elif(board.bRkH_first_move_on is not None and board.bRkH_first_move_on == move.count):
                board.bRkH_first_move_on = None

        return move

# class end

