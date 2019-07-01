
#include <map>
#include <string>

using namespace std;


typedef map<string, int> MapStrInt;
typedef map<int, int> MapIntInt;
typedef map<int, string> MapIntStr;

const MapStrInt PIECES = {
  {'blk', 0x0}, 
  {'wPw' , 0x1}, 
  {'wKn', 0x2}, 
  {'wBp', 0x3}, 
  {'wRk', 0x4}, 
  {'wQu', 0x5}, 
  {'wKg', 0x6}, 
  {'bPw', 0x9}, 
  {'bKn', 0xA}, 
  {'bBp', 0xB}, 
  {'bRk', 0xC}, 
  {'bQu', 0xD}, 
  {'bKg', 0xE}
};

const MapIntInt PIECES_BARE = {
    PIECES['blk']. 0,
    PIECES['wPw'], 1,
    PIECES['bPw'], 1,
    PIECES['wKn'], 2,
    PIECES['bKn'], 2,
    PIECES['wBp'], 3,
    PIECES['bBp'], 3,
    PIECES['wRk'], 4,
    PIECES['bRk'] : 4,
    PIECES['wQu'] : 5,
    PIECES['bQu'] : 5,
    PIECES['wKg'] : 6,
    PIECES['bKg'] : 6 
}

  const MapIntInt PIECES_RANK = {
 = {
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

const MapIntInt PIECES_MASK = {
 = {
    PIECES['blk'] : 0x0,
    PIECES['wPw'] : 0x1111111111111111111111111111111111111111111111111111111111111111,
    PIECES['wKn'] : 0x2222222222222222222222222222222222222222222222222222222222222222,
    PIECES['wBp'] : 0x3333333333333333333333333333333333333333333333333333333333333333,
    PIECES['wRk'] : 0x4444444444444444444444444444444444444444444444444444444444444444,
    PIECES['wQu'] : 0x5555555555555555555555555555555555555555555555555555555555555555,
    PIECES['wKg'] : 0x6666666666666666666666666666666666666666666666666666666666666666,
    PIECES['bPw'] : 0x9999999999999999999999999999999999999999999999999999999999999999,
    PIECES['bKn'] : 0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,
    PIECES['bBp'] : 0xBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB,
    PIECES['bRk'] : 0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC,
    PIECES['bQu'] : 0xDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD,
    PIECES['bKg'] : 0xEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
}

const MapIntInt PIECES_NMASK = {
 = {
    PIECES['blk'] : 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,
    PIECES['wPw'] : 0xEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE,
    PIECES['wKn'] : 0xDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD,
    PIECES['wBp'] : 0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC,
    PIECES['wRk'] : 0xBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB,
    PIECES['wQu'] : 0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,
    PIECES['wKg'] : 0x9999999999999999999999999999999999999999999999999999999999999999,
    PIECES['bPw'] : 0x6666666666666666666666666666666666666666666666666666666666666666,
    PIECES['bKn'] : 0x5555555555555555555555555555555555555555555555555555555555555555,
    PIECES['bBp'] : 0x4444444444444444444444444444444444444444444444444444444444444444,
    PIECES['bRk'] : 0x3333333333333333333333333333333333333333333333333333333333333333,
    PIECES['bQu'] : 0x2222222222222222222222222222222222222222222222222222222222222222,
    PIECES['bKg'] : 0x1111111111111111111111111111111111111111111111111111111111111111 
}

const MapIntStr STR_PIECES = {
 = {
    '0': 'blk',
    '1': 'wPw',
    '2': 'wKn',
    '3': 'wBp',
    '4': 'wRk',
    '5': 'wQu',
    '6': 'wKg',
    '9': 'bPw',
    'A': 'bKn',
    'B': 'bBp',
    'C': 'bRk',
    'D': 'bQu',
    'E': 'bKg'
}

const MapStrInt COLORS = {
 = {
    'undef' : 0,
    'white' : 1,
    'black' : 9 
}

const MapIntInt REVERSED_COLORS = {
 = { 
    COLORS['undef'] : COLORS['undef'],
    COLORS['white'] : COLORS['black'],
    COLORS['black'] : COLORS['white'] 
}

const MapIntInt PIECES_COLOR = {
 = {
    PIECES['blk'] : COLORS['undef'],
    PIECES['wPw'] : COLORS['white'],
    PIECES['wKn'] : COLORS['white'],
    PIECES['wBp'] : COLORS['white'],
    PIECES['wRk'] : COLORS['white'],
    PIECES['wQu'] : COLORS['white'],
    PIECES['wKg'] : COLORS['white'],
    PIECES['bPw'] : COLORS['black'],
    PIECES['bKn'] : COLORS['black'],
    PIECES['bBp'] : COLORS['black'],
    PIECES['bRk'] : COLORS['black'],
    PIECES['bQu'] : COLORS['black'],
    PIECES['bKg'] : COLORS['black']
}

const MapStrInt DIRS = {
 = {
    'nth' : 0,
    'sth' : 1,
    'est' : 2,
    'wst' : 3,
    'nth-est' : 4,
    'sth-wst' : 5,
    'nth-wst' : 6,
    'sth-est' : 7,
    '2nth-est' : 9,
    'nth-2est' : 10,
    'sth-2est' :  11,
    '2sth-est' :  12, 
    '2sth-wst' : 13, 
    'sth-2wst' : 14,
    'nth-2wst' : 15,
    '2nth-wst' : 16,
    'undef' : 17
}

const MapIntInt REVERSE_DIRS = {
 = {
    DIRS['nth'] : DIRS['sth'],
    DIRS['sth'] : DIRS['nth'],
    DIRS['est'] : DIRS['wst'],
    DIRS['wst'] : DIRS['est'],
    DIRS['nth-est'] : DIRS['sth-wst'],
    DIRS['sth-wst'] : DIRS['nth-est'],
    DIRS['nth-wst'] : DIRS['sth-est'],
    DIRS['sth-est'] : DIRS['nth-wst'],
    DIRS['2nth-est'] : DIRS['undef'],
    DIRS['nth-2est'] : DIRS['undef'],
    DIRS['sth-2est'] : DIRS['undef'],
    DIRS['2sth-est'] : DIRS['undef'],
    DIRS['2sth-wst'] : DIRS['undef'],
    DIRS['sth-2wst'] : DIRS['undef'],
    DIRS['nth-2wst'] : DIRS['undef'],
    DIRS['2nth-wst'] : DIRS['undef'],
    DIRS['undef'] : DIRS['undef'] 
}

const MapIntInt DIR_FOR_STEP = {
 = {
     8 : DIRS['nth'],
     16 : DIRS['nth'],
    -8 : DIRS['sth'],
    -16 : DIRS['sth'],
     1 : DIRS['est'],
     2 : DIRS['est'],
    -1 : DIRS['wst'],
    -2 : DIRS['wst'],
     9 : DIRS['nth-est'],
    -9 : DIRS['sth-wst'],
     7 : DIRS['nth-wst'],
    -7 : DIRS['sth-est'],
    17 : DIRS['2nth-est'],
    10 : DIRS['nth-2est'],
    -6 : DIRS['sth-2est'],
   -15 : DIRS['2sth-est'], 
   -17 : DIRS['2sth-wst'], 
   -10 : DIRS['sth-2wst'],
     6 : DIRS['nth-2wst'],
    15 : DIRS['2nth-wst']
}

const MapIntInt SCORES = {
 = { 
    PIECES['blk'] : 0,
    PIECES['wPw'] : -100,
    PIECES['wKn'] : -340,
    PIECES['wBp'] : -340,
    PIECES['wRk'] : -450,
    PIECES['wQu'] : -900,
    PIECES['wKg'] : -20000,
    PIECES['bPw'] : 100,
    PIECES['bKn'] : 340,
    PIECES['bBp'] : 340,
    PIECES['bRk'] : 450,
    PIECES['bQu'] : 900, 
    PIECES['bKg'] : 20000
}

const MapIntInt SUPPORTED_SCORES = {
 = {
    PIECES['blk'] : 0,
    PIECES['wPw'] : 6,
    PIECES['wKn'] : 18,
    PIECES['wBp'] : 18,
    PIECES['wRk'] : 24,
    PIECES['wQu'] : 30,
    PIECES['wKg'] : 0,
    PIECES['bPw'] : -6,
    PIECES['bKn'] : -18,
    PIECES['bBp'] : -18,
    PIECES['bRk'] : -24,
    PIECES['bQu'] : -30,
    PIECES['bKg'] : 0
}

const MapIntInt ATTACKED_SCORES = {
 = {
    PIECES['blk'] : 0,
    PIECES['wPw'] : -6,
    PIECES['wKn'] : -18,
    PIECES['wBp'] : -18,
    PIECES['wRk'] : -24,
    PIECES['wQu'] : -30,
    PIECES['wKg'] : 0,
    PIECES['bPw'] : 6,
    PIECES['bKn'] : 18,
    PIECES['bBp'] : 18,
    PIECES['bRk'] : 24,
    PIECES['bQu'] : 30,
    PIECES['bKg'] : 0
}
