
import copy
from ..values import *
from ..move import *
from ..pieces.searchforpiece import cSearchForRook, cSearchForBishop, list_field_touches, list_all_field_touches, list_field_touches_beyond


def lowest_piece(touches):
    if(len(touches) == 0):
        return None
    else:
        lowest = PIECES['wKg']
        for touch in touches:
            if(PIECES_RANK[touch.piece] < PIECES_RANK[lowest]):
                lowest = touch.piece
        return lowest


def find_touches_on_dstfield_after_move(match, piece, move):
    match.do_move(move.src, move.dst, move.prompiece)
    frdlytouches, enmytouches = list_all_field_touches(match, move.dst, match.color_of_piece(piece))
    match.undo_move()
    return frdlytouches, enmytouches


def is_supporter_lower_attacker(match, piece, move, supported):
    for attacker in supported.attacker_beyond:
        if(PIECES_RANK[piece] >= PIECES_RANK[attacker.piece]):
            return False
    return True


def check_mates_deep_search(match, move):
    newmatch = copy.deepcopy(match)
    newmatch.do_move(move.src, move.dst, move.prompiece)
    return calc_checks(newmatch, 3, 1)


def calc_checks(match, maxcnt, count):
    from .calc import generate_moves
    moves = generate_moves(match, None, None, False, False)
    if(len(moves) == 0 and count % 2 == 1):
        return True
    if(count >= maxcnt):
        return False
    for move in moves:
        match.do_move(move.src, move.dst, move.prompiece)
        if(calc_checks(match, maxcnt, count + 1)):
            return True
        else:
            match.undo_move()
    return False


def is_soft_pinned_move(match, piece, move):
    flag, pindir = match.is_soft_pin(move.src)
    cpiece = match.obj_for_piece(piece, move.src)
    mvdir = cpiece.dir_for_move(move.src, move.dst)
    return (flag and pindir != mvdir and pindir != REVERSE_DIRS[mvdir])


def is_supply(match, piece, move):
    supplies = cSearchForRook.list_field_touches(match, move.src, match.color_of_piece(piece))
    supplies.extend(cSearchForBishop.list_field_touches(match, move.src, match.color_of_piece(piece)))
    for supply in supplies:
        if(PIECES_BARE[supply.piece] == PIECES_BARE[PIECES['wQu']]):
            return True
        elif(PIECES_BARE[supply.piece] == PIECES_BARE[PIECES['wRk']]):
            return True
        elif(PIECES_BARE[supply.piece] == PIECES_BARE[PIECES['wBp']]):
            return True
    return False


def is_touched_field_within_move(match, piece, move, touched_field):
    cpiece = match.obj_for_piece(piece, move.src)
    mvdir1 = cpiece.dir_for_move(move.src, move.dst)
    mvdir2 = cpiece.dir_for_move(move.dst, touched_field)
    return (mvdir1 != DIRS['undef'] and (mvdir1 == mvdir2 or REVERSE_DIRS[mvdir1] == mvdir2))


def weight_for_standard(match, piece, move):
    friends_on_dstfield, enmies_on_dstfield = find_touches_on_dstfield_after_move(match, piece, move)
    lowest_enemy_on_dstfield = lowest_piece(enmies_on_dstfield)
    ###
    if(is_soft_pinned_move(match, piece, move)):
        return cTactic.WEIGHTS['bad-deal']
    elif(len(enmies_on_dstfield) == 0):
        return cTactic.WEIGHTS['good-deal']
    elif((lowest_enemy_on_dstfield is None or PIECES_RANK[piece] <= PIECES_RANK[lowest_enemy_on_dstfield]) and
         len(friends_on_dstfield) >= len(enmies_on_dstfield)):
        return cTactic.WEIGHTS['good-deal']
    else:
        return cTactic.WEIGHTS['bad-deal']


