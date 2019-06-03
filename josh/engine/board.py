
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
        self.wKg = self.COLS['E'] + self.RANKS['1'] * 8
        self.bKg = self.COLS['E'] + self.RANKS['8'] * 8
        self.wKg_first_move_on = None
        self.bKg_first_move_on = None
        self.wRkA_first_move_on = None
        self.wRkH_first_move_on = None
        self.bRkA_first_move_on = None
        self.bRkH_first_move_on = None

    def set_to_base(self):
        self.fields = self.BASE
        self.wKg = self.COLS['E'] + self.RANKS['1'] * 8
        self.bKg = self.COLS['E'] + self.RANKS['8'] * 8
        self.wKg_first_move_on = None
        self.bKg_first_move_on = None
        self.wRkA_first_move_on = None
        self.wRkH_first_move_on = None
        self.bRkA_first_move_on = None
        self.bRkH_first_move_on = None

    def clear(self):
        self.fields = 0x0
        self.wKg = None
        self.bKg = None
        self.wKg_first_move_on = None
        self.bKg_first_move_on = None
        self.wRkA_first_move_on = None
        self.wRkH_first_move_on = None
        self.bRkA_first_move_on = None
        self.bRkH_first_move_on = None

    def verify(self):
        wKg_cnt = 0
        bKg_cnt = 0
        wPw_cnt = 0
        bPw_cnt = 0
        wOfficer_cnt = 0
        bOfficer_cnt = 0
        for idx in range(64):
            piece = self.getfield(idx)
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
        if(self.wKg is None or self.bKg is None):
            return False
        if(abs(self.wKg // 8 - self.bKg // 8) < 2 and abs(self.wKg % 8 - self.bKg % 8) < 2):
            return False
        return True

    def setfield(self, idx, value):
        tmpfields = self.SINGLE >> (idx * 4)
        tmpfields = tmpfields ^ self.FULL
        tmpfields = tmpfields & self.fields
        self.fields = tmpfields | (value << ((63 - idx) * 4))

    def getfield(self, idx):
        return (self.fields >> ((63 - idx) * 4)) & 0xF

    def search(self, src, step, maxcnt=7):
        cnt = 0
        dst = src + step
        while(self.is_inbounds(src, dst, step) and cnt < maxcnt):
            piece = self.getfield(dst)
            if(piece != PIECES['blk']):
                return dst
            cnt += 1
            dst += step
        return None

    def search_bi_dirs(self, src, step, maxcnt=7):
        cnt = 0
        first = None
        steps = [step, (step * -1)]
        for step in steps:
            dst = src + step
            while(self.is_inbounds(src, dst, step) and cnt < maxcnt):
                piece = self.getfield(dst)
                if(piece != PIECES['blk']):
                    if(first is None):
                        first = dst
                        break
                    else:
                        return first, dst
                cnt += 1
                dst += step
            if(first is None):
                break
        return None, None

    @classmethod
    def is_inbounds_core(cls, src, dst):
        if(src < 0 or src > 63 or dst < 0 or dst > 63):
            return False
        else:
            return True

    @classmethod
    def is_nth(cls, src, dst):
        if(src < dst and abs(src - dst) % 8 == 0):
            return True
        else:
            return False

    @classmethod
    def is_sth(cls, src, dst):
        if(src > dst and abs(src - dst) % 8 == 0):
            return True
        else:
            return False

    @classmethod
    def is_est(cls, src, dst):
        if(src % 8 < dst % 8 and src // 8 == dst // 8):
            return True
        else:
            return False

    @classmethod
    def is_wst(cls, src, dst):
        if(src % 8 > dst % 8 and src // 8 == dst // 8):
            return True
        else:
            return False

    @classmethod
    def is_nth_est(cls, src, dst):
        if(abs(src - dst) % 9 == 0 and src < dst and src % 8 < dst % 8):
            return True
        else:
            return False

    @classmethod
    def is_sth_wst(cls, src, dst):
        if(abs(src - dst) % 9 == 0 and src > dst and src % 8 > dst % 8):
            return True
        else:
            return False

    @classmethod
    def is_nth_wst(cls, src, dst):
        if(abs(src - dst) % 7 == 0 and src < dst and src % 8 > dst % 8):
            return True
        else:
            return False

    @classmethod
    def is_sth_est(cls, src, dst):
        if(abs(src - dst) % 7 == 0 and src > dst and src % 8 < dst % 8):
            return True
        else:
            return False

    @classmethod
    def is_inbounds(cls, src, dst, step):
        if(src < 0 or src > 63 or dst < 0 or dst > 63):
            return False
        if(step is None):
            return True
        direction = DIR_FOR_STEP[step]
        if(direction is None):
            return False
        if(direction == DIRS['nth'] or direction == DIRS['sth']):
            return True
        if(direction == DIRS['est'] or direction == DIRS['nth-est'] or direction == DIRS['sth-est']):
            return (src % 8) < (dst % 8)
        if(direction == DIRS['wst'] or direction == DIRS['sth-wst'] or direction == DIRS['nth-wst']):
            return (src % 8) > (dst % 8)
        if(direction == DIRS['2nth-est'] or direction == DIRS['nth-2est'] or 
           direction == DIRS['sth-2est'] or direction == DIRS['2sth-est']):
            return (src % 8) < (dst % 8)
        if(direction == DIRS['2sth-wst'] or direction == DIRS['sth-2wst'] or 
           direction == DIRS['nth-2wst'] or direction == DIRS['2nth-wst']):
            return (src % 8) > (dst % 8)
        return False
# class end

