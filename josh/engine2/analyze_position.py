
from .match import *

from .pieces.white_pawn import cWhitePawn
from .pieces.black_pawn import cBlackPawn
from .pieces.king import cKing


def score_traps_and_touches(match):
    score = 0
    for y in range(8):
        for x in range(8):
            piece = match.board.readfield(x, y)
            cpiece = match.obj_for_piece(piece, x, y)
            if(cpiece is None):
                continue
            score += cpiece.score_touches()
            if(cpiece.is_trapped()):
                score += SCORES[cpiece.piece] // 3
    return score


def score_controled_horizontal_files(match):
    score = 0
    whiterate = ATTACKED_SCORES[PIECES['bKn']]
    blackrate = ATTACKED_SCORES[PIECES['wKn']]

    for y in range(0, 2, 1):
        wcnt = 0
        bcnt = 0
        for x in range(8):
            piece = match.board.readfield(x, y)
            if(piece == PIECES['wRk'] or piece == PIECES['wQu']):
                wcnt += 1
            elif(piece == PIECES['bRk'] or piece == PIECES['bQu']):
                bcnt += 1
            else:
                continue
        if(bcnt > wcnt):
            score += blackrate

    for y in range(6, 8, 1):
        wcnt = 0
        bcnt = 0
        for x in range(8):
            piece = match.board.readfield(x, y)
            if(piece == PIECES['bRk'] or piece == PIECES['bQu']):
                bcnt += 1
            elif(piece == PIECES['wRk'] or piece == PIECES['wQu']):
                wcnt += 1
            else:
                continue
        if(wcnt > bcnt):
            score += whiterate

    return score


def score_controled_vertical_files(match):
    score = 0
    whiterate = ATTACKED_SCORES[PIECES['bKn']]
    blackrate = ATTACKED_SCORES[PIECES['wKn']]

    for x in range(8):
        wcnt = 0
        bcnt = 0
        wpwcnt = 0
        bpwcnt = 0
        for y in range(8):
            piece = match.board.readfield(x, y)
            if(piece == PIECES['blk']):
                continue
            elif(piece == PIECES['wPw']):
                wpwcnt += 1
                continue
            elif(piece == PIECES['bPw']):
                bpwcnt += 1
                continue
            elif(piece == PIECES['wRk'] or piece == PIECES['wQu']):
                wcnt += 1
                continue
            elif(piece == PIECES['bRk'] or piece == PIECES['bQu']):
                bcnt += 1
                continue
            else:
                continue

        if(wpwcnt == 0 and bpwcnt == 0):
            if(wcnt > bcnt):
                score += whiterate
            elif(bcnt > wcnt):
                score += blackrate
    return score


def score_kings_safety(match):
    value = 0
    cking = cKing(match, match.board.wKg_x, match.board.wKg_y)
    if(cking.is_safe() == False):
        value += ATTACKED_SCORES[PIECES['wQu']] * 10
    cking = cKing(match, match.board.bKg_x, match.board.bKg_y)
    if(cking.is_safe() == False):
        value += ATTACKED_SCORES[PIECES['bQu']] * 10
    return value


def score_penalty_for_lost_castlings(match):
    value = 0
    wcastling = False
    bcastling = False

    for move in match.move_list:
        if(move.is_castling()):
            if(move.count % 2 == 1):
                wcastling = True
            else:
                bcastling = True

    if(wcastling == False and (match.board.wKg_first_move_on is not None or
       (match.board.wRkA_first_move_on is not None or match.board.wRkH_first_move_on is not None))):
        value += ATTACKED_SCORES[PIECES['wRk']] * 2
    
    if(bcastling == False and (match.board.bKg_first_move_on is not None or
       (match.board.bRkA_first_move_on is not None or match.board.bRkH_first_move_on is not None))):
        value += ATTACKED_SCORES[PIECES['bRk']] * 22

    return value


def score_penalty_for_multiple_moves(match):
    value = 0
    white_moves = []
    black_moves = []

    for i in range(2):
        for move in match.move_list:
            if(move.captpiece):
                continue
            if(move.count % 2 == 1):
                white_moves.append(move)
            else:
                black_moves.append(move)

    for i in range(2):
        if(i == 0):
            moves = white_moves
            rate =  ATTACKED_SCORES[PIECES['wRk']]
        else:
            moves = black_moves
            rate =  ATTACKED_SCORES[PIECES['bRk']]

        idx = 0
        for move in moves:
            idx += 1
            mvtcnt = 0
            if(idx == len(moves)):
                break
            lower_move = move
            for higher_move in moves[idx:]:
                if(lower_move.dstx == higher_move.srcx and lower_move.dsty == higher_move.srcy):
                    lower_move = higher_move
                    mvtcnt += 1
            if(mvtcnt >= 2):
                value += rate
    return value


def score_penalty_for_knight_bishop_on_baseline(match):
    value = 0
    for i in range(2):
        if(i == 0):
            y = match.board.RANKS['1']
            knight = PIECES['wKn']
            bishop = PIECES['wBp']
            rate = ATTACKED_SCORES[PIECES['wRk']]
        else:
            y = match.board.RANKS['8']
            knight = PIECES['bKn']
            bishop = PIECES['bBp']
            rate = ATTACKED_SCORES[PIECES['bRk']]
        for x in range(8):
            piece = match.board.readfield(x, y)
            if(piece == knight or piece == bishop):
                value += rate
    return value


