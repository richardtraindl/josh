
from ..values import *
from ..match import *
from ..pieces.whitepawn import cWhitePawn
from ..pieces.blackpawn import cBlackPawn
from ..pieces.knight import cKnight
from ..pieces.bishop import cBishop
from ..pieces.rook import cRook
from ..pieces.king import cKing
from ..pieces.queen import cQueen
from ..pieces import pawnfield
from ..pieces.touch import cTouch
from ..pieces.searchforpiece import list_field_touches, list_all_field_touches, list_field_touches_beyond


class cDirTouch:
    def __init__(self, piece, direction, field):
        self.piece = piece
        self.direction = direction
        self.field = field


def search_dir(match, field, direction, excl):
    dirtouches = []
    src = field
    step = cQueen.step_for_dir(direction)
    if(step is None):
        return dirtouches
    for i in range(7):
        dst = match.board.search(src, step, cQueen.MAXCNT)
        if(dst is not None and dst != excl):
            piece = match.board.getfield(dst)
            dirtouches.append(cDirTouch(piece, direction, dst))
            src = dst
        else:
            break
    return dirtouches


def search_lines_of_pin(match, color, field, excl):
    pinlines = []
    piece = match.board.getfield(field)
    oppcolor = REVERSED_COLORS[color]
 
    for i in range(len(cQueen.DIRS_ARY)):
        dirtouches = search_dir(match, field, cQueen.DIRS_ARY[i], excl)
        if(len(dirtouches) < 2):
            continue

        if(match.color_of_piece(dirtouches[0].piece) == color and 
           match.color_of_piece(dirtouches[1].piece) == oppcolor and
           PIECES_RANK[piece] > PIECES_RANK[dirtouches[0].piece] and 
           PIECES_RANK[piece] > PIECES_RANK[dirtouches[1].piece]):

            if(dirtouches[1].piece == PIECES['wQu'] or dirtouches[1].piece == PIECES['bQu']):
                pinlines.append([dirtouches[0], dirtouches[1]])

            elif(i < 4 and (dirtouches[1].piece == PIECES['wRk'] or dirtouches[1].piece == PIECES['bRk'])): 
                pinlines.append([dirtouches[0], dirtouches[1]])

            elif(i >= 4 and (dirtouches[1].piece == PIECES['wBp'] or dirtouches[1].piece == PIECES['bBp'])):
                pinlines.append([dirtouches[0], dirtouches[1]])

    return pinlines


def is_supported_running_pawn(match, supported):
    if(match.is_endgame() == False):
        return False
    if(supported.piece == PIECES['wPw']):
        cpawn = cWhitePawn(match, (supported.fieldx + supported.fieldy * 8))
        if(cpawn.is_running()):
            return True
    elif(supported.piece == PIECES['bPw']):
        cpawn = cBlackPawn3(match, (supported.fieldx + supported.fieldy * 8))
        if(cpawn.is_running()):
            return True
    return False


def castles(match, move):
    piece = match.board.getfield(move.src)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(abs(move.src - move.dst) == 2):
            return True
    return False


def promotes(move):
    if(move.prompiece != PIECES['blk']):
        return True
    else:
        return False


def captures(match, move):
    piece = match.board.getfield(move.src)
    color = match.color_of_piece(piece)
    dstpiece = match.board.getfield(move.dst)
    if(dstpiece != PIECES['blk']):
        return True
    elif((piece == PIECES['wPw'] or piece == PIECES['bPw']) and 
         (move.src % 8) != (move.dst %8)):
        return True
    else:
        return False


def forks(piece, from_dstfield_attacked):
    if(len(from_dstfield_attacked) < 2):
        return False
    count = 0
    for attacked in from_dstfield_attacked:
        if(len(attacked.supporter_beyond) == 0 or
           PIECES_RANK[attacked.piece] >= PIECES_RANK[piece]):
            count += 1
    return count >= 2


def defends_fork(match, move, piece, dstpiece):
    attacked = []
    supported = []
    if(dstpiece == PIECES['blk']):
        if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
            cpawn = match.obj_for_piece(piece, move.src)
            if(cpawn.is_ep_move_ok(move.dst)):
                forking = move.src
                forking_piece = match.board.getfield(forking)
            else:
                return False
        else:
            return False
    else:
        forking = move.dst
        forking_piece = dstpiece

    cforking_piece = match.obj_for_piece(forking_piece, forking)
    if(cforking_piece is not None):
        cforking_piece.find_attacks_and_supports(attacked, supported)
        return forks(forking_piece, attacked)
    else:
        return False


