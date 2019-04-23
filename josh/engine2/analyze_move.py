
from operator import attrgetter
import copy

from .match import *
from .move import *
from .helper import reverse_lookup
from .analyze_helper import *
from .generator import cGenerator

from .pieces.white_pawn import cWhitePawn
from .pieces.black_pawn import cBlackPawn
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .pieces.touch import cTouch
from .pieces.search_for_piece import list_all_field_touches, list_field_touches_beyond


def castles(gmove):
    match = gmove.match
    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(gmove.srcx - gmove.dstx == 2 or gmove.srcx - gmove.dstx == -2):
            return True


def promotes(gmove):
    if(gmove.prompiece != PIECES['blk']):
        return True


def captures(gmove):
    match = gmove.match
    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)
    dstpiece = match.board.readfield(gmove.dstx, gmove.dsty)
    if(dstpiece != PIECES['blk']):
        return True
    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and gmove.srcx != gmove.dstx ):
        return True
    else:
        return False


def exhausts_enemy(gmove):
    match = gmove.match
    ###
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
    is_discovered_attack_after_move = match.is_discovered_attack(gmove.dstx, gmove.dsty)
    match.undo_move()
    ###
    return is_discovered_attack_after_move and match.is_soft_pin(gmove.dstx, gmove.dsty)[0]


def forks(piece, from_dstfield_attacked):
    if(len(from_dstfield_attacked) < 2):
        return False
    count = 0
    for attacked in from_dstfield_attacked:
        if(len(attacked.supporter_beyond) == 0 or
           PIECES_RANK[attacked.piece] >= PIECES_RANK[piece]):
            count += 1
    return count >= 2


def defends_fork(gmove, piece, dstpiece):
    attacked = []
    supported = []
    match = gmove.match

    if(dstpiece == PIECES['blk']):
        if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
            cpawn = match.obj_for_piece(piece, gmove.srcx, gmove.srcy)
            if(cpawn.is_ep_move_ok(gmove.dstx, gmove.dsty)):
                forkingx = gmove.srcx
                forkingy = gmove.dsty
                forking_piece = match.board.readfield(forkingx, forkingy)
            else:
                return False
        else:
            return False
    else:
        forkingx = gmove.dstx
        forkingy = gmove.dsty
        forking_piece = dstpiece

    cforking_piece = match.obj_for_piece(forking_piece, forkingx, forkingy)
    if(cforking_piece is not None):
        cforking_piece.find_attacks_and_supports(attacked, supported)
        return forks(forking_piece, attacked)
    else:
        return False


def threatens_fork(gmove):
    attacked = []
    supported = []
    is_fork_threat = False
    match = gmove.match
    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    ###
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
    cpiece = match.obj_for_piece(piece, gmove.dstx, gmove.dsty)
    first_move_dir = cpiece.dir_for_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)
    if(cpiece is not None):
        moves = cpiece.generate_moves(False)
        for move in moves:
            cnewpiece = match.obj_for_piece(piece, move.dstx, move.dsty)
            second_move_dir = cnewpiece.dir_for_move(move.srcx, move.srcy, move.dstx, move.dsty)
            if(first_move_dir == second_move_dir or 
               REVERSE_DIRS[first_move_dir] == second_move_dir):
                continue
            newdstpiece = match.board.readfield(move.dstx, move.dsty)
            match.board.writefield(move.srcx, move.srcy, PIECES['blk'])
            match.board.writefield(move.dstx, move.dsty, piece)
            if(cnewpiece is not None):
                attacked.clear()
                supported.clear()
                cnewpiece.find_attacks_and_supports(attacked, supported)
                if(forks(piece, attacked)):
                    is_fork_threat = True
                    match.board.writefield(move.srcx, move.srcy, piece)
                    match.board.writefield(move.dstx, move.dsty, newdstpiece)
                    break
            match.board.writefield(move.srcx, move.srcy, piece)
            match.board.writefield(move.dstx, move.dsty, newdstpiece)
    match.undo_move()
    ###
    return is_fork_threat


