from . piece import *
from . rook import cRook
from . bishop import cBishop


class cKing(cPiece):
    STEPS = [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]
    GEN_STEPS = [ [[0, 1, PIECES['blk']]],
                  [[1, 1, PIECES['blk']]],
                  [[1, 0, PIECES['blk']]], 
                  [[1, -1, PIECES['blk']]],
                  [[0, -1, PIECES['blk']]], 
                  [[-1, -1, PIECES['blk']]],
                  [[-1, 0, PIECES['blk']]],
                  [[-1, 1, PIECES['blk']]],
                  [[2, 0, PIECES['blk']]],
                  [[-2, 0, PIECES['blk']]] ]
    MAXCNT = 1

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == 0 and step_y == 1):
            return DIRS['valid']
        elif(step_x == 1 and step_y == 1):
            return DIRS['valid']
        elif(step_x == 1 and step_y == 0):
            return DIRS['valid']
        elif(step_x == 1 and step_y == -1):
            return DIRS['valid']
        elif(step_x == 0 and step_y == -1):
            return DIRS['valid']
        elif(step_x == -1 and step_y == -1):
            return DIRS['valid']
        elif(step_x == -1 and step_y == 0):
            return DIRS['valid']
        elif(step_x == -1 and step_y == 1):
            return DIRS['valid']
        elif(step_x == 2 and step_y == 0):
            return DIRS['sh-castling']
        elif(step_x == -2 and step_y == 0):
            return DIRS['lg-castling']
        else:
            return DIRS['undefined']

    def is_trapped(self):
        return False # king cannot be trapped

    def is_piece_stuck(self):
        return False # king cannot stuck

    def is_move_stuck(self, dstx, dsty):
        return False # not used for king

    def is_attacked(self):
        return is_field_touched(self.match, self.xpos, self.ypos, REVERSED_COLORS[self.color], self.match.EVAL_MODES['ignore-pins'])

    def is_move_valid(self, dstx, dsty, prompiece=PIECES['blk']):
        opp_color = self.match.oppcolor_of_piece(self.piece)
        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == DIRS['sh-castling']):
            return self.is_sh_castling_ok(dstx, dsty)
        if(direction == DIRS['lg-castling']):
            return self.is_lg_castling_ok(dstx, dsty)
        if(direction == DIRS['undefined']):
            return False
        captured = self.match.board.readfield(dstx, dsty)
        ###
        self.match.board.writefield(self.xpos, self.ypos, PIECES['blk'])
        self.match.board.writefield(dstx, dsty, self.piece)
        attacked = is_field_touched(self.match, dstx, dsty, opp_color, self.match.EVAL_MODES['ignore-pins'])
        self.match.board.writefield(self.xpos, self.ypos, self.piece)
        self.match.board.writefield(dstx, dsty, captured)
        ##
        if(attacked == True):
            return False
        dstpiece = self.match.board.readfield(dstx, dsty)
        if(self.match.color_of_piece(dstpiece) == self.color):
            return False
        return True

################
    def do_move(self, dstx, dsty, prompiece=PIECES['blk']):
        board = self.match.board
        dstpiece = board.readfield(dstx, dsty)
        move = super().do_move(dstx, dsty, prompiece)

        if(dstx - self.xpos == 2):
            move.iscastling = True
            rook = board.readfield(self.xpos + 3, self.ypos)
            board.writefield(self.xpos + 3, self.ypos, PIECES['blk'])
            board.writefield(dstx - 1, dsty, rook)
        elif(dstx - self.xpos == -2):
            move.iscastling = True
            rook = board.readfield(self.xpos - 4, self.ypos)
            board.writefield(self.xpos - 4, self.ypos, PIECES['blk'])
            board.writefield(dstx + 1, dsty, rook)

        if(move.iscastling):
            if(self.color == COLORS['white']):
                if(board.white_movecnt_short_castling_lost == 0):
                    board.white_movecnt_short_castling_lost = move.count
                if(board.white_movecnt_long_castling_lost == 0):
                    board.white_movecnt_long_castling_lost = move.count
            else:
                if(board.black_movecnt_short_castling_lost == 0):
                    board.black_movecnt_short_castling_lost = move.count
                if(board.black_movecnt_long_castling_lost == 0):
                    board.black_movecnt_long_castling_lost = move.count

        if(self.piece == PIECES['wKg']):
            board.wKg_x = dstx
            board.wKg_y = dsty
        else:
            board.bKg_x = dstx
            board.bKg_y = dsty

        return move
################

