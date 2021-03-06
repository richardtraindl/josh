
import multiprocessing as mp
import random, time, copy
from operator import attrgetter

from ..values import *
from ..move import cPrioMove, cTactic
from .openings import retrieve_move
from .analyze_position import *


def prnt_priomoves(match, priomoves):
    print("------------------------------------------------")
    idx = 1
    for priomove in priomoves:
        print(str(idx), end=".")
        print(priomove.move.format() + " prio: " + str(priomove.prio) + " is_tactic_stormy: " + str(priomove.is_tactic_stormy()))
        print(priomove.concat_fmttactics())
        idx += 1
    print("------------------------------------------------")


def prnt_search(match, label, score, move, candidates):
    if(move):
        str_gmove = " [" + move.format() + "] "
    else:
        str_gmove = ""
    print(label + str(score).rjust(8, " ") + str_gmove + concat_fmtmoves(match, candidates))


def concat_fmtmoves(match, moves):
    str_gmoves = ""
    for move in moves:
        if(move):
            str_moves += " [" + move.format() + "] "
    return str_moves


def generate_moves(match, candidate, dbggmove, search_for_mate, mode):
    color = match.next_color()
    moves = []
    #for idx in range(64):
    fields = match.board.fields
    for idx in range(63, -1, -1):
        piece = fields & 0xF
        fields = fields >> 4
        #piece = match.board.getfield(idx)
        if(piece == PIECES['blk'] or color != match.color_of_piece(piece)):
            continue
        else:
            cpiece = match.obj_for_piece(piece, idx)
            piecemoves = cpiece.generate_moves(candidate, dbggmove, search_for_mate, mode)
            if(len(piecemoves) > 0):
                moves.extend(piecemoves)
    return moves


def append_newmove(move, candidates, newcandidates):
    candidates.clear()
    candidates.append(move)
    for newcandidate in newcandidates:
        if(newcandidate):
            candidates.append(newcandidate)
        else:
            break


def alphabeta(match, depth, slimits, alpha, beta, maximizing, last_pmove, candidate):
    color = match.next_color()
    candidates = []
    newcandidates = []
    count = 0
    starttime = time.time()

    if(maximizing):
        bestscore = SCORES[PIECES['wKg']] * 10
    else:
        bestscore = SCORES[PIECES['bKg']] * 10

    dbggmove = cMove(None, 3, 51, PIECES['blk'])
    search_for_mate = match.is_endgame()
    priomoves = generate_moves(match, candidate, dbggmove, search_for_mate, True)
    priomoves.sort(key = attrgetter('prio'))
    maxcnt = select_movecnt(match, priomoves, depth, slimits, last_pmove)

    if(len(priomoves) == 0 or maxcnt == 0):
        return score_position(match, len(priomoves)), candidates

    if(depth == 1):
        prnt_priomoves(match, priomoves)

    for priomove in priomoves:
        move = priomove.move
        count += 1

        if(depth == 1):
            print("CURRENT SEARCH: " + priomove.move.format())

        match.do_move(move.src, move.dst, move.prompiece)
        newscore, newcandidates = alphabeta(match, depth + 1, slimits, alpha, beta, not maximizing, priomove, None)
        match.undo_move()

        if(maximizing):
            if(newscore > bestscore):
                bestscore = newscore
                append_newmove(move, candidates, newcandidates)
                if(depth == 1):
                    if(candidates):
                        prnt_search(match, "CANDIDATE:      ", bestscore, None, candidates)
                alpha = max(alpha, bestscore)
                if(bestscore >= beta):
                    break # beta cut-off
        else:
            if(newscore < bestscore):
                bestscore = newscore
                append_newmove(move, candidates, newcandidates)
                if(depth == 1):
                    if(candidates):
                        prnt_search(match, "CANDIDATE:      ", bestscore, None, candidates)
                beta = min(beta, bestscore)
                if(bestscore <= alpha):
                    break # alpha cut-off
        if(count >= maxcnt):
            break

    return bestscore, candidates


class SearchLimits:
    def __init__(self, match):
        self.add_mvcnt = 2
        if(match.level == match.LEVELS['blitz']):
            self.dpth_max = 8
            self.dpth_stage1 = 2
            self.dpth_stage2 = 4
            #self.dpth_stage3 = 4
            self.mvcnt_stage1 = 8
            self.mvcnt_stage2 = 6
            #self.mvcnt_stage3 = 2
        if(match.level == match.LEVELS['low']):
            self.dpth_max = 12
            self.dpth_stage1 = 2
            self.dpth_stage2 = 5
            #self.dpth_stage3 = 6
            self.mvcnt_stage1 = 10
            self.mvcnt_stage2 = 6
            #self.mvcnt_stage3 = 2
        elif(match.level == match.LEVELS['medium']):
            self.dpth_max = 16
            self.dpth_stage1 = 2
            self.dpth_stage2 = 6
            #self.dpth_stage3 = 8
            self.mvcnt_stage1 = 10
            self.mvcnt_stage2 = 6
            #self.mvcnt_stage3 = 3
        elif(match.level == match.LEVELS['high']):
            self.dpth_max = 20
            self.dpth_stage1 = 3
            self.dpth_stage2 = 6
            #self.dpth_stage3 = 8
            self.mvcnt_stage1 = 12
            self.mvcnt_stage2 = 6
            #self.mvcnt_stage3 = 3

        if(match.is_endgame()):
            self.dpth_stage1 += 2
            self.dpth_stage2 += 1