def flees(gmove):
    match = gmove.match
    lower_enmy_cnt_old = 0
    lower_enmy_cnt_new = 0
    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)

    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        return False

    frdlytouches_old, enmytouches_old = list_all_field_touches(match, gmove.srcx, gmove.srcy, color)
    ###
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
    frdlytouches_new, enmytouches_new = list_all_field_touches(match, gmove.dstx, gmove.dsty, color)
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


def find_touches_after_move(gmove):
    attacked = []
    supported = []
    match = gmove.match
    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    ###
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
    cpiece = match.obj_for_piece(piece, gmove.dstx, gmove.dsty)
    if(cpiece):
        cpiece.find_attacks_and_supports(attacked, supported)
        if(cpiece.piece == PIECES['wKg'] or cpiece.piece == PIECES['bKg']):
            if(gmove.srcx - gmove.dstx == -2):
                crook = cRook(match, gmove.dstx - 1, gmove.dsty)
                crook.find_attacks_and_supports(attacked, supported)
            elif(gmove.srcx - gmove.dstx == 2):
                crook = cRook(match, gmove.dstx + 1, gmove.dsty)
                crook.find_attacks_and_supports(attacked, supported)
    match.undo_move()
    ###
    return supported, attacked


def find_touches_on_dstfield_after_move(gmove):
    match = gmove.match
    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
    frdlytouches, enmytouches = list_all_field_touches(match, gmove.dstx, gmove.dsty, match.color_of_piece(piece))
    match.undo_move()
    return frdlytouches, enmytouches


def does_unpin(gmove):
    match = gmove.match
    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)
    pinlines_before = search_lines_of_pin(match, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)
    ###
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
    pinlines_after = search_lines_of_pin(match, color, gmove.dstx, gmove.dsty, None, None)
    match.undo_move()
    ###
    if(len(pinlines_after) < len(pinlines_before)):
        return True
    for pbefore in pinlines_before:
        identical = False
        for pafter in pinlines_after:
            if(pbefore[0].fieldx == pafter[0].fieldx and pbefore[0].fieldy == pafter[0].fieldy):
                identical = True
        if(identical == False):
            return True
    return False


def defends_check(match):
    if(match.next_color() == COLORS['white']):
        cking = cKing(match, match.board.wKg_x, match.board.wKg_y)
    else:
        cking = cKing(match, match.board.bKg_x, match.board.bKg_y)
    return cking.is_attacked()


def is_attacked_king_safe(match, piece):
    if(match.oppcolor_of_piece(piece) == COLORS['white']):
        cking = cKing(match, match.board.wKg_x, match.board.wKg_y)
    else:
        cking = cKing(match, match.board.bKg_x, match.board.bKg_y)
    return cking.is_safe()


def calc_checks(match, maxcnt, count):
    cgenerator = cGenerator(match)
    priomoves = cgenerator.generate_priomoves()
    if(len(priomoves) == 0 and count % 2 == 1):
        return True
    if(count >= maxcnt):
        return False
    for priomove in priomoves:
        gmove = priomove.gmove
        match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
        if(calc_checks(match, maxcnt, count + 1)):
            return True
        else:
            match.undo_move()
    return False

def check_mates_deep_search(gmove):
    newmatch = copy.deepcopy(gmove.match)
    newmatch.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
    return calc_checks(newmatch, 3, 1)


def check_mates(gmove):
    match = gmove.match
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
    is_move_available = match.is_move_available()
    match.undo_move()
    return not is_move_available


