
from .. values import *
from .piece import cPiece
from .searchforpiece import is_field_touched, list_all_field_touches


class cKing(cPiece):
    STEPS    = [8, 9, 1, -7, -8, -9, -1, 7]
    MV_STEPS = [[8, PIECES['blk']],  [9, PIECES['blk']],  [1, PIECES['blk']],  [-7, PIECES['blk']], 
                [-8, PIECES['blk']], [-9, PIECES['blk']], [-1, PIECES['blk']], [ 7, PIECES['blk']],
                [2, PIECES['blk']],  [-2, PIECES['blk']]]
    MAXCNT = 1

    def __init__(self, match, pos):
        super().__init__(match, pos)

    def is_move_stuck(self, dst):
        return False # not useful for king

    def is_trapped(self):
        return False # king cannot be trapped

    def is_move_valid(self, dst, prompiece=PIECES['blk']):
        if(self.is_short_castling_ok(dst)):
            return True
        if(self.is_long_castling_ok(dst)):
            return True
        opp_color = self.match.oppcolor_of_piece(self.piece)
        flag = False
        for step in self.STEPS:
            if((self.pos + step) == dst and 
                self.match.board.is_inbounds(self.pos, dst, step)):
                flag = True
                break
        if(flag == False):
            return False
        captured = self.match.board.getfield(dst)
        ###
        self.match.board.setfield(self.pos, PIECES['blk'])
        self.match.board.setfield(dst, self.piece)
        attacked = is_field_touched(self.match, dst, opp_color, self.match.EVAL_MODES['ignore-pins'])
        self.match.board.setfield(self.pos, self.piece)
        self.match.board.setfield(dst, captured)
        ##
        if(attacked == True):
            return False
        dstpiece = self.match.board.getfield(dst)
        if(self.match.color_of_piece(dstpiece) == self.color):
            return False
        return True

    def is_short_castling_ok(self, dst):
        if(self.pos - dst != -2):
            return False
        if(self.color == COLORS['white']):
            shorttest  = 0x0000600400000000000000000000000000000000000000000000000000000000
            shortmask  = 0x0000FFFF00000000000000000000000000000000000000000000000000000000
        else:
            shorttest  = 0x000000000000000000000000000000000000000000000000000000000000E00C
            shortmask  = 0x000000000000000000000000000000000000000000000000000000000000FFFF            
        fields = self.match.board.fields & shortmask
        if(fields != shorttest):
            return False
        if(self.color == COLORS['white']):
            if(self.match.board.wKg_first_move_on is not None or 
               self.match.board.wRkH_first_move_on is not None):
                return False
        else:
            if(self.match.board.bKg_first_move_on is not None or 
               self.match.board.bRkH_first_move_on is not None):
                return False
        self.match.board.setfield(self.pos, PIECES['blk'])
        for i in range(3):
            dst2 = self.pos + i
            attacked = is_field_touched(self.match, dst2, self.match.oppcolor_of_piece(self.piece), self.match.EVAL_MODES['ignore-pins'])
            if(attacked == True):
                self.match.board.setfield(self.pos, self.piece)
                return False
        self.match.board.setfield(self.pos, self.piece)
        return True

    def is_long_castling_ok(self, dst):
        if(self.pos - dst != 2):
            return False
        if(self.color == COLORS['white']):
            longtest  = 0x4000600000000000000000000000000000000000000000000000000000000000
            longmask  = 0xFFFFF00000000000000000000000000000000000000000000000000000000000
        else:
            longtest  = 0x00000000000000000000000000000000000000000000000000000000C000E000
            longmask  = 0x00000000000000000000000000000000000000000000000000000000FFFFF000            
        fields = self.match.board.fields & longmask
        if(fields != longtest):
            return False
        if(self.color == COLORS['white']):
            if(self.match.board.wKg_first_move_on is not None or 
               self.match.board.wRkA_first_move_on is not None):
                return False
        else:
            if(self.match.board.bKg_first_move_on is not None or 
               self.match.board.bRkA_first_move_on is not None):
                return False
        self.match.board.setfield(self.pos, PIECES['blk'])
        for i in range(3):
            dst2 = self.pos - i
            attacked = is_field_touched(self.match, dst2, self.match.oppcolor_of_piece(self.piece), self.match.EVAL_MODES['ignore-pins'])
            if(attacked == True):
                self.match.board.setfield(self.pos, self.piece)
                return False
        self.match.board.setfield(self.pos, self.piece)
        return True

    def do_move(self, dst, prompiece=PIECES['blk'], movecnt=None):
        board = self.match.board
        dstpiece = board.getfield(dst)
        move = super().do_move(dst, prompiece)
        if(self.pos - dst == -2):
            rook = board.getfield(self.pos + 3)
            board.setfield(self.pos + 3, PIECES['blk'])
            board.setfield(dst - 1, rook)
        elif(self.pos - dst == 2):
            rook = board.getfield(self.pos - 4)
            board.setfield(self.pos - 4, PIECES['blk'])
            board.setfield(dst + 1, rook)
        if(self.piece == PIECES['wKg']):
            if(board.wKg_first_move_on is None):
                board.wKg_first_move_on = movecnt
            board.wKg = dst
        else:
            if(board.bKg_first_move_on is None):
                board.bKg_first_move_on = movecnt
            board.bKg = dst
        return move

    def undo_move(self, move, movecnt):
        board = self.match.board
        super().undo_move(move)
        if(self.piece == PIECES['wKg']):
            if(board.wKg_first_move_on is not None and 
               board.wKg_first_move_on == movecnt):
                board.wKg_first_move_on = None
            board.wKg = move.src
        else:
            if(board.bKg_first_move_on is not None and 
               board.bKg_first_move_on == movecnt):
                board.bKg_first_move_on = None
            board.bKg = move.src
        return move

    def score_touches(self):
        return 0

    def is_safe(self):
        count = 0
        for step in self.STEPS:
            dst = self.pos + step
            if(self.match.board.is_inbounds(self.pos, dst, step)):
                friends, enemies = list_all_field_touches(self.match, dst, self.color)
                if(len(friends) < len(enemies)):
                    return False
                if(len(enemies) > 0):
                    count += 1
        if(count > 2):
            return False
        friends.clear()
        enemies.clear()
        friends, enemies = list_all_field_touches(self.match, self.pos, self.color)
        if(len(enemies) == 0):
            return True
        if(len(enemies) >= 2):
            return False
        else:
            enemy = enemies[0]
            friends_beyond, enemies_beyond = list_all_field_touches(self.match, enemy.field, self.color)
            if(len(friends_beyond) >= len(enemies_beyond)):
                return True
            cenemy = self.match.obj_for_piece(enemy.piece, enemy.field)
            direction = cenemy.dir_for_move(self.pos, enemy.field)
            if(direction == DIRS['undef']):
                return True
            else:
                step = cenemy.step_for_dir(direction)
            dst = self.pos + step
            while(self.match.board.is_inbounds(self.pos, dst, step)):
                blocking_friends, blocking_enemies = list_all_field_touches(self.match, dst, self.color)
                if(len(blocking_friends) > 0):
                    return True
                dst += step
        return False

# class end