################
    def undo_move(self, move):
        board = self.match.board
        super().undo_move(move)

        if(move.iscastling):
            if(move.dstx == 6):
                rook = board.readfield(move.dstx - 1, move.dsty)
                board.writefield(move.dstx - 1, move.dsty, PIECES['blk'])
                board.writefield(move.dstx + 1, move.dsty, rook)
            else:
                rook = board.readfield(move.dstx + 1, move.dsty)
                board.writefield(move.dstx + 1, move.dsty, PIECES['blk'])
                board.writefield(move.dstx - 2, move.dsty, rook)

        if(self.piece == PIECES['wKg']):
            board.wKg_x = move.srcx
            board.wKg_y = move.srcy
        else:
            board.bKg_x = move.srcx
            board.bKg_y = move.srcy

        return move
################

    def is_sh_castling_ok(self, dstx, dsty):
        opp_color = self.match.oppcolor_of_piece(self.piece)
        for i in range(1, 3, 1):
            fieldx = self.xpos + i
            field = self.match.board.readfield(fieldx, self.ypos)
            if(field != PIECES['blk']):
                return False
        if( self.match.is_inbounds(dstx + 1, dsty)):
            rook = self.match.board.readfield(dstx + 1, dsty)
        else:
            return False
        if(self.color == COLORS['white']):
            if(self.match.board.white_movecnt_short_castling_lost > 0 or rook != PIECES['wRk']):
                return False
        else:
            if(self.match.board.black_movecnt_short_castling_lost > 0 or rook != PIECES['bRk']):
                return False            
        self.match.board.writefield(self.xpos, self.ypos, PIECES['blk'])
        for i in range(3):
            castlingx = self.xpos + i
            attacked = is_field_touched(self.match, castlingx, self.ypos, opp_color, self.match.EVAL_MODES['ignore-pins'])
            if(attacked == True):
                self.match.board.writefield(self.xpos, self.ypos, self.piece)
                return False
        self.match.board.writefield(self.xpos, self.ypos, self.piece)
        return True

    def is_lg_castling_ok(self, dstx, dsty):
        opp_color = self.match.oppcolor_of_piece(self.piece)
        for i in range(1, 4, 1):
            fieldx = self.xpos - i
            field = self.match.board.readfield(fieldx, self.ypos)
            if(field != PIECES['blk']):
                return False
        if(self.match.is_inbounds(dstx - 2, dsty)):
            rook = self.match.board.readfield(dstx - 2, dsty)
        else:
            return False
        if(self.color == COLORS['white']):
            if(self.match.board.white_movecnt_long_castling_lost > 0 or rook != PIECES['wRk']):
                return False
        else:
            if(self.match.board.black_movecnt_long_castling_lost > 0 or rook != PIECES['bRk']):
                return False
        self.match.board.writefield(self.xpos, self.ypos, PIECES['blk'])
        for i in range(0, -3, -1):
            castlingx = self.xpos + i
            attacked = is_field_touched(self.match, castlingx, self.ypos, opp_color, self.match.EVAL_MODES['ignore-pins'])
            if(attacked == True):
                self.match.board.writefield(self.xpos, self.ypos, self.piece)
                return False
        self.match.board.writefield(self.xpos, self.ypos, self.piece)
        return True

    def move_controles_file(self, dstx, dsty):
        return False

    def score_touches(self):
        return 0

    def is_safe(self):
        count = 0
        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                friends, enemies = list_all_field_touches(self.match, x1, y1, self.color)
                if(len(friends) < len(enemies)):
                    return False
                if(len(enemies) > 0):
                    count += 1
        if(count > 2):
            return False
        friends.clear()
        enemies.clear()
        friends, enemies = list_all_field_touches(self.match, self.xpos, self.ypos, self.color)
        if(len(enemies) >= 2):
            return False
        for enemy in enemies:
            friends_beyond, enemies_beyond = list_all_field_touches(self.match, enemy.fieldx, enemy.fieldy, self.color)
            if(len(friends_beyond) >= len(enemies_beyond)):
                continue
            direction = cRook.dir_for_move(self.xpos, self.ypos, enemy.fieldx, enemy.fieldy)
            if(direction != DIRS['undefined']):
                stepx, stepy = cRook.step_for_dir(direction)
                if(stepx is None):
                    continue
            else:
                direction = cBishop.dir_for_move(self.xpos, self.ypos, enemy.fieldx, enemy.fieldy)
                if(direction != DIRS['undefined']):
                    stepx, stepy = cBishop.step_for_dir(direction)
                    if(stepx is None):
                        continue
                else:
                    return False
            x1 = self.xpos + stepx
            y1 = self.ypos + stepy
            while(self.match.is_inbounds(x1, y1)):
                blocking_friends, blocking_enemies = list_all_field_touches(self.match, x1, y1, self.color)
                if(len(blocking_friends) > 0):
                    break
        return True

    def is_centered(self):
        if(self.xpos >= 2 and self.xpos <= 5 and self.ypos >= 2 and self.ypos <= 5):
            return True
        else:
            return False

# class end

