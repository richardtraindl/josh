
from .values import *


class cBoard:
    RANKS = {
        '1' : 0,
        '2' : 1,
        '3' : 2,
        '4' : 3,
        '5' : 4,
        '6' : 5,
        '7' : 6,
        '8' : 7,
    }

    COLS = {
        'A' : 0,
        'B' : 1,
        'C' : 2,
        'D' : 3,
        'E' : 4,
        'F' : 5,
        'G' : 6,
        'H' : 7,
    }

    BASE   = 0x23456432111111110000000000000000000000000000000099999999ABCDECBA
    FULL   = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    SINGLE = 0xF000000000000000000000000000000000000000000000000000000000000000

    def __init__(self):
        self.fields = self.BASE
        self.wKg_x = self.COLS['E']
        self.wKg_y = self.RANKS['1']
        self.bKg_x = self.COLS['E']
        self.bKg_y = self.RANKS['8']
        self.wKg_first_move_on = None
        self.bKg_first_move_on = None
        self.wRkA_first_move_on = None
        self.wRkH_first_move_on = None
        self.bRkA_first_move_on = None
        self.bRkH_first_move_on = None
        self.wQu_cnt = 1
        self.bQu_cnt = 1
        self.wOfficer_cnt = 6
        self.bOfficer_cnt = 6

    def set_to_base(self):
        self.fields = self.BASE
        self.wKg_x = self.COLS['E']
        self.wKg_y = self.RANKS['1']
        self.bKg_x = self.COLS['E']
        self.bKg_y = self.RANKS['8']
        self.wKg_first_move_on = None
        self.bKg_first_move_on = None
        self.wRkA_first_move_on = None
        self.wRkH_first_move_on = None
        self.bRkA_first_move_on = None
        self.bRkH_first_move_on = None
        self.wQu_cnt = 1
        self.bQu_cnt = 1
        self.wOfficer_cnt = 6
        self.bOfficer_cnt = 6

    def clear(self):
        self.fields = 0x0
        self.wKg_x = None
        self.wKg_y = None
        self.bKg_x = None
        self.bKg_y = None
        self.wKg_first_move_on = None
        self.bKg_first_move_on = None
        self.wRkA_first_move_on = None
        self.wRkH_first_move_on = None
        self.bRkA_first_move_on = None
        self.bRkH_first_move_on = None
        self.wQu_cnt = 0
        self.bQu_cnt = 0
        self.wOfficer_cnt = 0
        self.bOfficer_cnt = 0

    def verify(self):
        wKg_cnt = 0
        bKg_cnt = 0
        wPw_cnt = 0
        bPw_cnt = 0
        wOfficer_cnt = 0
        bOfficer_cnt = 0
        for y in range(8):
            for x in range(8):
                piece = self.readfield(x, y)
                if(piece == PIECES['wKg']):
                    wKg_cnt += 1
                elif(piece == PIECES['bKg']):
                    bKg_cnt += 1
                elif(piece == PIECES['wPw']):
                    wPw_cnt += 1
                elif(piece == PIECES['bPw']):
                    bPw_cnt += 1
                elif(piece == PIECES['wRk'] or piece == PIECES['wBp'] or 
                     piece == PIECES['wKn'] or piece == PIECES['wQu']):
                    wOfficer_cnt += 1
                elif(piece == PIECES['bRk'] or piece == PIECES['bBp'] or 
                     piece == PIECES['bKn'] or piece == PIECES['bQu']):
                    bOfficer_cnt += 1
                elif(piece == PIECES['blk']):
                    continue
                else:
                    return False
        if(wKg_cnt != 1 or bKg_cnt != 1):
            return False
        if(wPw_cnt > 8 or bPw_cnt > 8):
            return False
        if(wPw_cnt + wOfficer_cnt > 15):
            return False
        if(bPw_cnt + bOfficer_cnt > 15):
            return False
        if(self.wKg_x is None or self.wKg_y is None or self.bKg_x is None or self.bKg_y is None):
            return False
        if(self.readfield(self.wKg_x, self.wKg_y) != PIECES['wKg']):
            return False
        if(self.readfield(self.bKg_x, self.bKg_y) != PIECES['bKg']):
            return False
        if(abs(self.wKg_y - self.bKg_y) < 2 and abs(self.wKg_x - self.bKg_x) < 2):
            return False
        return True

    def decr_officer_counter(self, dstpiece):
        self.update_officer_counter(dstpiece, -1)

    def incr_officer_counter(self, move):
        self.update_officer_counter(move.captpiece, 1)

    def update_officer_counter(self, piece, value):
        if(piece == PIECES['wQu']):
            self.wQu_cnt += value
        elif(piece == PIECES['bQu']):
            self.bQu_cnt += value
        elif(piece == PIECES['wKn'] or piece == PIECES['wBp'] or piece == PIECES['wRk']):
            self.wOfficer_cnt += value
        elif(piece == PIECES['bKn'] or piece == PIECES['bBp'] or piece == PIECES['bRk']):
            self.bOfficer_cnt += value

    def writefield(self, x, y, value):
        idx = y * 8 + x
        tmpfields = self.SINGLE >> idx * 4
        tmpfields = tmpfields ^ self.FULL
        tmpfields = tmpfields & self.fields
        self.fields = tmpfields | value << (63 - idx) * 4

    def setfield(self, idx, value):
        tmpfields = self.SINGLE >> idx * 4
        tmpfields = tmpfields ^ self.FULL
        tmpfields = tmpfields & self.fields
        self.fields = tmpfields | value << (63 - idx) * 4

    def readfield(self, x, y):
        idx = y * 8 + x
        value = self.fields >> ((63 - idx) * 4)
        return value & 0xF

    def getfield(self, idx):
        value = self.fields >> ((63 - idx) * 4)
        return value & 0xF

    def search(self, srcx, srcy, stepx, stepy, maxcnt=7):
        cnt = 0
        x = srcx + stepx
        y = srcy + stepy
        while(x >= self.COLS['A'] and x <= self.COLS['H'] and 
              y >= self.RANKS['1'] and y <= self.RANKS['8'] and 
              cnt < maxcnt):
            piece = self.readfield(x, y)
            if(piece != PIECES['blk']):
                return x, y
            cnt += 1
            x += stepx
            y += stepy
        return None, None

    def search_bi_dirs(self, srcx, srcy, stepx, stepy, maxcnt=7):
        cnt = 0
        first_x = None
        first_y = None
        steps = [[stepx, stepy], [stepx * -1, stepy * -1]]
        for step in steps:
            x = srcx + step[0]
            y = srcy + step[1]
            while(x >= self.COLS['A'] and x <= self.COLS['H'] and 
                  y >= self.RANKS['1'] and y <= self.RANKS['8'] and 
                  cnt < maxcnt):
                piece = self.readfield(x, y)
                if(piece != PIECES['blk']):
                    if(first_x is None):
                        first_x = x
                        first_y = y
                        break
                    else:
                        return first_x, first_y, x, y
                cnt += 1
                x += stepx
                y += stepy
            if(first_x is None):
                break
        return None, None, None, None

    def step(self, srcx, srcy, stepx, stepy):
        x = srcx + stepx
        y = srcy + stepy
        if(x >= self.COLS['A'] and x <= self.COLS['H'] and 
           y >= self.RANKS['1'] and y <= self.RANKS['8']):
            return x, y, self.readfield(x, y)
        else:
            return None, None, None

    @classmethod
    def is_inbounds(cls, x, y):
        if(x < cls.COLS['A'] or x > cls.COLS['H'] or 
           y < cls.RANKS['1'] or y > cls.RANKS['8']):
            return False
        else:
            return True

    @classmethod
    def is_move_inbounds(cls, srcx, srcy, dstx, dsty):
        if(srcx < cls.COLS['A'] or srcx > cls.COLS['H'] or 
           srcy < cls.RANKS['1'] or srcy > cls.RANKS['8'] or
           dstx < cls.COLS['A'] or dstx > cls.COLS['H'] or 
           dsty < cls.RANKS['1'] or dsty > cls.RANKS['8']):
            return False
        else:
            return True

# class end
