
from .. values import *
from .. board import cBoard
from .piece import cPiece
from .pawn import cPawn

class cWhitePawn(cPawn):
    STEPS = [9, 7]
    MAXCNT = 1

    def __init__(self, match, pos):
        super().__init__(match, pos)
        if((self.pos // 8) < 6):
            self.GEN_STEPS = [ [[8, PIECES['blk']]], [[16, PIECES['blk']]], [[9, PIECES['blk']]], [[7, PIECES['blk']]] ]
        else:
            self.GEN_STEPS = [ [[8, PIECES['wQu']], [8, PIECES['wRk']], [8, PIECES['wBp']], [8, PIECES['wKn']]],
                               [[9, PIECES['wQu']], [9, PIECES['wRk']], [9, PIECES['wBp']], [9, PIECES['wKn']]],
                               [[7, PIECES['wQu']], [7, PIECES['wRk']], [7, PIECES['wBp']], [7, PIECES['wKn']]] ]

    @classmethod
    def dir_for_move(cls, src, dst):
        if(src == dst):
            return DIRS['undef']
        if(cBoard.is_inbounds_core(src, dst) == False):
            return DIRS['undef']
        if(src + 8 == dst or src + 16 == dst):
            return DIRS['nth']
        elif(src + 9 == dst and src % 8 < dst % 8):
            return DIRS['nth-est']
        elif(src + 7 == dst and src % 8 > dst % 8):
            return DIRS['nth-wst']
        else:
            return DIRS['undef']

    @classmethod
    def step_for_dir(cls, direction):
        if(direction == DIRS['nth']):
            return 8
        elif(direction == DIRS['nth-est']):
            return 9
        elif(direction == DIRS['nth-wst']):
            return 7
        else:
            return None

    def is_move_valid(self, dst, prompiece):
        flag = False
        STEPS = []
        STEPS.extend(self.STEPS)
        STEPS.extend([8, 16])
        for step in STEPS:
            if((self.pos + step) == dst and 
                self.match.board.is_inbounds(self.pos, dst, step)):
                flag = True
                break
        if(flag == False):
            return False
        move_dir = self.dir_for_move(self.pos, dst)
        if(move_dir == DIRS['undef']):
            return False
        pin_dir = self.match.eval_pin_dir(self.pos)
        dstpiece = self.match.board.getfield(dst)
        # check pins
        if(move_dir == DIRS['nth']):
            if(pin_dir != DIRS['nth'] and pin_dir != DIRS['sth'] and pin_dir != DIRS['undef']):
                return False
        elif(move_dir == DIRS['nth-wst']):
            if(pin_dir != DIRS['nth-wst'] and pin_dir != DIRS['sth-est'] and pin_dir != DIRS['undef']):
                return False
        elif(move_dir == DIRS['nth-est']):
            if(pin_dir != DIRS['nth-est'] and pin_dir != DIRS['sth-wst'] and pin_dir != DIRS['undef']):
                return False
        else:
            return False
        # check fields
        if(move_dir == DIRS['nth']):
            if(dstpiece != PIECES['blk']):
                return False
            if(self.pos - dst == -16):
                midpiece = self.match.board.getfield(self.pos + 8)
                if(midpiece != PIECES['blk']):
                    return False
        elif(move_dir == DIRS['nth-est'] or move_dir == DIRS['nth-wst']):
            if(self.match.color_of_piece(dstpiece) != COLORS['black']):
                return self.is_ep_move_ok(dst)
        # check promotion
        if((dst // 8) == 7 and prompiece != PIECES['wQu'] and 
           prompiece != PIECES['wRk'] and 
           prompiece != PIECES['wBp'] and 
           prompiece != PIECES['wKn']):
            return False
        elif((dst // 8) < 7 and prompiece != PIECES['blk']):
            return False
        return True

    def is_ep_move_ok(self, dst):
        if(len(self.match.minutes) == 0):
            return False
        else:
            lastmove = self.match.minutes[-1]
        dstpiece = self.match.board.getfield(dst)
        enemy = self.match.board.getfield(lastmove.dst)
        if(dstpiece == PIECES['blk'] and enemy == PIECES['bPw']):
            if((lastmove.src // 8) - (lastmove.dst // 8) == 2 and 
               (lastmove.dst // 8) == (self.pos // 8) and 
               (lastmove.dst % 8) == (dst % 8) and 
               (lastmove.dst // 8) - (dst // 8) == -1):
                return True
        return False
           
# class end

