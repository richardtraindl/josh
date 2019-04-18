from .values import *


class cGenerator:
    def __init__(self, match):
        self.match = match

    def generate_priomoves(self):
        color = self.match.next_color()
        moves = []
        for y in range(0, 8, 1):
            for x in range(0, 8, 1):
                piece = self.match.board.readfield(x, y)
                if(piece == PIECES['blk'] or color != self.match.color_of_piece(piece)):
                    continue
                else:
                    cpiece = self.match.obj_for_piece(piece, x, y)
                    piecemoves = cpiece.generate_priomoves()
                    if(len(piecemoves) > 0):
                        moves.extend(piecemoves)
        return moves

# class end