def score_weak_pawns(match):
    value = 0
    for y in range(8):
        for x in range(8):
            piece = match.board.readfield(x, y)
            if(piece == PIECES['wPw']):
                cpawn = cWhitePawn(match, x, y)
                if(cpawn.is_weak()):
                    value += ATTACKED_SCORES[PIECES['wRk']]
            elif(piece == PIECES['bPw']):
                cpawn = cBlackPawn(match, x, y)
                if(cpawn.is_weak()):
                    value += ATTACKED_SCORES[PIECES['bRk']]
    return value


def score_penalty_for_weak_fianchetto(match):
    value = 0

    piece = match.board.readfield(match.board.COLS['B'], match.board.RANKS['2'])
    if(piece == PIECES['blk']):
        value += ATTACKED_SCORES[PIECES['wRk']]

    piece = match.board.readfield(match.board.COLS['G'], match.board.RANKS['2'])
    if(piece == PIECES['blk']):
        value += ATTACKED_SCORES[PIECES['wRk']]

    piece = match.board.readfield(match.board.COLS['B'], match.board.RANKS['7'])
    if(piece == PIECES['blk']):
        value += ATTACKED_SCORES[PIECES['bRk']]

    piece = match.board.readfield(match.board.COLS['G'], match.board.RANKS['7'])
    if(piece == PIECES['blk']):
        value += ATTACKED_SCORES[PIECES['bRk']]

    return value


def score_opening(match):
    value = 0
    value += score_penalty_for_multiple_moves(match)
    value += score_penalty_for_knight_bishop_on_baseline(match)
    value += score_kings_safety(match)
    value += score_penalty_for_lost_castlings(match)
    value += score_weak_pawns(match)
    value += score_penalty_for_weak_fianchetto(match)
    return value


def score_middlegame(match):
    value = 0
    value += score_penalty_for_knight_bishop_on_baseline(match)
    value += score_kings_safety(match)
    value += score_weak_pawns(match)
    return value


def score_endgame(match):
    value = 0
    whiterate = ATTACKED_SCORES[PIECES['bPw']]
    white_step_rates = [ 0, 0, 1, 2, 3, 4, 5, 0]
    blackrate = ATTACKED_SCORES[PIECES['wPw']]
    black_step_rates = [0, 5, 4, 3, 2, 1, 0, 0 ]
    for y in range(8):
        for x in range(8):
            piece = match.board.readfield(x, y)
            if(piece == PIECES['wPw']):
                cpawn = cWhitePawn(match, x, y)
                if(cpawn.is_running()):
                    value += whiterate
                    value += whiterate * white_step_rates[y]
            elif(piece == PIECES['bPw']):
                cpawn = cBlackPawn(match, x, y)
                if(cpawn.is_running()):
                    value += blackrate
                    value += blackrate * black_step_rates[y]
    #value += score_kings_safety(match)
    return value


def score_position(match, movecnt):
    status = match.evaluate_status()

    if(movecnt == 0 and status != match.STATUS['open']):
        if(status == match.STATUS['winner_black']):
            return ( SCORES[PIECES['wKg']] + match.movecnt() )
        elif(status == match.STATUS['winner_white']):
            return ( SCORES[PIECES['bKg']] - match.movecnt() )
        else: # draw
            return SCORES[PIECES['blk']]
    else:
        score = match.score
        score += score_traps_and_touches(match)
        score += score_controled_horizontal_files(match)
        score += score_controled_vertical_files(match)
        if(match.is_opening()):
            score += score_opening(match)
        elif(match.is_endgame()):
            score += score_endgame(match)
        else:
            score += score_middlegame(match)
        return score


def is_stormy(match):
    color = match.next_color()

    ### is pawn on last row before promotion
    for x in range(8):
        piece = match.board.readfield(x, 6)
        if(piece == PIECES['wPw']):
            return True
    
    for x in range(8):
        piece = match.board.readfield(x, 1)
        if(piece == PIECES['bPw']):
            return True
    ###

    ### attacks
    for y in range(8):
        for x in range(8):
            piece = match.board.readfield(x, y)
            if(piece == PIECES['blk']):
                continue

            piece_color = match.color_of_piece(piece)

            frdlytouches, enmytouches = list_all_field_touches(match, x, y, piece_color)

            """if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                if(len(enmytouches) > 0):
                    return True
                else:
                    continue"""

            """if(len(enmytouches) > len(frdlytouches)):
                return True"""

            if(match.is_pinned(x, y) or match.is_soft_pin(x, y)[0]):
                return True

            for enmy in enmytouches:
                if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
                    return True

                """enmyfriends, enmyenemies = list_all_field_touches(match, Match.color_of_piece(enmy.piece), enmy.fieldx, enmy.fieldy)
                if(len(enmyenemies) == 0):
                    print("is_stormy: enmyenemies == 0")
                    return True"""
    ###

    return False


