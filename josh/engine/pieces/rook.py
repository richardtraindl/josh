
from .. values import *
from .. board import cBoard
from .piece import cPiece


class cRook(cPiece):
    DIRS_ARY = [DIRS['nth'], DIRS['sth'], DIRS['est'], DIRS['wst']]
    STEPS    = [8, -8, 1, -1]
    MV_STEPS = [[8, PIECES['blk']], [-8, PIECES['blk']],  [1, PIECES['blk']], [-1, PIECES['blk']]]

    def __init__(self, match, pos):
        super().__init__(match, pos)

    @classmethod
    def dir_for_move(cls, src, dst):
        if(cBoard.is_inbounds_core(src, dst) == False):
            return DIRS['undef']
        if(cBoard.is_nth(src, dst)):
            return DIRS['nth']
        elif(cBoard.is_sth(src, dst)):
            return DIRS['sth']
        elif(cBoard.is_est(src, dst)):
            return DIRS['est']
        elif(cBoard.is_wst(src, dst)):
            return DIRS['wst']
        else:
            return DIRS['undef']

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
        else:
            return None

    def do_move(self, dst, prompiece=PIECES['blk'], movecnt=None):
        board = self.match.board
        dstpiece = board.getfield(dst)
        move = super().do_move(dst, prompiece)
        srcx = self.pos % 8
        srcy = self.pos // 8
        if(self.color == COLORS['white']):
            if(srcx == board.COLS['A'] and srcy == board.RANKS['1'] and 
               board.wRkA_first_move_on is None):
                board.wRkA_first_move_on = movecnt
            elif(srcx == board.COLS['H'] and srcy == board.RANKS['1'] and 
                 board.wRkH_first_move_on is None):
                board.wRkH_first_move_on = movecnt
        else:
            if(srcx == board.COLS['A'] and srcy == board.RANKS['8'] and 
               board.bRkA_first_move_on is None):
                board.bRkA_first_move_on = movecnt
            elif(srcx == board.COLS['H'] and srcy == board.RANKS['8'] and 
                 board.bRkH_first_move_on is None):
                board.bRkH_first_move_on = movecnt
        return move

    def undo_move(self, move, movecnt):
        board = self.match.board
        super().undo_move(move)
        if(self.piece == PIECES['wRk']):
            if(board.wRkA_first_move_on is not None and board.wRkA_first_move_on == movecnt):
                board.wRkA_first_move_on = None
            elif(board.wRkH_first_move_on is not None and board.wRkH_first_move_on == movecnt):
                board.wRkH_first_move_on = None
        else:
            if(board.bRkA_first_move_on is not None and board.bRkA_first_move_on == movecnt):
                board.bRkA_first_move_on = None
            elif(board.bRkH_first_move_on is not None and board.bRkH_first_move_on == movecnt):
                board.bRkH_first_move_on = None
        return move

# class end
