
import time
from operator import attrgetter

from .match import *
from .move import *
from .openings import retrieve_move
from .analyze_move import *
from .analyze_position import score_position
from .helper import *
from .generator import cGenerator


def prnt_before_calc(match, count, priomove):
    print("\n***********************************************")
    print("count: " + str(count))
    print("calculate: " + priomove.gmove.format_genmove())
    print("tactics: " + priomove.concat_tactics(" | "))
    print("priority: " + str(priomove.prio))
    print("***********************************************")


def prnt_search(match, label, score, gmove, candidates):
    if(gmove):
        str_gmove = " [" + gmove.format_genmove() + "] "
    else:
        str_gmove = ""
    print(label + str(score).rjust(8, " ") + str_gmove + concat_fmt_gmoves(match, candidates))


def concat_fmt_gmoves(match, gmoves):
    str_gmoves = ""
    for gmove in gmoves:
        if(gmove):
            str_gmoves += " [" + gmove.format_genmove() + "] "
    return str_gmoves


def prnt_priomoves(match, priomoves, last_pmove):
    is_exchange = resort_exchange_or_stormy_moves(priomoves, 0, last_pmove, True)
    print("------------------------------------------------")
    print("is_exchange: " + str(is_exchange))
    idx = 1
    for priomove in priomoves:
        print(str(idx), end=".")
        """if(priomove.prio <= cPrioMove.PRIO['prio0']):
            print("----------prio0---------------------------------")
        elif(priomove.prio <= cPrioMove.PRIO['prio1']):
            print("----------prio1---------------------------------")
        elif(priomove.prio <= cPrioMove.PRIO['prio2']):
            print("----------prio2---------------------------------")
        elif(priomove.prio <= cPrioMove.PRIO['prio3']):
            print("----------prio3---------------------------------")
        else:
            print("----------> prio3--------------------------------")"""
        print(priomove.gmove.format_genmove() + " prio: " + str(priomove.prio) + " is_tactic_stormy: " + str(priomove.is_tactic_stormy()))
        priomove.prnt_tactics()
        idx += 1