def threatens_fork(match, move):
    attacked = []
    supported = []
    is_fork_threat = False
    piece = match.board.getfield(move.src)
    ###
    newmatch = copy.deepcopy(match)
    newmatch.do_move(move.src, move.dst, move.prompiece)
    cpiece = newmatch.obj_for_piece(piece, move.dst)
    first_move_dir = cpiece.dir_for_move(move.src, move.dst)
    if(cpiece is not None):
        moves = cpiece.generate_moves(False, None, False, None)
        for mv in moves:
            cnewpiece = newmatch.obj_for_piece(piece, mv.dst)
            second_move_dir = cnewpiece.dir_for_move(mv.src, mv.dst)
            if(first_move_dir == second_move_dir or 
               REVERSE_DIRS[first_move_dir] == second_move_dir):
                continue
            newdstpiece = newmatch.board.getfield(mv.dst)
            newmatch.board.setfield(mv.src, PIECES['blk'])
            newmatch.board.setfield(mv.dst, piece)
            if(cnewpiece is not None):
                attacked.clear()
                supported.clear()
                cnewpiece.find_attacks_and_supports(attacked, supported)
                if(forks(piece, attacked)):
                    is_fork_threat = True
                    newmatch.board.setfield(mv.src, piece)
                    newmatch.board.setfield(mv.dst, newdstpiece)
                    break
            newmatch.board.setfield(mv.src, piece)
            newmatch.board.setfield(mv.dst, newdstpiece)
    ###
    return is_fork_threat


def flees(match, move):
    lower_enmy_cnt_old = 0
    lower_enmy_cnt_new = 0
    piece = match.board.getfield(move.src)
    color = match.color_of_piece(piece)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        return False
    frdlytouches_old, enmytouches_old = list_all_field_touches(match, move.src, color)
    ###
    match.do_move(move.src, move.dst, move.prompiece)
    frdlytouches_new, enmytouches_new = list_all_field_touches(match, move.dst, color)
    match.undo_move()
    ###
    if(len(enmytouches_old) > 0 and 
       (len(frdlytouches_old) < len(frdlytouches_new))):
        return True
    if(len(enmytouches_old) > len(enmytouches_new)):
        return True
    for enmy in enmytouches_old:
        if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
            lower_enmy_cnt_old += 1
    for enmy in enmytouches_new:
        if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
            lower_enmy_cnt_new += 1
    if(lower_enmy_cnt_old > lower_enmy_cnt_new):
        return True
    else:
        return False


def find_touches_after_move(match, move):
    attacked = []
    supported = []
    piece = match.board.getfield(move.src)
    ###
    match.do_move(move.src, move.dst, move.prompiece)
    cpiece = match.obj_for_piece(piece, move.dst)
    cpiece.find_attacks_and_supports(attacked, supported)
    if(cpiece.piece == PIECES['wKg'] or cpiece.piece == PIECES['bKg']):
        if((move.src % 8) - (move.dst % 8) == -2):
            crook = cRook(match, move.dst)
            crook.find_attacks_and_supports(attacked, supported)
        elif((move.src % 8) - (move.dst % 8) == 2):
            crook = cRook(match, move.dst + 1)
            crook.find_attacks_and_supports(attacked, supported)
    match.undo_move()
    ###
    return supported, attacked


def find_touches_on_dstfield_after_move(match, move):
    piece = match.board.getfield(move.src)
    match.do_move(move.src, move.dst, move.prompiece)
    list_all_field_touches(match, move.dst, match.color_of_piece(piece))
    match.undo_move()
    return frdlytouches, enmytouches


def does_unpin(match, move):
    piece = match.board.getfield(move.src)
    color = match.color_of_piece(piece)
    pinlines_before = search_lines_of_pin(match, color, move.src, move.dst)
    ###
    match.do_move(move.src, move.dst, move.prompiece)
    pinlines_after = search_lines_of_pin(match, color, move.dst, None)
    match.undo_move()
    ###
    if(len(pinlines_after) < len(pinlines_before)):
        return True
    for pbefore in pinlines_before:
        identical = False
        for pafter in pinlines_after:
            if(pbefore[0].field == pafter[0].field):
                identical = True
        if(identical == False):
            return True
    return False


def defends_check(match):
    if(match.next_color() == COLORS['white']):
        return is_field_touched(match, match.board.wKg, COLORS['black'], cMatch.EVAL_MODES['ignore-pins'])
    else:
        return is_field_touched(match, match.board.bKg, COLORS['white'], cMatch.EVAL_MODES['ignore-pins'])