def find_disclosed_pieces(match, srcx, srcy, dstx, dsty, discl_attacked, discl_supported):
    piece = match.board.readfield(srcx, srcy)
    color = match.color_of_piece(piece)
    idx = 0
    for step in cQueen.STEPS:
        if(idx % 2 == 0):
            first = cTouch(PIECES['blk'], 0, 0)
            second = cTouch(PIECES['blk'], 0, 0)
        if(idx < 4):
            cpiece = cRook
            excluded_dir = cRook.dir_for_move(srcx, srcy, dstx, dsty)
            faces = [PIECES['wRk'], PIECES['bRk'], PIECES['wQu'], PIECES['bQu']]
        else:
            cpiece = cBishop
            excluded_dir = cBishop.dir_for_move(srcx, srcy, dstx, dsty)
            faces = [PIECES['wBp'], PIECES['bBp'], PIECES['wQu'], PIECES['bQu']]
        idx += 1

        stepx = step[0]
        stepy = step[1]
        direction = cpiece.dir_for_move(srcx, srcy, (srcx + stepx), (srcy + stepy))
        if(direction == excluded_dir or direction == REVERSE_DIRS[excluded_dir]):
            break
        x1, y1 = match.board.search(srcx, srcy, stepx, stepy)
        if(x1 is not None):
            piece = match.board.readfield(x1, y1)
            if(first.piece == PIECES['blk']):
                first.piece = piece
                first.fieldx = x1
                first.fieldy = y1
                continue
            elif(second.piece == PIECES['blk']):
                second.piece = piece
                second.fieldx = x1
                second.fieldy = y1

            if(first.piece == PIECES['blk'] or second.piece == PIECES['blk']):
                continue
                
            if(match.color_of_piece(first.piece) != match.color_of_piece(second.piece)):
                if(match.color_of_piece(first.piece) == color):
                    for face in faces:
                        if(first.piece == face):
                            discl_attacked.append(second)
                            break
                else:
                    for face in faces:
                        if(second.piece == face):
                            discl_attacked.append(first)
                            break
            elif(match.color_of_piece(first.piece) == match.color_of_piece(second.piece)):
                if(match.color_of_piece(first.piece) == color):
                    for face in faces:
                        if(first.piece == face):
                            discl_supported.append(second)
                            break
                    for face in faces:
                        if(second.piece == face):
                            discl_supported.append(first)
                            break

def find_disclosures(match, gmove):
    discl_supported = []
    discl_attacked = []
    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)
    ###
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
    find_disclosed_pieces(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, discl_attacked, discl_supported)
    match.undo_move()
    ###
    match.board.writefield(gmove.srcx, gmove.srcy, PIECES['blk'])
    for ctouch_beyond in discl_attacked:
        list_field_touches_beyond(match, ctouch_beyond, color)
    for ctouch_beyond in discl_supported:
        list_field_touches_beyond(match, ctouch_beyond, color)
    match.board.writefield(gmove.srcx, gmove.srcy, piece)
    ###
    return discl_supported, discl_attacked


def blocks(gmove):
    STEPS = [ [0, 1], [1, 0], [1, 1], [-1, 1] ]
    match = gmove.match
    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)
    #frdlytouches_before_count = 0
    enmytouches_before_count = 0
    #frdlytouches_after_count = 0
    enmytouches_after_count = 0

    for step in STEPS:
        stepx = step[0]
        stepy = step[1]
        x1, y1, x2, y2 = match.board.search_bi_dirs(gmove.dstx, gmove.dsty, stepx, stepy)
        if(x1 is not None):
            if((x1 == gmove.srcx and y1 == gmove.srcy) or
               (x2 == gmove.srcx and y2 == gmove.srcy)):
                    continue
            piece1 = match.board.readfield(x1, y1)
            piece2 = match.board.readfield(x2, y2)
            if(match.color_of_piece(piece1) == match.color_of_piece(piece2)):
                continue
            if(match.color_of_piece(piece1) == color):
                frdlytouches, enmytouches = list_all_field_touches(match, x1, y1, color)
            else:
                frdlytouches, enmytouches = list_all_field_touches(match, x2, y2, color)
            enmytouches_before_count += len(enmytouches)

    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)

    for step in STEPS:
        stepx = step[0]
        stepy = step[1]
        x1, y1, x2, y2 = match.board.search_bi_dirs(gmove.dstx, gmove.dsty, stepx, stepy)
        if(x1 is not None):
            if((x1 == gmove.srcx and y1 == gmove.srcy) or
               (x2 == gmove.srcx and y2 == gmove.srcy)):
                    continue
            piece1 = match.board.readfield(x1, y1)
            piece2 = match.board.readfield(x2, y2)
            if(match.color_of_piece(piece1) == match.color_of_piece(piece2)):
                continue
            if(match.color_of_piece(piece1) == color):
                frdlytouches, enmytouches = list_all_field_touches(match, x1, y1, color)
            else:
                frdlytouches, enmytouches = list_all_field_touches(match, x2, y2, color)
            enmytouches_after_count += len(enmytouches)

    match.undo_move()

    if(enmytouches_after_count < enmytouches_before_count):
           return True
    else:
        return False


