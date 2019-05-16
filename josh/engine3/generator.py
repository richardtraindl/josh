from .values import *


class cGenerator:
    def __init__(self, match):
        self.match = match

    def generate_priomoves(self):
        color = self.match.next_color()
        moves = []
        for idx in range(64):
            piece = self.match.board.getfield(idx)
            if(piece == PIECES['blk'] or color != self.match.color_of_piece(piece)):
                continue
            else:
                x = idx % 8
                y = idx // 8
                cpiece = self.match.obj_for_piece(piece, x, y)
                piecemoves = cpiece.generate_priomoves()
                if(len(piecemoves) > 0):
                    moves.extend(piecemoves)
        return moves

# class end


