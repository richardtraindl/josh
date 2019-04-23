
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

    def __init__(self):
        self.fields = [ [PIECES['wRk'], PIECES['wKn'], PIECES['wBp'], PIECES['wQu'], PIECES['wKg'], PIECES['wBp'], PIECES['wKn'], PIECES['wRk']],
                        [PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw']],
                        [PIECES['bRk'], PIECES['bKn'], PIECES['bBp'], PIECES['bQu'], PIECES['bKg'], PIECES['bBp'], PIECES['bKn'], PIECES['bRk']] ]
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
        self.writefield(self.COLS['A'], self.RANKS['1'], PIECES['wRk'])
        self.writefield(self.COLS['B'], self.RANKS['1'], PIECES['wKn'])
        self.writefield(self.COLS['C'], self.RANKS['1'], PIECES['wBp'])
        self.writefield(self.COLS['D'], self.RANKS['1'], PIECES['wQu'])
        self.writefield(self.COLS['E'], self.RANKS['1'], PIECES['wKg'])
        self.writefield(self.COLS['F'], self.RANKS['1'], PIECES['wBp'])
        self.writefield(self.COLS['G'], self.RANKS['1'], PIECES['wKn'])
        self.writefield(self.COLS['H'], self.RANKS['1'], PIECES['wRk'])
        for y in range(1, 2, 1):
            for x in range(8):
                self.writefield(x, y, PIECES['wPw'])
        for y in range(2, 6, 1):
            for x in range(8):
                self.writefield(x, y, PIECES['blk'])
        for y in range(6, 7, 1):
            for x in range(8):
                self.writefield(x, y, PIECES['bPw'])
        self.writefield(self.COLS['A'], self.RANKS['8'], PIECES['bRk'])
        self.writefield(self.COLS['B'], self.RANKS['8'], PIECES['bKn'])
        self.writefield(self.COLS['C'], self.RANKS['8'], PIECES['bBp'])
        self.writefield(self.COLS['D'], self.RANKS['8'], PIECES['bQu'])
        self.writefield(self.COLS['E'], self.RANKS['8'], PIECES['bKg'])
        self.writefield(self.COLS['F'], self.RANKS['8'], PIECES['bBp'])
        self.writefield(self.COLS['G'], self.RANKS['8'], PIECES['bKn'])
        self.writefield(self.COLS['H'], self.RANKS['8'], PIECES['bRk'])
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
        for y in range(8):
            for x in range(8):
                self.writefield(x, y, PIECES['blk'])
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
        self.fields[y][x] = value

    def readfield(self, x, y):
        return self.fields[y][x]

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