def running_pawn_in_endgame(gmove):
    if(gmove.match.is_endgame()):
        piece = gmove.match.board.readfield(gmove.srcx, gmove.srcy)
        if(piece == PIECES['wPw']):
            cpawn = cWhitePawn(gmove.match, gmove.srcx, gmove.srcy)
            return cpawn.is_running()
        elif(piece == PIECES['bPw']):
            cpawn = cBlackPawn(gmove.match, gmove.srcx, gmove.srcy)
            return cpawn.is_running()
    return False


def defends_invasion(match, gmove):
    piece = match.board.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)
    board =  [[0] * 8 for i in range(8)]

    for y in range(8):
        for x in range(8):
            piece = match.board.readfield(x, y)
            if(match.color_of_piece(piece) == COLORS['white']):
                board[y][x] += 1
            elif(match.color_of_piece(piece) == COLORS['black']):
                board[y][x] -= 1
   
    return False


def controles_file(gmove):
    match = gmove.match
    piece = match.board.readfield(gmove.srcx, gmove.srcy)

    if(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        cbishop = cBishop(match, gmove.srcx, gmove.srcy)
        return cbishop.move_controles_file(gmove.dstx, gmove.dsty)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        crook = cRook(match, gmove.srcx, gmove.srcy)
        return crook.move_controles_file(gmove.dstx, gmove.dsty)
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        cqueen = cQueen(match, gmove.srcx, gmove.srcy)
        return cqueen.move_controles_file(gmove.dstx, gmove.dsty)
    else:
        return False


def is_tactical_draw(gmove):
    newmatch = copy.deepcopy(gmove.match)
    newmatch.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
    
    if(newmatch.is_fifty_moves_rule()):
        return True

    if(len(newmatch.move_list) < 9):
        return False
    boards = []
    for i in range(9):
        str_board = ""
        for y in range(8):
            for x in range(8):
                piece = newmatch.board.readfield(x, y)
                str_board += reverse_lookup(PIECES, piece)
        boards.append(str_board)
        newmatch.undo_move()
    count = 0
    str_board = boards[0]
    for i in range(1, 9):
        if(boards[i] == str_board):
            count += 1
    return count >= 2


def is_progress(gmove):
    match = gmove.match
    if(match.is_opening()):
        piece = match.board.readfield(gmove.srcx, gmove.srcy)
        if(piece == PIECES['wPw']):
            if(gmove.srcy == match.board.RANKS['2'] and 
               gmove.srcx >= match.board.COLS['C'] and gmove.srcx <= match.board.COLS['F']):
                return True
        elif(piece == PIECES['bPw']):
            if(gmove.srcy == match.board.RANKS['7'] and 
               gmove.srcx >= match.board.COLS['C'] and gmove.srcx <= match.board.COLS['F']):
                return True
        elif(piece == PIECES['wKn']):
            if(gmove.srcy == match.board.RANKS['1'] and 
               (gmove.srcx == match.board.COLS['B'] or gmove.srcx == match.board.COLS['G'])):
                return True
        elif(piece == PIECES['bKn']):
            if(gmove.srcy == match.board.RANKS['8'] and 
               (gmove.srcx == match.board.COLS['B'] or gmove.srcx == match.board.COLS['G'])):
                return True
        elif(piece == PIECES['wBp']):
            if(gmove.srcy == match.board.RANKS['1'] and 
               (gmove.srcx == match.board.COLS['C'] or gmove.srcx == match.board.COLS['F'])):
                return True
        elif(piece == PIECES['bBp']):
            if(gmove.srcy == match.board.RANKS['8'] and 
               (gmove.srcx == match.board.COLS['C'] or gmove.srcx == match.board.COLS['F'])):
                return True
        return False
    else:
        return False


def rank_gmoves(match, pmoves, last_pmove, search_deep_check_mate, candidate, dbggmove, dbgprio):
    all_attacking = []
    all_supporting = []
    all_fork_defending = []
    all_fork_threatening = []
    all_discl_attacking = []
    all_discl_supporting = []
    all_fleeing = []
    all_running = []
    excludes = []

    for pmove in pmoves:
        gmove = pmove.gmove
        piece = match.board.readfield(gmove.srcx, gmove.srcy)
        cpiece = match.obj_for_piece(piece, gmove.srcx, gmove.srcy)
        dstpiece = match.board.readfield(gmove.dstx, gmove.dsty)
        frdlytouches_on_srcfield, enmytouches_on_srcfield = list_all_field_touches(match, gmove.srcx, gmove.srcy, match.color_of_piece(piece))
        frdlytouches_on_dstfield, enmytouches_on_dstfield = find_touches_on_dstfield_after_move(gmove)
        from_dstfield_supported, from_dstfield_attacked = find_touches_after_move(gmove)
        discl_supported, discl_attacked = find_disclosures(match, gmove)
        lowest_enemy_on_srcfield = lowest_piece(enmytouches_on_srcfield)
        lowest_enemy_on_dstfield = lowest_piece(enmytouches_on_dstfield)
        ###
        is_soft_pinned_before_mv, enemy_dir_before_mv = match.is_soft_pin(gmove.srcx, gmove.srcy)
        mv_dir = cpiece.dir_for_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)
        is_mv_within_soft_pinned_dirs = mv_dir = enemy_dir_before_mv or \
                                        REVERSE_DIRS[mv_dir] == enemy_dir_before_mv
        """match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
        is_soft_pinned_after_mv, enemy_dir_after_mv = match.is_soft_pin(gmove.dstx, gmove.dsty)
        match.undo_move()"""

        if(candidate):
            if(candidate.srcx == gmove.srcx and
               candidate.srcy == gmove.srcy and
               candidate.dstx == gmove.dstx and
               candidate.dsty == gmove.dsty and
               candidate.prompiece == gmove.prompiece):
                pmove.tactics.append(cTactic(pmove.TACTICS['prev-candidate'], pmove.SUB_TACTICS['good-deal']))

        if((PIECES_RANK[piece] <= PIECES_RANK[dstpiece] or lowest_enemy_on_dstfield is None) and 
           (is_soft_pinned_before_mv == False or is_mv_within_soft_pinned_dirs)):
            subtactic = pmove.SUB_TACTICS['better-deal']
        elif(lowest_enemy_on_dstfield is not None and 
             PIECES_RANK[piece] <= PIECES_RANK[lowest_enemy_on_dstfield] and
             len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield) and
             (is_soft_pinned_before_mv == False or is_mv_within_soft_pinned_dirs)):
            subtactic = pmove.SUB_TACTICS['good-deal']
        else:
            subtactic = pmove.SUB_TACTICS['bad-deal']
            
        if(defends_check(match)):
            pmove.tactics.append(cTactic(pmove.TACTICS['defends-check'], subtactic))

        if(castles(gmove)):
            match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
            cking = cKing(match, gmove.dstx, gmove.dsty)
            is_king_safe = cking.is_safe()
            match.undo_move()
            if(is_king_safe):
                pmove.tactics.append(cTactic(pmove.TACTICS['castles'], pmove.SUB_TACTICS['good-deal']))
            else:
                pmove.tactics.append(cTactic(pmove.TACTICS['castles'], pmove.SUB_TACTICS['bad-deal']))

        if(is_tactical_draw(gmove)):
            pmove.tactics.append(cTactic(pmove.TACTICS['is-tactical-draw'], pmove.SUB_TACTICS['good-deal']))

        if(promotes(gmove)):
            pmove.tactics.append(cTactic(pmove.TACTICS['promotes'], subtactic))

        if(captures(gmove)):
            if(exhausts_enemy(gmove)):
                captures_subtactic = min(subtactic, pmove.SUB_TACTICS['better-deal'])
            else:
                captures_subtactic = subtactic
            pmove.tactics.append(cTactic(pmove.TACTICS['captures'], captures_subtactic))

        if(does_unpin(gmove)):
            pmove.tactics.append(cTactic(pmove.TACTICS['unpins'], subtactic))

        if(forks(piece, from_dstfield_attacked)):
            pmove.tactics.append(cTactic(pmove.TACTICS['forks'], subtactic))

        if(defends_fork(gmove, piece, dstpiece)):
            pmove.tactics.append(cTactic(pmove.TACTICS['defends-fork'], subtactic))
            all_fork_defending.append(pmove)

        if(threatens_fork(gmove)):
            pmove.tactics.append(cTactic(pmove.TACTICS['threatens-fork'], subtactic))
            all_fork_threatening.append(pmove)

        if(flees(gmove)):
            flees_subtactic = subtactic
            if((subtactic == pmove.SUB_TACTICS['good-deal'] or subtactic == pmove.SUB_TACTICS['better-deal'])):
                if(lowest_enemy_on_srcfield is not None and 
                   PIECES_RANK[piece] > PIECES_RANK[lowest_enemy_on_srcfield]):
                    flees_subtactic = pmove.SUB_TACTICS['stormy']
                elif(len(frdlytouches_on_srcfield) == 0 and len(enmytouches_on_srcfield) > 0):
                    flees_subtactic = pmove.SUB_TACTICS['stormy']
            pmove.tactics.append(cTactic(pmove.TACTICS['flees'], flees_subtactic))
            all_fleeing.append(pmove)

        if(len(from_dstfield_attacked) > 0):
            for attacked in from_dstfield_attacked:
                if(attacked.piece == PIECES['wKg'] or 
                   attacked.piece == PIECES['bKg']):
                    if(search_deep_check_mate):
                        is_check_mate = check_mates_deep_search(gmove)
                    else:
                        is_check_mate = check_mates(gmove)
                    if(is_check_mate):
                        pmove.tactics.append(cTactic(pmove.TACTICS['attacks-king'], pmove.SUB_TACTICS['stormy']))
                    else:
                        """if(is_attacked_king_safe(match, piece) == False):
                            check_subtactic = min(subtactic, pmove.SUB_TACTICS['good-deal'])
                        else:
                            check_subtactic = subtactic"""
                        pmove.tactics.append(cTactic(pmove.TACTICS['attacks-king'], subtactic))
                elif((subtactic == pmove.SUB_TACTICS['good-deal'] or subtactic == pmove.SUB_TACTICS['better-deal'])):
                    if(PIECES_RANK[piece] <= PIECES_RANK[attacked.piece] or 
                       len(attacked.supporter_beyond) == 0 or 
                       match.is_soft_pin(attacked.fieldx, attacked.fieldy)[0]): 
                        pmove.tactics.append(cTactic(pmove.TACTICS['attacks'], pmove.SUB_TACTICS['stormy']))
                    elif(PIECES_RANK[piece] < PIECES_RANK[attacked.piece] and 
                         PIECES_RANK[piece] == PIECES_RANK[PIECES['wPw']] and
                         (len(frdlytouches_on_dstfield) > 0 or len(enmytouches_on_dstfield) == 0)): 
                        check_subtactic = min(subtactic, pmove.SUB_TACTICS['better-deal'])
                        pmove.tactics.append(cTactic(pmove.TACTICS['attacks'], check_subtactic))
                    else:
                        pmove.tactics.append(cTactic(pmove.TACTICS['attacks'], pmove.SUB_TACTICS['bad-deal']))
                else:
                    pmove.tactics.append(cTactic(pmove.TACTICS['attacks'], pmove.SUB_TACTICS['bad-deal']))
            all_attacking.append(pmove)

        if(len(from_dstfield_supported) > 0):
            for supported in from_dstfield_supported:
                if(is_supported_running_pawn(match, supported)):
                    support_tactic = pmove.TACTICS['supports-running-pawn']
                elif(len(supported.attacker_beyond) > 0):
                    support_tactic = pmove.TACTICS['supports']
                else:
                    support_tactic = pmove.TACTICS['supports-unattacked']

                if((subtactic == pmove.SUB_TACTICS['good-deal'] or subtactic == pmove.SUB_TACTICS['better-deal']) and 
                   len(supported.attacker_beyond) > 0 and
                   (is_supporter_lower_attacker(gmove, supported) or
                    match.is_soft_pin(supported.fieldx, supported.fieldy)[0])):
                    pmove.tactics.append(cTactic(support_tactic, pmove.SUB_TACTICS['stormy']))
                else:
                    pmove.tactics.append(cTactic(support_tactic, subtactic))
            all_supporting.append(pmove)

        if(len(discl_attacked) > 0):
            if((subtactic == pmove.SUB_TACTICS['good-deal'] or subtactic == pmove.SUB_TACTICS['better-deal']) and 
               is_discl_attacked_supported(discl_attacked) == False):
                pmove.tactics.append(cTactic(pmove.TACTICS['attacks'], pmove.SUB_TACTICS['stormy']))
            else:
                pmove.tactics.append(cTactic(pmove.TACTICS['attacks'], subtactic))
            all_discl_attacking.append(pmove)

        if(len(discl_supported) > 0):
            if((subtactic == pmove.SUB_TACTICS['good-deal'] or subtactic == pmove.SUB_TACTICS['better-deal']) and 
               is_discl_supported_weak(discl_supported)):
                pmove.tactics.append(cTactic(pmove.TACTICS['supports'], pmove.SUB_TACTICS['stormy']))
            else:
                pmove.tactics.append(cTactic(pmove.TACTICS['supports'], subtactic))
            all_discl_supporting.append(pmove)

        if(blocks(gmove)):
            pmove.tactics.append(cTactic(pmove.TACTICS['blocks'], subtactic))

        if(running_pawn_in_endgame(gmove)):
            if(len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield)):
                pmove.tactics.append(cTactic(pmove.TACTICS['is-running-pawn'], pmove.SUB_TACTICS['good-deal']))
            else:
                pmove.tactics.append(cTactic(pmove.TACTICS['is-running-pawn'], pmove.SUB_TACTICS['bad-deal']))
            all_running.append(pmove)

        if(controles_file(pmove.gmove)):
            pmove.tactics.append(cTactic(pmove.TACTICS['controles-file'], subtactic))

        if(is_progress(gmove)):
            pmove.tactics.append(cTactic(pmove.TACTICS['is-progress'], subtactic))

        if(len(pmove.tactics) > 0):
            pmove.evaluate_priorities(piece, dstpiece)
            
    all_attacking.sort(key=attrgetter('prio'))
    for pmove in all_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['attacks'])
            pmove.evaluate_priorities(piece, dstpiece)

    excludes.clear()
    all_discl_attacking.sort(key=attrgetter('prio'))
    for pmove in all_discl_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['attacks'])
            pmove.evaluate_priorities(piece, dstpiece)

    excludes.clear()
    all_supporting.sort(key=attrgetter('prio'))
    for pmove in all_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['supports'])
            pmove.evaluate_priorities(piece, dstpiece)

    excludes.clear()
    all_discl_supporting.sort(key=attrgetter('prio'))
    for pmove in all_discl_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['supports'])
            pmove.evaluate_priorities(piece, dstpiece)

    excludes.clear()
    all_fork_defending.sort(key=attrgetter('prio'))
    for pmove in all_fork_defending:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['defends-fork'])
            pmove.evaluate_priorities(piece, dstpiece)

    excludes.clear()
    all_fork_threatening.sort(key=attrgetter('prio'))
    for pmove in all_fork_threatening:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['threatens-fork'])
            pmove.evaluate_priorities(piece, dstpiece)

    excludes.clear()
    all_fleeing.sort(key=attrgetter('prio'))
    for pmove in all_fleeing:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['flees'])
            pmove.evaluate_priorities(piece, dstpiece)

    """excludes.clear()
    all_running.sort(key=attrgetter('prio'))
    for pmove in all_running:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['is-running-pawn'])
            pmove.evaluate_priorities()"""

    if(dbggmove):
        for pmove in pmoves:
            if(pmove.gmove.srcx == dbggmove.srcx and 
               pmove.gmove.srcy == dbggmove.srcy and 
               pmove.gmove.dstx == dbggmove.dstx and 
               pmove.gmove.dsty == dbggmove.dsty):
                pmove.prio = dbgprio
                break
    pmoves.sort(key=attrgetter('prio'))
