
from ..match import *
from ..board import cBoard
from ..pieces.whitepawn import cWhitePawn
from ..pieces.blackpawn import cBlackPawn
from ..pieces.king import cKing


def score_traps_and_touches(match):
    score = 0
    fields = match.board.fields
    for idx in range(63, -1, -1):
        piece = fields & 0xF
        fields = fields >> 4
        #piece = match.board.getfield(idx)
        cpiece = match.obj_for_piece(piece, idx)
        if(cpiece is None):
            continue
        score += cpiece.score_touches()
        if(cpiece.is_trapped()):
            score += SCORES[cpiece.piece] // 3
    return score


def score_controled_horizontal_files(match):
    score = 0
    row7_row8 = 0x000000000000000000000000000000000000000000000000FFFFFFFFFFFFFFFF
    wrooks = match.board.fields
    cBoard.mask_pieces(wrooks, PIECES['wRk'])
    wqueens = match.board.fields
    cBoard.mask_pieces(wqueens, PIECES['wQu'])
    if(wrooks & row7_row8 or wqueens & row7_row8):
        score += ATTACKED_SCORES[PIECES['bKn']]

    row1_row2 = 0xFFFFFFFFFFFFFFFF000000000000000000000000000000000000000000000000
    brooks = match.board.fields
    cBoard.mask_pieces(brooks, PIECES['bRk'])
    bqueens = match.board.fields
    cBoard.mask_pieces(bqueens, PIECES['bQu'])
    if(brooks & row1_row2 or bqueens & row1_row2):
        score += ATTACKED_SCORES[PIECES['wKn']]
    return score


def score_controled_vertical_files(match):
    score = 0
    wpwcolumn = 0x0000000010000000100000001000000010000000100000001000000000000000
    wrkcolumn = 0x4000000040000000400000004000000040000000400000004000000040000000
    wqucolumn = 0x5000000050000000500000005000000050000000500000005000000050000000
    wpawns = match.board.fields
    cBoard.mask_pieces(wpawns, PIECES['wPw'])
    if(wpawns & wpwcolumn == 0x0):
        wrooks = match.board.fields
        cBoard.mask_pieces(wrooks, PIECES['wRk'])
        wqueens = match.board.fields
        cBoard.mask_pieces(wqueens, PIECES['wQu'])
        if(wrooks & wrkcolumn or wqueens & wqucolumn):
            score += ATTACKED_SCORES[PIECES['bKn']]

    bpwcolumn = 0x0000000090000000900000009000000090000000900000009000000000000000
    brkcolumn = 0xC0000000C0000000C0000000C0000000C0000000C0000000C0000000C0000000
    bqucolumn = 0xD0000000D0000000D0000000D0000000D0000000D0000000D0000000D0000000
    bpawns = match.board.fields
    cBoard.mask_pieces(bpawns, PIECES['bPw'])
    if(bpawns & bpwcolumn == 0x0):
        brooks = match.board.fields
        cBoard.mask_pieces(brooks, PIECES['bRk'])
        bqueens = match.board.fields
        cBoard.mask_pieces(bqueens, PIECES['bQu'])
        if(brooks & brkcolumn or bqueens & bqucolumn):
            score += ATTACKED_SCORES[PIECES['wKn']]
    return score


def score_kings_safety(match):
    value = 0
    cking = cKing(match, match.board.wKg)
    if(cking.is_safe() == False):
        value += ATTACKED_SCORES[PIECES['wQu']] * 5
    cking = cKing(match, match.board.bKg)
    if(cking.is_safe() == False):
        value += ATTACKED_SCORES[PIECES['bQu']] * 5
    return value


def score_penalty_for_lost_castlings(match):
    score = 0
    wcastling = False
    bcastling = False
    idx = 0
    for move in match.minutes:
        idx += 1
        piece = move.getprevfield(move.src)
        if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
            if(abs(move.src - move.dst) == 2):
                if(idx % 2 == 1):
                    wcastling = True
                else:
                    bcastling = True
    if(wcastling == False and (match.board.wKg_first_move_on is not None or
       (match.board.wRkA_first_move_on is not None or match.board.wRkH_first_move_on is not None))):
        score += ATTACKED_SCORES[PIECES['wRk']] * 2
    if(bcastling == False and (match.board.bKg_first_move_on is not None or
       (match.board.bRkA_first_move_on is not None or match.board.bRkH_first_move_on is not None))):
        score += ATTACKED_SCORES[PIECES['bRk']] * 2
    return score


"""def score_penalty_for_multiple_moves(match):
    value = 0
    white_moves = []
    black_moves = []

    for i in range(2):
        for move in match.minutes:
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
                if(lower_move.dst == higher_move.src):
                    lower_move = higher_move
                    mvtcnt += 1
            if(mvtcnt >= 2):
                value += rate
    return value"""


