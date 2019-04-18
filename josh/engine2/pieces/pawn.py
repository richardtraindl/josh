from .. values import *
from .piece import *


class cPawn(cPiece):
    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    def is_trapped(self):
        return False # pawn cannot be trapped

################
    def do_move(self, dstx, dsty, prompiece=PIECES['blk']):
        board = self.match.board
        dstpiece = board.readfield(dstx, dsty)
        move = super().do_move(dstx, dsty, prompiece)

        if(prompiece):
            board.writefield(dstx, dsty, prompiece)
            self.match.score -= (SCORES[prompiece] - SCORES[self.piece])
        elif(dstpiece == PIECES['blk'] and self.xpos != dstx):
            move.enpassx = self.xpos
            move.enpassy = dsty
            move.captpiece = board.readfield(move.enpassx, move.enpassy)
            board.writefield(move.enpassx, move.enpassy, PIECES['blk'])
            self.match.score += SCORES[move.captpiece]

        return move
################

################
    def undo_move(self, move):
        board = self.match.board
        super().undo_move(move)

        if(move.prompiece):
            if(self.color == COLORS['white']):
                origin = PIECES['wPw']
            else:
                origin = PIECES['bPw']
            board.writefield(move.srcx, move.srcy, origin)
            board.writefield(move.dstx, move.dsty, move.captpiece)
            self.match.score += (SCORES[move.prompiece] - SCORES[origin])
        elif(move.enpassx and move.enpassy):
            board.writefield(move.dstx, move.dsty, PIECES['blk'])
            board.writefield(move.enpassx, move.enpassy, move.captpiece)

        return move
################

    def move_controles_file(self, dstx, dsty):
        return False

    def is_running(self):
        if(self.color == COLORS['white']):
            stepx = 0
            stepy = 1
            opp_pawn = PIECES['bPw']
        else:
            stepx = 0
            stepy = -1
            opp_pawn = PIECES['wPw']
        for i in range(-1, 2, 1):
            x1 = self.xpos + i
            y1 = self.ypos
            while(True):
                x1, y1 = self.match.board.search(x1, y1, stepx, stepy)
                if(x1 is not None):
                    piece = self.match.board.readfield(x1, y1)
                    if(piece == opp_pawn):
                        return False
                else:
                    break
        return True

    def is_weak(self):
        friends, enemies = list_all_field_touches(self.match, self.xpos, self.ypos, self.color)
        if(len(friends) >= len(enemies)):
            return False
        if(self.color == COLORS['white']):
            stepy = -1
        else:
            stepy = 1
        for i in range(2):
            if(i == 0):
                newx = self.xpos + 1
            else:
                newx = self.xpos - 1
            if(self.match.is_inbounds(newx, self.ypos)):
                x1, y1 = self.match.board.search(newx, self.ypos, newx, stepy)
                if(x1 is not None):
                    piece = self.match.board.readfield(x1, y1)
                    if((piece == PIECES['wPw'] or piece == PIECES['bPw']) and
                       self.color == self.match.color_of_piece(piece)):
                        return False
        return True

# class end

