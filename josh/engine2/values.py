

PIECES = {
    'blk' : 0,
    'wKg' : 1,
    'wPw' : 2,
    'wRk' : 3,
    'wKn' : 4,
    'wBp' : 5,
    'wQu' : 6,
    'bKg' : 9,
    'bPw' : 10,
    'bRk' : 11,
    'bKn' : 12,
    'bBp' : 13,
    'bQu' : 14 
}


COLORS = {
    'undefined' : 0,
    'white' : 1,
    'black' : 9 
}


REVERSED_COLORS = { 
    COLORS['undefined'] : COLORS['undefined'],
    COLORS['white'] : COLORS['black'],
    COLORS['black'] : COLORS['white'] 
}


PIECES_COLOR = {
    PIECES['blk'] : COLORS['undefined'],
    PIECES['wKg'] : COLORS['white'],
    PIECES['wPw'] : COLORS['white'],
    PIECES['wRk'] : COLORS['white'],
    PIECES['wKn'] : COLORS['white'],
    PIECES['wBp'] : COLORS['white'],
    PIECES['wQu'] : COLORS['white'],
    PIECES['bKg'] : COLORS['black'],
    PIECES['bPw'] : COLORS['black'],
    PIECES['bRk'] : COLORS['black'],
    PIECES['bKn'] : COLORS['black'],
    PIECES['bBp'] : COLORS['black'],
    PIECES['bQu'] : COLORS['black'] 
}

PIECES_TEXT = {
    PIECES['blk'] : u"\u0020",
    PIECES['wKg'] : u"\u2654",
    PIECES['wQu'] : u"\u2655",
    PIECES['wRk'] : u"\u2656",
    PIECES['wBp'] : u"\u2657",
    PIECES['wKn'] : u"\u2658",
    PIECES['wPw'] : u"\u2659",
    PIECES['bKg'] : u"\u265A",
    PIECES['bQu'] : u"\u265B",
    PIECES['bRk'] : u"\u265C",
    PIECES['bBp'] : u"\u265D",
    PIECES['bKn'] : u"\u265E",
    PIECES['bPw'] : u"\u265F" }


PIECES_RANK = {
    PIECES['blk'] : 0,
    PIECES['wPw'] : 1,
    PIECES['bPw'] : 1,
    PIECES['wKn'] : 3,
    PIECES['bKn'] : 3,
    PIECES['wBp'] : 3,
    PIECES['bBp'] : 3,
    PIECES['wRk'] : 5,
    PIECES['bRk'] : 5,
    PIECES['wQu'] : 9,
    PIECES['bQu'] : 9,
    PIECES['wKg'] : 20,
    PIECES['bKg'] : 20 
}


SCORES = { 
    PIECES['blk'] : 0,
    PIECES['wKg'] : -20000,
    PIECES['wPw'] : -100,
    PIECES['wRk'] : -450,
    PIECES['wKn'] : -340,
    PIECES['wBp'] : -340,
    PIECES['wQu'] : -900,
    PIECES['bKg'] : 20000,
    PIECES['bPw'] : 100,
    PIECES['bRk'] : 450,
    PIECES['bKn'] : 340,
    PIECES['bBp'] : 340,
    PIECES['bQu'] : 900 
}


SUPPORTED_SCORES = {
    PIECES['blk'] : 0,
    PIECES['wKg'] : 0,
    PIECES['wPw'] : 6,
    PIECES['wRk'] : 24,
    PIECES['wKn'] : 18,
    PIECES['wBp'] : 18,
    PIECES['wQu'] : 30,
    PIECES['bKg'] : 0,
    PIECES['bPw'] : -6,
    PIECES['bRk'] : -24,
    PIECES['bKn'] : -18,
    PIECES['bBp'] : -18,
    PIECES['bQu'] : -30 
}


ATTACKED_SCORES = {
    PIECES['blk'] : 0,
    PIECES['wKg'] : 0,
    PIECES['wPw'] : -6,
    PIECES['wRk'] : -24,
    PIECES['wKn'] : -18,
    PIECES['wBp'] : -18,
    PIECES['wQu'] : -30,
    PIECES['bKg'] : 0,
    PIECES['bPw'] : 6,
    PIECES['bRk'] : 24,
    PIECES['bKn'] : 18,
    PIECES['bBp'] : 18,
    PIECES['bQu'] : 30
}

DIRS = {
    'north' : 1,
    'south' : 2,
    'east' : 3,
    'west' : 4,
    'north-east' : 5,
    'south-west' : 6,
    'north-west' : 7,
    'south-east' : 8,
    '2north' : 9,
    '2south' : 10,
    'sh-castling' : 11,
    'lg-castling' : 12,
    'valid' : 13,
    'undefined' : 14 
}

REVERSE_DIRS = {
    DIRS['north'] : DIRS['south'],
    DIRS['south'] : DIRS['north'],
    DIRS['east'] : DIRS['west'],
    DIRS['west'] : DIRS['east'],
    DIRS['north-east'] : DIRS['south-west'],
    DIRS['south-west'] : DIRS['north-east'],
    DIRS['north-west'] : DIRS['south-east'],
    DIRS['south-east'] : DIRS['north-west'],
    DIRS['2north'] : DIRS['2south'],
    DIRS['2south'] : DIRS['2north'],
    DIRS['sh-castling'] : DIRS['undefined'],
    DIRS['lg-castling'] : DIRS['undefined'],
    DIRS['valid'] : DIRS['valid'],
    DIRS['undefined'] : DIRS['undefined'] 
}