def score_penalty_for_knight_bishop_on_baseline(match):
    score = 0
    for i in range(2):
        if(i == 0):
            idx = match.board.RANKS['1'] * 8
            knight = PIECES['wKn']
            bishop = PIECES['wBp']
            rate = ATTACKED_SCORES[PIECES['wRk']]
        else:
            idx = match.board.RANKS['8'] * 8
            knight = PIECES['bKn']
            bishop = PIECES['bBp']
            rate = ATTACKED_SCORES[PIECES['bRk']]
        for i in range(8):
            piece = match.board.getfield(idx + i)
            if(piece == knight or piece == bishop):
                score += rate
    return score


"""def score_weak_pawns(match):
    value = 0
    for idx in range(64):
        piece = match.board.getfield(idx)
        if(piece == PIECES['wPw']):
            cpawn = cWhitePawn(match, idx)
            if(cpawn.is_weak()):
                value += ATTACKED_SCORES[PIECES['wRk']]
        elif(piece == PIECES['bPw']):
            cpawn = cBlackPawn(match, idx)
            if(cpawn.is_weak()):
                value += ATTACKED_SCORES[PIECES['bRk']]
    return value"""


def score_penalty_for_weak_fianchetto(match):
    score = 0
    piece = match.board.getfield(match.board.COLS['B'] + match.board.RANKS['2'] * 8)
    if(piece == PIECES['blk']):
        score += ATTACKED_SCORES[PIECES['wRk']]
    piece = match.board.getfield(match.board.COLS['G'] + match.board.RANKS['2'] * 8)
    if(piece == PIECES['blk']):
        score += ATTACKED_SCORES[PIECES['wRk']]
    piece = match.board.getfield(match.board.COLS['B'] + match.board.RANKS['7'] * 8)
    if(piece == PIECES['blk']):
        score += ATTACKED_SCORES[PIECES['bRk']]
    piece = match.board.getfield(match.board.COLS['G'] + match.board.RANKS['7'] * 8)
    if(piece == PIECES['blk']):
        score += ATTACKED_SCORES[PIECES['bRk']]
    return score


def score_opening(match):
    score = 0
    #score += score_penalty_for_multiple_moves(match)
    score += score_penalty_for_knight_bishop_on_baseline(match)
    score += score_penalty_for_lost_castlings(match)
    #score += score_weak_pawns(match)
    score += score_penalty_for_weak_fianchetto(match)
    return score


def score_middlegame(match):
    score = 0
    score += score_penalty_for_knight_bishop_on_baseline(match)
    #score += score_weak_pawns(match)
    score score


def score_endgame(match):
    score = 0
    whiterate = ATTACKED_SCORES[PIECES['bPw']]
    white_step_rates = [ 0, 0, 1, 2, 3, 4, 5, 0]
    blackrate = ATTACKED_SCORES[PIECES['wPw']]
    black_step_rates = [0, 5, 4, 3, 2, 1, 0, 0 ]
    for idx in range(64):
        piece = match.board.getfield(idx)
        if(piece == PIECES['wPw']):
            cpawn = cWhitePawn(match, idx)
            if(cpawn.is_running()):
                value += whiterate
                value += whiterate * white_step_rates[(idx // 8)]
        elif(piece == PIECES['bPw']):
            cpawn = cBlackPawn(match, idx)
            if(cpawn.is_running()):
                value += blackrate
                value += blackrate * black_step_rates[(idx // 8)]
    return score


def score_position(match, movecnt):
    status = match.evaluate_status()
    if(movecnt == 0 and status != match.STATUS['active']):
        if(status == match.STATUS['winner_black']):
            return ( SCORES[PIECES['wKg']] + match.movecnt() )
        elif(status == match.STATUS['winner_white']):
            return ( SCORES[PIECES['bKg']] - match.movecnt() )
        else: # draw
            return SCORES[PIECES['blk']]
    else:
        score = match.score
        score += score_traps_and_touches(match)
        score += score_kings_safety(match)
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
        piece = match.board.getfield((x + 6 * 8))
        if(piece == PIECES['wPw']):
            return True
    
    for x in range(8):
        piece = match.board.getfield((x + 1 * 8))
        if(piece == PIECES['bPw']):
            return True
    ###

    ### attacks
    for idx in range(64):
        piece = match.board.getfield(idx)
        if(piece == PIECES['blk']):
            continue

        piece_color = match.color_of_piece(piece)

        frdlytouches, enmytouches = list_all_field_touches(match, (idx % 8), (idx // 8), piece_color)

        """if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
            if(len(enmytouches) > 0):
                return True
            else:
                continue"""

        """if(len(enmytouches) > len(frdlytouches)):
            return True"""

        if(match.is_pinned(idx) or match.is_soft_pin(idx)[0]):
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