def weight_for_capture(match, piece, move, weight):
    dstpiece = match.board.getfield(move.dst)
    friends_on_dstfield, enmies_on_dstfield = find_touches_on_dstfield_after_move(match, piece, move)
    ###
    if(PIECES_RANK[piece] < PIECES_RANK[dstpiece]):
        return cTactic.WEIGHTS['stormy']
    elif(is_soft_pinned_move(match, piece, move) == False and len(enmies_on_dstfield) == 0):
        return cTactic.WEIGHTS['stormy']
    elif(is_soft_pinned_move(match, piece, move) == False and 
         match.is_soft_pin((move.dst))[0] and is_supply(match, piece, move)):
        return cTactic.WEIGHTS['stormy']
    elif(is_soft_pinned_move(match, piece, move) == False and 
         PIECES_RANK[piece] == PIECES_RANK[dstpiece]):
        if(len(friends_on_dstfield) > len(enmies_on_dstfield)):
            return cTactic.WEIGHTS['better-deal']
        else:
            return cTactic.WEIGHTS['good-deal']
    else:
        return weight


def weight_for_flee(match, piece, move, weight):
    friends_on_srcfield, enmies_on_srcfield = list_all_field_touches(match, move.src, match.color_of_piece(piece))
    lowest_enemy_on_srcfield = lowest_piece(enmies_on_srcfield)
    ###
    if(weight == cTactic.WEIGHTS['good-deal'] or 
       weight == cTactic.WEIGHTS['better-deal']):
        if(lowest_enemy_on_srcfield is not None and 
           PIECES_RANK[piece] > PIECES_RANK[lowest_enemy_on_srcfield]):
            return cTactic.WEIGHTS['stormy']
        elif(len(friends_on_srcfield) == 0 and len(enmies_on_srcfield) > 0):
            return cTactic.WEIGHTS['stormy']
    return weight


def weight_for_running_pawn(match, piece, move, weight):
    friends_on_dstfield, enmies_on_dstfield = find_touches_on_dstfield_after_move(match, piece, move)
    ###
    if((weight == cTactic.WEIGHTS['good-deal'] or 
        weight == cTactic.WEIGHTS['better-deal']) and 
        len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield)):
        return cTactic.WEIGHTS['good-deal']
    else:
        return weight


def weight_for_discl_supported(discl_supported, weight):
    if((weight == cTactic.WEIGHTS['good-deal'] or 
        weight == cTactic.WEIGHTS['better-deal']) and 
        len(discl_supported.attacker_beyond) > len(discl_supported.supporter_beyond)):
        return cTactic.WEIGHTS['stormy']
    return weight


def weight_for_discl_attacked(discl_attacked, weight):
    if((weight == cTactic.WEIGHTS['good-deal'] or 
        weight == cTactic.WEIGHTS['better-deal']) and 
        len(discl_attacked.supporter_beyond) <= len(discl_attacked.attacker_beyond)):
        return cTactic.WEIGHTS['stormy']
    else:
        return weight


def weight_for_supporting(match, piece, move, supported, weight):
    if(is_touched_field_within_move(match, piece, move, supported.field)):
        return weight
    if(weight == cTactic.WEIGHTS['good-deal'] or 
       weight == cTactic.WEIGHTS['better-deal']):
        if(len(supported.attacker_beyond) > 0 and
           len(supported.attacker_beyond) > len(supported.supporter_beyond) and
           (is_supporter_lower_attacker(match, piece, move, supported) or
            match.is_soft_pin((supported.field))[0])):
            return cTactic.WEIGHTS['stormy']
    return weight


def weight_for_attacking_king(match, move, weight):
    if(check_mates_deep_search(match, move)):
        return cTactic.WEIGHTS['stormy']
    else:
        return weight


def weight_for_attacking(match, piece, move, attacked, weight):
    friends_on_dstfield, enmies_on_dstfield = find_touches_on_dstfield_after_move(match, piece, move)
    ###
    if(is_touched_field_within_move(match, piece, move, attacked.field)):
        return weight
    if(weight == cTactic.WEIGHTS['good-deal'] or 
       weight == cTactic.WEIGHTS['better-deal']):
        if(PIECES_RANK[piece] < PIECES_RANK[attacked.piece] or  
           (len(attacked.supporter_beyond) == 0 or
            len(attacked.supporter_beyond) <= len(attacked.attacker_beyond) or
            match.is_soft_pin((attacked.field))[0])): 
            return cTactic.WEIGHTS['stormy']
        elif(PIECES_RANK[piece] < PIECES_RANK[attacked.piece] and 
             PIECES_RANK[piece] == PIECES_RANK[PIECES['wPw']] and
             (len(friends_on_dstfield) > 0 or len(enmies_on_dstfield) == 0)): 
            return cTactic.WEIGHTS['better-deal']
    return cTactic.WEIGHTS['bad-deal']