def prnt_fmttime(msg, seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    print( msg + "%02d:%02d:%02d" % (hour, minute, sec))


class SearchLimits:
    def __init__(self, match):
        self.add_mvcnt = 2
        self.dpth_max = 20
        if(match.level == match.LEVELS['blitz']):
            self.dpth_stage1 = 2
            self.dpth_stage2 = 5
            self.dpth_stage3 = 8
            self.mvcnt_stage1 = 4
            self.mvcnt_stage2 = 3
            self.mvcnt_stage3 = 2
        elif(match.level == match.LEVELS['low']):
            self.dpth_stage1 = 2
            self.dpth_stage2 = 5
            self.dpth_stage3 = 8
            self.mvcnt_stage1 = 8
            self.mvcnt_stage2 = 5
            self.mvcnt_stage3 = 3
        elif(match.level == match.LEVELS['medium']):
            self.dpth_stage1 = 3
            self.dpth_stage2 = 6
            self.dpth_stage3 = 10
            self.mvcnt_stage1 = 10
            self.mvcnt_stage2 = 4
            self.mvcnt_stage3 = 2
        else: # high
            self.dpth_stage1 = 4
            self.dpth_stage2 = 6
            self.dpth_stage3 = 10
            self.mvcnt_stage1 = 12
            self.mvcnt_stage2 = 6
            self.mvcnt_stage3 = 4

        if(match.is_endgame()):
            if(match.board.wQu_cnt == 0 and match.board.bQu_cnt == 0):
                self.dpth_stage1 += 1
                self.dpth_stage2 += 1

# class end


def append_newmove(gmove, candidates, newcandidates):
    candidates.clear()
    candidates.append(gmove)
    for newcandidate in newcandidates:
        if(newcandidate):
            candidates.append(newcandidate)
        else:
            break


def count_up_to_prio(priomoves, prio_limit):
    count = 0
    for priomove in priomoves:
        if(priomove.prio <= prio_limit):
            count += 1
    return count


def resort_exchange_or_stormy_moves(priomoves, new_prio, last_pmove, only_exchange):
    if(only_exchange and last_pmove is not None and last_pmove.has_domain_tactic(cPrioMove.TACTICS['captures']) == False):
        return False
    if(last_pmove is not None and last_pmove.has_tactic_ext(cTactic(cPrioMove.TACTICS['captures'], cPrioMove.SUB_TACTICS['bad-deal']))):
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
        elif(priomove.has_domain_tactic(cPrioMove.TACTICS['captures'])):
            subtactic = priomove.fetch_subtactic(cPrioMove.TACTICS['captures'])
            if(subtactic > cPrioMove.SUB_TACTICS['bad-deal']):
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


def select_maxcount(match, priomoves, depth, slimits, last_pmove):
    if(len(priomoves) == 0 or depth > slimits.dpth_max):
        return 0
    if(depth <= slimits.dpth_stage1 and priomoves[0].has_domain_tactic(cPrioMove.TACTICS['defends-check'])):
        return len(priomoves)

    if(depth <= slimits.dpth_stage1):
        resort_exchange_or_stormy_moves(priomoves, cPrioMove.PRIO['prio1'], last_pmove, False)
        count = count_up_to_prio(priomoves, cPrioMove.PRIO['prio2'])
        return min(slimits.mvcnt_stage1, count)
    elif(depth <= slimits.dpth_stage2):
        resort_exchange_or_stormy_moves(priomoves, cPrioMove.PRIO['prio1'], last_pmove, False)
        count = count_up_to_prio(priomoves, cPrioMove.PRIO['prio1'])
        return min(slimits.mvcnt_stage2, count)
    else:
        if(resort_exchange_or_stormy_moves(priomoves, cPrioMove.PRIO['prio0'], last_pmove, True)):
            count = count_up_to_prio(priomoves, cPrioMove.PRIO['prio0'])
            if(depth <= slimits.dpth_stage3):
                return count
            else:
                return min(slimits.mvcnt_stage3, count)
                #return min(2, count)
        else:
            return 0


def alphabeta(match, depth, slimits, alpha, beta, maximizing, last_pmove, candidate):
    color = match.next_color()
    candidates = []
    newcandidates = []
    count = 0
    starttime = time.time()

    if(maximizing):
        maxscore = alpha
    else:
        minscore = beta

    cgenerator = cGenerator(match)
    priomoves = cgenerator.generate_priomoves()
    #gmove = cGenMove(match, 1, 7, 3, 6, None)
    search_deep_check_mate = depth <= slimits.dpth_stage1
    rank_gmoves(match, priomoves, last_pmove, search_deep_check_mate, candidate, None, 1)
    maxcnt = select_maxcount(match, priomoves, depth, slimits, last_pmove)

    if(depth == 1):
        print("************ maxcnt: " + str(maxcnt) + " ******************")
        prnt_priomoves(match, priomoves, last_pmove)
        if(len(priomoves) == 1):
            pmove = priomoves[0]
            candidates.append(pmove.gmove)
            candidates.append(None)
            if(pmove.has_domain_tactic(cPrioMove.TACTICS['is-tactical-draw'])):
                return 0, candidates
            else:
                return score_position(match, len(priomoves)), candidates

    if(len(priomoves) == 0 or maxcnt == 0):
        candidates.append(None)
        return score_position(match, len(priomoves)), candidates
        
    for priomove in priomoves:
        gmove = priomove.gmove
        count += 1

        if(depth == 1):
            prnt_before_calc(match, count, priomove)
        if(depth == 2):
            print("calculate 2nd: " + priomove.gmove.format_genmove())

        if(priomove.has_domain_tactic(cPrioMove.TACTICS['is-tactical-draw'])):
            newcandidates.clear()
            newcandidates.append(None)
            newscore = 0
        else:
            match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prompiece)
            if(maximizing):
                newscore, newcandidates = alphabeta(match, depth + 1, slimits, maxscore, beta, False, priomove, None)
            else:
                newscore, newcandidates = alphabeta(match, depth + 1, slimits, alpha, minscore, True, priomove, None)
            match.undo_move()

        if(maximizing):
            if(depth == 1):
                prnt_search(match, "CURRENT SEARCH: ", newscore, gmove, newcandidates)
                if(candidates):
                    prnt_search(match, "CANDIDATE:      ", maxscore, None, candidates)
            if(newscore > maxscore):
                maxscore = newscore
                if(maxscore >= beta):
                    break # beta cut-off
                else:
                    append_newmove(gmove, candidates, newcandidates)
                    if(depth == 1):
                        prnt_search(match, "new CANDIDATE:  ", maxscore, None, candidates)
        else:
            if(depth == 1):
                prnt_search(match, "CURRENT SEARCH: ", newscore, gmove, newcandidates)
                if(candidates):
                    prnt_search(match, "CANDIDATE:      ", minscore, None, candidates)
            if(newscore < minscore):
                minscore = newscore
                if(minscore <= alpha):
                    break # alpha cut-off
                else:
                    append_newmove(gmove, candidates, newcandidates)
                    if(depth == 1):
                        prnt_search(match, "new CANDIDATE:  ", minscore, None, candidates)
        if(depth == 1):
            if(color == COLORS['white']):
                huge_diff = maxscore < match.score + (SCORES[PIECES['wPw']] * 2)
            else:
                huge_diff = minscore > match.score + (SCORES[PIECES['bPw']] * 2)
            exceeded = False
        else:
            huge_diff = False
            exceeded = False
        if(huge_diff and exceeded == False and count < maxcnt + slimits.add_mvcnt):
            continue
        if(count >= maxcnt):
            break

    if(maximizing):
        return maxscore, candidates
    else:
        return minscore, candidates


def calc_move(match, candidate):
    print("movecnt " + str(match.movecnt()))
    if(match.is_opening()):
        msg = "is opening"
    elif(match.is_endgame()):
        msg = "is endgame"
    else:
        msg = "is middlegame"
    print(msg)

    candidates = []
    slimits = SearchLimits(match)
    time_start = time.time()
    gmove = None

    if(match.is_opening()):
        gmove = retrieve_move(match)

    if(gmove):
        candidates.append(gmove)
        score = match.score
    else:
        maximizing = match.next_color() == COLORS['white']
        alpha = SCORES[PIECES['wKg']] * 10
        beta = SCORES[PIECES['bKg']] * 10 
        score, candidates = alphabeta(match, 1, slimits, alpha, beta, maximizing, None, candidate)

    msg = "result: " + str(score) + " match: " + str(match.created_at) + " "
    print(msg + concat_fmt_gmoves(match, candidates))

    prnt_fmttime("\ncalc-time: ", time.time() - time_start)

    return candidates