def find_disclosed_pieces(match, src, dst, discl_attacked, discl_supported):
    piece = match.board.getfield(src)
    color = match.color_of_piece(piece)
    #
    excldir = cRook.dir_for_move(src, dst)
    for i in range(0, len(cRook.STEPS), 2):
        if(excldir != cRook.DIRS_ARY[i] and excldir != cRook.DIRS_ARY[i + 1]):
            first, second = match.board.search_bi_dirs(src, cRook.STEPS[0], cRook.MAXCNT)
            if(first and second):
                first_piece = match.board.getfield(first)
                second_piece = match.board.getfield(second)
                if(match.color_of_piece(first_piece) == match.color_of_piece(second_piece)):
                    disclosed = discl_supported
                else:
                    disclosed = discl_attacked
                if(match.color_of_piece(first_piece) == color and
                   (PIECES_BARE[first_piece] == PIECES_BARE[PIECES['wRk']] or
                    PIECES_BARE[first_piece] == PIECES_BARE[PIECES['wQu']])):
                    disclosed.append(cTouch(PIECES[second], second))
                elif(match.color_of_piece(second_piece) == color and
                     (PIECES_BARE[second_piece] == PIECES_BARE[PIECES['wRk']] or
                      PIECES_BARE[second_piece] == PIECES_BARE[PIECES['wQu']])):
                    disclosed.append(cTouch(first_piece, first))
    #
    excldir = cBishop.dir_for_move(src, dst)
    for i in range(0, len(cBishop.STEPS), 2):
        if(excldir != cBishop.DIRS_ARY[i] and excldir != cBishop.DIRS_ARY[i + 1]):
            first, second = match.board.search_bi_dirs(src, cBishop.STEPS[0], cBishop.MAXCNT)
            if(first and second):
                first_piece = match.board.getfield(first)
                second_piece = match.board.getfield(second)
                if(match.color_of_piece(first_piece) == match.color_of_piece(second_piece)):
                    disclosed = discl_supported
                else:
                    disclosed = discl_attacked
                if(match.color_of_piece(first_piece) == color and
                   (PIECES_BARE[first_piece] == PIECES_BARE[PIECES['wBp']] or
                    PIECES_BARE[first_piece] == PIECES_BARE[PIECES['wQu']])):
                    disclosed.append(cTouch(second_piece, second))
                elif(match.color_of_piece(second_piece) == color and
                     (PIECES_BARE[second_piece] == PIECES_BARE[PIECES['wBp']] or
                      PIECES_BARE[second_piece] == PIECES_BARE[PIECES['wQu']])):
                    disclosed.append(cTouch(first_piece, first))


def find_disclosures(match, move):
    discl_supported = []
    discl_attacked = []
    piece = match.board.getfield(move.src)
    color = match.color_of_piece(piece)
    ###
    match.do_move(move.src, move.dst, move.prompiece)
    find_disclosed_pieces(match, move.src, move.dst, discl_attacked, discl_supported)
    match.undo_move()
    ###
    match.board.setfield(move.src, PIECES['blk'])
    for ctouch_beyond in discl_attacked:
        list_field_touches_beyond(match, ctouch_beyond, color)
    for ctouch_beyond in discl_supported:
        list_field_touches_beyond(match, ctouch_beyond, color)
    match.board.setfield(move.src, piece)
    ###
    return discl_supported, discl_attacked


def blocks(match, move):
    STEPS = [8, 1, 9, -7]
    piece = match.board.getfield(move.src)
    color = match.color_of_piece(piece)
    #frdlytouches_before_count = 0
    enmytouches_before_count = 0
    #frdlytouches_after_count = 0
    enmytouches_after_count = 0
    for step in STEPS:
        dst1, dst2 = match.board.search_bi_dirs(move.dst, step)
        if(dst1 is not None):
            if(dst1 == move.src or dst2 == move.src):
                continue
            piece1 = match.board.getfield(dst1)
            piece2 = match.board.getfield(dst2)
            if(match.color_of_piece(piece1) == match.color_of_piece(piece2)):
                continue
            if(match.color_of_piece(piece1) == color):
                frdlytouches, enmytouches = list_all_field_touches(match, dst1, color)
            else:
                frdlytouches, enmytouches = list_all_field_touches(match, dst2, color)
            enmytouches_before_count += len(enmytouches)
    ###
    match.do_move(move.src, move.dst, move.prompiece)
    for step in STEPS:
        dst1, dst2 = match.board.search_bi_dirs(move.dst, step)
        if(dst1 is not None):
            if(dst1 == move.src or dst2 == move.src):
                continue
            piece1 = match.board.getfield(dst1)
            piece2 = match.board.getfield(dst2)
            if(match.color_of_piece(piece1) == match.color_of_piece(piece2)):
                continue
            if(match.color_of_piece(piece1) == color):
                frdlytouches, enmytouches = list_all_field_touches(match, dst1, color)
            else:
                frdlytouches, enmytouches = list_all_field_touches(match, dst2, color)
            enmytouches_after_count += len(enmytouches)
    match.undo_move()
    ###
    if(enmytouches_after_count < enmytouches_before_count):
           return True
    else:
        return False


def running_pawn_in_endgame(match, move):
    if(match.is_endgame()):
        piece = match.board.getfield(move.src)
        if(piece == PIECES['wPw']):
            cpawn = cWhitePawn(match, move.src)
            return cpawn.is_running()
        elif(piece == PIECES['bPw']):
            cpawn = cBlackPawn(match, move.src)
            return cpawn.is_running()
    return False


def defends_invasion(match, move):
    """piece = match.board.getfield(move.src)
    color = match.color_of_piece(piece)
    board =  [[0] * 8 for i in range(8)]

    for y in range(8):
        for x in range(8):
            piece = match.board.readfield(x, y)
            if(match.color_of_piece(piece) == COLORS['white']):
                board[y][x] += 1
            elif(match.color_of_piece(piece) == COLORS['black']):
                board[y][x] -= 1"""
    return False


def controles_file(match, move):
    return False


def is_tactical_draw(match, move):
    if(match.is_fifty_moves_rule()):
        return True
    match.do_move(move.src, move.dst, move.prompiece)
    is_move_repetition = match.is_move_repetition()
    match.undo_move()
    return is_move_repetition


def is_progress(match, move):
    return False