# class end


def count_up_to_prio(priomoves, priolimit):
    count = 0
    for priomove in priomoves:
        if(priomove.prio <= priolimit or priomove.is_tactic_stormy()):
            count += 1
        else:
            break
    return count


def count_up_within_stormy(priomoves):
    count = 0
    for priomove in priomoves:
        if(priomove.is_tactic_stormy()):
            count += 1
        else:
            break
    return count


def resort_exchange_or_stormy_moves(priomoves, new_prio, last_pmove, only_exchange):
    if(only_exchange and last_pmove is not None and 
       last_pmove.has_domain(cTactic.DOMAINS['captures']) == False):
        return False
    if(last_pmove is not None and 
       last_pmove.has_tactic_ext(cTactic(cTactic.DOMAINS['captures'], cTactic.WEIGHTS['bad-deal']))):
        last_pmove_capture_bad_deal = True
    else:
        last_pmove_capture_bad_deal = False
    count_of_stormy = 0
    count_of_good_captures = 0
    first_silent = None
    bad_captures = []
    for priomove in priomoves:
        if(only_exchange == False and priomove.is_tactic_stormy()):
            count_of_stormy += 1
            priomove.prio = min(priomove.prio, (new_prio + priomove.prio % 10) - 13)
        elif(priomove.has_domain(cTactic.DOMAINS['captures'])):
            weight = priomove.fetch_weight(cTactic.DOMAINS['captures'])
            if(weight > cTactic.WEIGHTS['bad-deal']):
                count_of_good_captures += 1
                priomove.prio = min(priomove.prio, (new_prio  + priomove.prio % 10) - 12)
            elif(last_pmove_capture_bad_deal):
                bad_captures.append(priomove)
                #count_of_bad_captures += 1
                #priomove.prio = min(priomove.prio, new_prio)
        elif(first_silent is None):
            first_silent = priomove
    if(len(bad_captures) > 0 and count_of_good_captures == 0 and count_of_stormy == 0):
        if(first_silent):
            first_silent.prio = min(first_silent.prio, (new_prio + first_silent.prio % 10) - 10)
        for capture in bad_captures:
            capture.prio = min(capture.prio, new_prio + capture.prio % 10)
    priomoves.sort(key=attrgetter('prio'))
    return True


def select_movecnt(match, priomoves, depth, slimits, last_pmove):
    if(len(priomoves) == 0 or depth > slimits.dpth_max):
        return 0
    if(depth <= slimits.dpth_stage1 and priomoves[0].has_domain(cTactic.DOMAINS['defends-check'])):
        return len(priomoves)

    stormycnt = count_up_within_stormy(priomoves)
    if(depth <= slimits.dpth_stage1):
        resort_exchange_or_stormy_moves(priomoves, cPrioMove.PRIOS['prio1'], last_pmove, False)
        count = count_up_to_prio(priomoves, cPrioMove.PRIOS['prio2'])
        if(count == 0):
            count = slimits.mvcnt_stage1
        else:
            count = min(count, slimits.mvcnt_stage1)
        return max(stormycnt, count)
    elif(depth <= slimits.dpth_stage2):
        resort_exchange_or_stormy_moves(priomoves, cPrioMove.PRIOS['prio1'], last_pmove, False)
        count = count_up_to_prio(priomoves, cPrioMove.PRIOS['prio2'])
        if(count == 0):
            count = slimits.mvcnt_stage2
        else:
            count = min(count, slimits.mvcnt_stage2)
        return max(stormycnt, count)
        """elif(depth <= slimits.dpth_stage3):
        resort_exchange_or_stormy_moves(priomoves, cPrioMove.PRIOS['prio0'], last_pmove, False)
        count = count_up_to_prio(priomoves, cPrioMove.PRIOS['prio0'])
        if(count == 0):
            count = slimits.mvcnt_stage3
        else:
            count = min(count, slimits.mvcnt_stage3)
        return max(stormycnt, count)"""
    else:
        if(resort_exchange_or_stormy_moves(priomoves, cPrioMove.PRIOS['prio0'], last_pmove, True)):
            return count_up_to_prio(priomoves, cPrioMove.PRIOS['prio0'])
            #return min(slimits.mvcnt_stage3, count)
            #return min(2, count)
        else:
            return 0


def concat_fmtmoves(match, moves):
    str_moves = ""
    for move in moves:
        if(move):
            str_moves += " [" + move.format() + "] "
    return str_moves

def prnt_fmttime(msg, seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    print( msg + "%02d:%02d:%02d" % (hour, minute, sec))


def calc_move(match, candidate):
    time_start = time.time()
    move = retrieve_move(match)
    candidates = []

    if(move):
        candidates.append(move)
        score = match.score
    else:
        slimits = SearchLimits(match)
        maximizing = match.next_color() == COLORS['white']
        alpha = SCORES[PIECES['wKg']] * 10
        beta = SCORES[PIECES['bKg']] * 10
        score, candidates = alphabeta(match, 1, slimits, alpha, beta, maximizing, None, candidate)

    msg = "result: " + str(score) + " match: " + str(match.created_at) + " "
    print(msg + concat_fmtmoves(match, candidates))
    prnt_fmttime("\ncalc-time: ", time.time() - time_start)
    return candidates

