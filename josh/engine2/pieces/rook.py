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

    def does_move_effect_short_castling(self, move):
        board = self.match.board
        if(self.color == COLORS['white']):
            if(board.white_movecnt_short_castling_lost == 0 and 
               move.srcx == board.COLS['H'] and move.srcy == board.RANKS['1']):
                return True, COLORS['white']
            else:
                return super().does_move_effect_short_castling(move)
        else:
            if(board.black_movecnt_short_castling_lost == 0 and 
               move.srcx == board.COLS['H'] and move.srcy == board.RANKS['8']):
                return True, COLORS['black']
            else:
                return super().does_move_effect_short_castling(move)

    def does_move_effect_long_castling(self, move):
        board = self.match.board
        if(self.color == COLORS['white']):
            if(board.white_movecnt_long_castling_lost == 0 and 
               move.srcx == board.COLS['A'] and move.srcy == board.RANKS['1']):
                return True, COLORS['white']
            else:
                return super().does_move_effect_long_castling(move)
        else:
            if(board.black_movecnt_long_castling_lost == 0 and 
               move.srcx == board.COLS['A'] and move.srcy == board.RANKS['8']):
                return True, COLORS['black']
            else:
                return super().does_move_effect_short_castling(move)

# class end

