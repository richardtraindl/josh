from datetime import datetime
from .values import *
from .board import cBoard
from .pieces.white_pawn import cWhitePawn
from .pieces.black_pawn import cBlackPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .pieces.pawnfield import cPawnField
from .pieces.search_for_piece import cSearchForRook, cSearchForBishop, is_field_touched


class cMatch:
    STATUS = {
            'open' : 10,
            'draw' : 11,
            'winner_white' : 12,
            'winner_black' : 13,
            'paused' : 14,
            'setup' : 15 }

    LEVELS = {
            'blitz' : 0,
            'low' : 1,
            'medium' : 2,
            'high' : 3 }

    SECONDS_PER_MOVE = {
            LEVELS['blitz'] : 15,
            LEVELS['low'] : 30,
            LEVELS['medium'] : 60,
            LEVELS['high'] : 90 }

    RETURN_CODES = {
        'ok' : 10,
        'draw' : 11,
        'winner_white' : 12,
        'winner_black' : 13,
        'match-cancelled' : 14,
        'wrong-color' : 15,
        'piece-error' : 16,
        'king-attacked-error' : 17,
        'format-error' : 18,
        'out-of-bounds' : 19,
        'general-error' : 20,
    }

    RETURN_MSGS = {
        RETURN_CODES['ok'] : "move okay",
        RETURN_CODES['draw'] : "draw",
        RETURN_CODES['winner_white'] : "winner white",
        RETURN_CODES['winner_black'] : "winner black",
        RETURN_CODES['match-cancelled'] : " match is cancelled",
        RETURN_CODES['wrong-color'] : "wrong color",
        RETURN_CODES['piece-error'] : "piece error",
        RETURN_CODES['king-attacked-error'] : "king attacked error",
        RETURN_CODES['format-error'] : "format wrror",
        RETURN_CODES['out-of-bounds'] : "wrong square",
        RETURN_CODES['general-error'] : "general error",
    }

    EVAL_MODES = {
        'ignore-pins' : 0,
        'only-pins-to-king' : 1,
        'all-pins' : 2
    }

    def __init__(self):
        self.status = self.STATUS['open']
        self.score = 0
        self.level = self.LEVELS['blitz']
        self.board = cBoard()
        self.move_list = []
        self.candidate_list = []

    def update_attributes(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            for move in self.move_list:
                if(self.board.white_movecnt_short_castling_lost == move.count):
                    self.board.white_movecnt_short_castling_lost = move.count
                if(self.board.white_movecnt_long_castling_lost == move.count):
                    self.board.white_movecnt_long_castling_lost = move.count
                if(self.board.black_movecnt_short_castling_lost == move.count):
                    self.board.black_movecnt_short_castling_lost = move.count
                if(self.board.black_movecnt_long_castling_lost == move.count):
                    self.board.black_movecnt_long_castling_lost = move.count

        self.score = 0
        self.board.wQu_cnt = 0
        self.board.bQu_cnt = 0
        self.board.wOfficer_cnt = 0
        self.board.bOfficer_cnt = 0
        for y in range(8):
            for x in range(8):
                piece = self.board.readfield(x, y)
                self.score -= SCORES[piece]
                if(piece == PIECES['wKg']):
                    self.board.wKg_x = x
                    self.board.wKg_y = y
                elif(piece == PIECES['bKg']):
                    self.board.bKg_x = x
                    self.board.bKg_y = y
                else:
                    self.board.update_officer_counter(piece, 1)
    # update_attributes() end

    def movecnt(self):
        return len(self.move_list)

    def next_color(self):
        if(len(self.move_list) % 2 == 0 ):
            return COLORS['white']
        else:
            return COLORS['black']

    def is_opening(self):
        count = self.board.wQu_cnt + self.board.wOfficer_cnt + self.board.bQu_cnt + self.board.bOfficer_cnt
        return (len(self.move_list) <= 20 and count > 8)

    def is_endgame(self):
        count = self.board.wQu_cnt + self.board.wOfficer_cnt + self.board.bQu_cnt + self.board.bOfficer_cnt
        return count <= 6

    def is_fifty_moves_rule(self):
        # 100 Züge davor kein Bauernzug und keine Figur geschlagen
        return False

    def is_last_move_capture(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            if(move.captpiece != PIECES['blk']):
                return True

        return False

    def is_last_move_promotion(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            if(move.prompiece != PIECES['blk']):
                return True

        return False

    def read_move_list(self, idx):
        if(len(self.move_list) > 0):
            return self.move_list[idx]
        else:
            return None

    @classmethod
    def color_of_piece(cls, piece):
        return PIECES_COLOR[piece]

    @classmethod
    def oppcolor_of_piece(cls, piece):
        color = PIECES_COLOR[piece]
        return REVERSED_COLORS[color]

    def is_inbounds(self, x, y):
        return self.board.is_inbounds(x, y)

    def is_move_inbounds(self, srcx, srcy, dstx, dsty):
        return self.board.is_move_inbounds(srcx, srcy, dstx, dsty)

    def is_move_valid(self, srcx, srcy, dstx, dsty, prompiece):
        if(not self.is_move_inbounds(srcx, srcy, dstx, dsty)):
            return False, self.RETURN_CODES['out-of-bounds']
        piece = self.board.readfield(srcx, srcy)
        if(self.next_color() != self.color_of_piece(piece)):
            return False, self.RETURN_CODES['wrong-color']
        if(piece != PIECES['wKg'] and piece != PIECES['bKg']):
            if(self.is_king_after_move_attacked(srcx, srcy, dstx, dsty)):
                return False, self.RETURN_CODES['king-attacked-error']
        cpiece = self.obj_for_piece(piece, srcx, srcy)
        if(cpiece):
            if(cpiece.is_move_valid(dstx, dsty, prompiece)):
                return True, self.RETURN_CODES['ok']
            else:
                return False, self.RETURN_CODES['piece-error']
        else:
            return False, self.RETURN_CODES['general-error']

    def is_move_after_move_valid(self, srcx, srcy, dstx, dsty, prompiece):
        if(not self.is_move_inbounds(srcx, srcy, dstx, dsty)):
            return False, self.RETURN_CODES['out-of-bounds']
        piece = self.board.readfield(srcx, srcy)
        cpiece = self.obj_for_piece(piece, srcx, srcy)
        if(cpiece is not None):
            if(cpiece.is_move_valid(dstx, dsty, prompiece)):
                return True, self.RETURN_CODES['ok']
            else:
                return False, self.RETURN_CODES['piece-error']
        else:
            return False, self.RETURN_CODES['general-error']

    def do_move(self, srcx, srcy, dstx, dsty, prompiece):
        piece = self.board.readfield(srcx, srcy)
        cpiece = self.obj_for_piece(piece, srcx, srcy)
        if(cpiece):
            move = cpiece.do_move(dstx, dsty, prompiece)
            self.move_list.append(move)
            return move
        else:
            return None

    def undo_move(self):
        if(len(self.move_list) > 0):
            move = self.move_list.pop()
        else:
            return None
        piece = self.board.readfield(move.dstx, move.dsty)
        if(move.prompiece):
            if(self.color_of_piece(piece) == COLORS['white']):
                cpawn = cWhitePawn(self, move.dstx, move.dsty)
            else:
                cpawn = cBlackPawn(self, move.dstx, move.dsty)
            return cpawn.undo_move(move)
        else:
            cpiece = self.obj_for_piece(piece, move.dstx, move.dsty)
            if(cpiece):
                return cpiece.undo_move(move)
            else:
                return None

    def is_king_after_move_attacked(self, srcx, srcy, dstx, dsty):
        piece = self.board.readfield(srcx, srcy)

        pawnenmy = None
        if(piece == PIECES['wPw']):
            cpawn = cWhitePawn(self, srcx, srcy)
            if(cpawn.is_ep_move_ok(dstx, dsty)):
                pawnenmy = self.board.readfield(dstx, srcy)
                self.board.writefield(dstx, srcy, PIECES['blk'])
        elif(piece == PIECES['bPw']):
            cpawn = cBlackPawn(self, srcx, srcy)
            if(cpawn.is_ep_move_ok(dstx, dsty)):
                pawnenmy = self.board.readfield(dstx, srcy)
                self.board.writefield(dstx, srcy, PIECES['blk'])

        self.board.writefield(srcx, srcy, PIECES['blk'])
        dstpiece = self.board.readfield(dstx, dsty)
        self.board.writefield(dstx, dsty, piece)

        if(self.color_of_piece(piece) == COLORS['white']):
            flag = is_field_touched(self, self.board.wKg_x, self.board.wKg_y, COLORS['black'], self.EVAL_MODES['ignore-pins'])
        else:
            flag = is_field_touched(self, self.board.bKg_x, self.board.bKg_y, COLORS['white'], self.EVAL_MODES['ignore-pins'])

        self.board.writefield(dstx, dsty, dstpiece)
        self.board.writefield(srcx, srcy, piece)
        if(pawnenmy):
            self.board.writefield(dstx, srcy, pawnenmy)

        return flag

    def is_move_available(self):
        color = self.next_color()
        for y1 in range(8):
            for x1 in range(8):
                piece = self.board.readfield(x1, y1)
                if(color == self.color_of_piece(piece)):
                    if(piece == PIECES['wPw'] and y1 == self.board.RANKS['7']):
                        prompiece = PIECES['wQu']
                    elif(piece == PIECES['bPw'] and y1 == self.board.RANKS['2']):
                        prompiece = PIECES['bQu']
                    else:
                        prompiece = PIECES['blk']
                    for y2 in range(8):
                        for x2 in range(8):
                            flag = self.is_move_valid(x1, y1, x2, y2, prompiece)[0]
                            if(flag):
                                return True
        return False

    def evaluate_status(self):
        if(self.status == self.STATUS['paused'] or self.status == self.STATUS['setup']):
            return self.status
        if(self.is_move_available()):
            return self.STATUS['open']
        else:
            if(self.next_color() == COLORS['white']):
                if(is_field_touched(self, self.board.wKg_x, self.board.wKg_y, COLORS['black'], self.EVAL_MODES['ignore-pins'])):
                    return self.STATUS['winner_black']
            else:
                if(is_field_touched(self, self.board.bKg_x, self.board.bKg_y, COLORS['white'], self.EVAL_MODES['ignore-pins'])):
                    return self.STATUS['winner_white']
        return self.STATUS['draw']

    def eval_pin_dir(self, srcx, srcy):
        cpieces = [cRook, cBishop]
        white_faces = [PIECES['wRk'], PIECES['wBp']]
        black_faces = [PIECES['bRk'], PIECES['bBp']]

        for idx in range(2):
            piece = self.board.readfield(srcx, srcy)
            color = self.color_of_piece(piece)
            if(color == COLORS['white']):
                kgx = self.board.wKg_x
                kgy = self.board.wKg_y
            else:
                kgx = self.board.bKg_x
                kgy = self.board.bKg_y
            direction = cpieces[idx].dir_for_move(srcx, srcy, kgx, kgy)
            if(direction != DIRS['undefined']):
                stepx, stepy = cpieces[idx].step_for_dir(direction)
                if(stepx is not None):
                    dstx, dsty = self.board.search(srcx, srcy, stepx, stepy)
                    if(dstx is not None):
                        piece = self.board.readfield(dstx, dsty)
                        if( (color == COLORS['white'] and piece == PIECES['wKg']) or
                            (color == COLORS['black'] and piece == PIECES['bKg']) ):
                            reverse_dir = REVERSE_DIRS[direction]
                            stepx, stepy = cpieces[idx].step_for_dir(reverse_dir)
                            if(stepx is not None):
                                dstx, dsty = self.board.search(srcx, srcy, stepx, stepy)
                                if(dstx is not None):
                                    piece = self.board.readfield(dstx, dsty)
                                    if(color == COLORS['white']):
                                        if(piece == PIECES['bQu'] or piece == black_faces[idx]):
                                            return direction
                                        else:
                                            return DIRS['undefined']
                                    else:
                                        if(piece == PIECES['wQu'] or piece == white_faces[idx]):
                                            return direction
                                        else:
                                            return DIRS['undefined']
        return DIRS['undefined']

    def is_pinned(self, x, y):
        piece = self.board.readfield(x, y)
        direction = self.eval_pin_dir(x, y)
        return direction != DIRS['undefined']

    def is_soft_pin(self, srcx, srcy):
        piece = self.board.readfield(srcx, srcy)
        color = self.color_of_piece(piece)
        opp_color = self.oppcolor_of_piece(piece)
        enemies = cSearchForRook.list_field_touches(self, srcx, srcy, opp_color)        
        for enemy in enemies:
            enemy_dir = cRook.dir_for_move(srcx, srcy, enemy.fieldx, enemy.fieldy)
            stepx, stepy = cRook.step_for_dir(REVERSE_DIRS[enemy_dir])
            if(stepx is not None):
                x1, y1 = self.board.search(srcx, srcy, stepx, stepy)
                if(x1 is not None):
                    friend = self.board.readfield(x1, y1)
                    if(self.color_of_piece(friend) == color and 
                       PIECES_RANK[friend] > PIECES_RANK[piece] and 
                       PIECES_RANK[friend] > PIECES_RANK[enemy.piece]):
                        return True, enemy_dir
        enemies.clear()
        enemies = cSearchForBishop.list_field_touches(self, srcx, srcy, opp_color) 
        for enemy in enemies:
            enemy_dir = cBishop.dir_for_move(srcx, srcy, enemy.fieldx, enemy.fieldy)
            stepx, stepy = cBishop.step_for_dir(REVERSE_DIRS[enemy_dir])
            if(stepx is not None):
                x1, y1 = self.board.search(srcx, srcy, stepx, stepy)
                if(x1 is not None):
                    friend = self.board.readfield(x1, y1)
                    if(self.color_of_piece(friend) == color and 
                       PIECES_RANK[friend] > PIECES_RANK[piece] and 
                       PIECES_RANK[friend] > PIECES_RANK[enemy.piece]):
                        return True, enemy_dir
        return False, None

    def is_discovered_attack(self, srcx, srcy):
        piece = self.board.readfield(srcx, srcy)
        color = self.color_of_piece(piece)
        attackers = cSearchForRook.list_field_touches(self, srcx, srcy, color)        
        for attacker in attackers:
            enemy_dir = cRook.dir_for_move(srcx, srcy, attacker.fieldx, attacker.fieldy)
            stepx, stepy = cRook.step_for_dir(REVERSE_DIRS[enemy_dir])
            if(stepx is not None):
                x1, y1 = self.board.search(srcx, srcy, stepx, stepy)
                if(x1 is not None):
                    attacked = self.board.readfield(x1, y1)
                    if(self.color_of_piece(attacked) != color and 
                       PIECES_RANK[attacked] > PIECES_RANK[attacker.piece]):
                        return True
        attackers.clear()
        attackers = cSearchForBishop.list_field_touches(self, srcx, srcy, color) 
        for attacker in attackers:
            enemy_dir = cBishop.dir_for_move(srcx, srcy, attacker.fieldx, attacker.fieldy)
            stepx, stepy = cBishop.step_for_dir(REVERSE_DIRS[enemy_dir])
            if(stepx is not None):
                x1, y1 = self.board.search(srcx, srcy, stepx, stepy)
                if(x1 is not None):
                    attacked = self.board.readfield(x1, y1)
                    if(self.color_of_piece(attacked) != color and 
                       PIECES_RANK[attacked] > PIECES_RANK[attacker.piece]):
                        return True
        return False

    def obj_for_piece(self, piece, xpos, ypos):
        if(piece == PIECES['wPw']):
            return cWhitePawn(self, xpos, ypos)
        if(piece == PIECES['bPw']):
            return cBlackPawn(self, xpos, ypos)
        elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
            return cKnight(self, xpos, ypos)
        elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
            return cBishop(self, xpos, ypos)
        elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
            return cRook(self, xpos, ypos)
        elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
            return cQueen(self, xpos, ypos)
        elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
            return cKing(self, xpos, ypos)
        else:
            return None

# class end
