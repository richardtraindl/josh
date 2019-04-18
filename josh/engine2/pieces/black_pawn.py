from .. values import *
from .. board import cBoard
from .pawn import cPawn


class cBlackPawn(cPawn):
    STEPS = [ [1, -1], [-1, -1] ]
    MAXCNT = 1

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)
        if(self.ypos > 1):
            self.GEN_STEPS = [ [[0, -1, PIECES['blk']]], [[0, -2, PIECES['blk']]], [[-1, -1, PIECES['blk']]], [[1, -1, PIECES['blk']]] ]
        else:
            self.GEN_STEPS = [ [[0, -1, PIECES['bQu']],  [0, -1, PIECES['bRk']],  [0, -1, PIECES['bBp']],  [0, -1, PIECES['bKn']]],
                               [[1, -1, PIECES['bQu']],  [1, -1, PIECES['bRk']],  [1, -1, PIECES['bBp']],  [1, -1, PIECES['bKn']]],
                               [[-1, -1, PIECES['bQu']], [-1, -1, PIECES['bRk']], [-1, -1, PIECES['bBp']], [-1, -1, PIECES['bKn']]] ]

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == 0 and step_y == -1):
            return DIRS['south']
        elif(step_x == 0 and step_y == -2 and 
             srcy == cBoard.RANKS['7']):
            return DIRS['2south']
        elif(step_x == 1 and step_y == -1):
            return DIRS['south-east']
        elif(step_x == -1 and step_y == -1):
            return DIRS['south-west']
        else:
            return DIRS['undefined']

    def is_move_valid(self, dstx, dsty, prompiece):
        move_dir = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(move_dir == DIRS['undefined']):
            return False
        pin_dir = self.match.eval_pin_dir(self.xpos, self.ypos)
        dstpiece = self.match.board.readfield(dstx, dsty)
        # check pins
        if(move_dir == DIRS['south'] or move_dir == DIRS['2south']):
            if(pin_dir != DIRS['north'] and pin_dir != DIRS['south'] and pin_dir != DIRS['undefined']):
                return False
        elif(move_dir == DIRS['south-east']):
            if(pin_dir != DIRS['north-west'] and pin_dir != DIRS['south-east'] and pin_dir != DIRS['undefined']):
                return False
        elif(move_dir == DIRS['south-west']):
            if(pin_dir != DIRS['north-east'] and pin_dir != DIRS['south-west'] and pin_dir != DIRS['undefined']):
                return False
        else:
            return False
        # check fields
        if(move_dir == DIRS['south'] and dstpiece != PIECES['blk']):
            return False
        elif(move_dir == DIRS['2south']):
            midpiece = self.match.board.readfield(dstx, self.ypos + -1)
            if(midpiece != PIECES['blk'] or dstpiece != PIECES['blk']):
                return False
        elif(move_dir == DIRS['south-east'] or move_dir == DIRS['south-west']):
            if(self.match.color_of_piece(dstpiece) != COLORS['white']):
                return self.is_ep_move_ok(dstx, dsty)
        # check promotion
        if(dsty == 0 and prompiece != PIECES['bQu'] and 
           prompiece != PIECES['bRk'] and 
           prompiece != PIECES['bBp'] and 
           prompiece != PIECES['bKn']):
            return False
        elif(dsty > 0 and prompiece != PIECES['blk']):
            return False
        return True

    def is_ep_move_ok(self, dstx, dsty):
        if(len(self.match.move_list) == 0):
            return False
        else:
            lastmove = self.match.move_list[-1]
        dstpiece = self.match.board.readfield(dstx, dsty)
        enemy = self.match.board.readfield(lastmove.dstx, lastmove.dsty)
        if(dstpiece == PIECES['blk'] and enemy == PIECES['wPw']):
            if(lastmove.srcy - lastmove.dsty == -2 and 
               lastmove.dsty == self.ypos and 
               lastmove.dstx == dstx and 
               lastmove.dsty - dsty == 1):
                return True
        return False

# class end

