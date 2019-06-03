
from ..match import *
from ..move import *
from .tactics_helper import *
from .weights_helper import *


class cExcluded:
    def __init__(self, priomove, tactic, prio=None):
        self.priomove = priomove
        self.tactic = tactic
# class end


def add_tactics(priomove, match, candidate, dbggmove, search_for_mate):
    excludes = []
    move = priomove.move
    piece = match.board.getfield(move.src)
    dstpiece = match.board.getfield(move.dst)
    from_dstfield_supported, from_dstfield_attacked = find_touches_after_move(match, move)
    discl_supported, discl_attacked = find_disclosures(match, move)

    weight = weight_for_standard(match, move)

    if(candidate):
        if(candidate.src == move.src and candidate.dst == move.dst and candidate.prompiece == move.prompiece):
            priomove.tactics.append(cTactic(cTactic.DOMAINS['prev-candidate'], cTactic.WEIGHTS['good-deal']))

    if(defends_check(match)):
        priomove.tactics.append(cTactic(cTactic.DOMAINS['defends-check'], weight))

    if(castles(match, move)):
        priomove.tactics.append(cTactic(cTactic.DOMAINS['castles'], weight))

    if(is_tactical_draw(match, move)):
        priomove.tactics.append(cTactic(cTactic.DOMAINS['is-tactical-draw'], cTactic.WEIGHTS['good-deal']))

    if(promotes(move)):
        priomove.tactics.append(cTactic(cTactic.DOMAINS['promotes'], weight))

    if(captures(match, move)):
        capture_weight = weight_for_capture(match, move, weight)
        priomove.tactics.append(cTactic(cTactic.DOMAINS['captures'], capture_weight))

    if(does_unpin(match , move)):
        priomove.tactics.append(cTactic(cTactic.DOMAINS['unpins'], weight))

    if(forks(piece, from_dstfield_attacked)):
        priomove.tactics.append(cTactic(cTactic.DOMAINS['forks'], weight))

    if(defends_fork(match, move, piece, dstpiece)):
        tactic = cTactic(cTactic.DOMAINS['defends-fork'], weight)
        priomove.tactics.append(tactic)
        excludes.append(cExcluded(priomove, tactic))

    if(threatens_fork(match, move)):
        tactic = cTactic(cTactic.DOMAINS['threatens-fork'], weight)
        priomove.tactics.append(tactic)
        excludes.append(cExcluded(priomove, tactic))

    if(flees(match, move)):
        flee_weight = weight_for_flee(match, move, weight)
        tactic = cTactic(cTactic.DOMAINS['flees'], flee_weight, move.src)
        priomove.tactics.append(tactic)
        excludes.append(cExcluded(priomove, tactic))

    if(len(from_dstfield_attacked) > 0):
        for attacked in from_dstfield_attacked:
            if(attacked.piece == PIECES['wKg'] or attacked.piece == PIECES['bKg']):
                if(search_for_mate):
                    attacking_weight = weight_for_attacking_king(match, move, weight)
                else:
                    attacking_weight = weight
                tactic = cTactic(cTactic.DOMAINS['attacks-king'], attacking_weight, attacked.field)
                priomove.tactics.append(tactic)
                excludes.append(cExcluded(priomove, tactic))
            else:
                attacking_weight = weight_for_attacking(match, move, attacked, weight)
                tactic = cTactic(cTactic.DOMAINS['attacks'], attacking_weight, attacked.field)
                priomove.tactics.append(tactic)
                excludes.append(cExcluded(priomove, tactic))

    if(len(from_dstfield_supported) > 0):
        for supported in from_dstfield_supported:
            if(is_supported_running_pawn(match, supported)):
                supporting_tactic = cTactic.DOMAINS['supports-running-pawn']
            elif(len(supported.attacker_beyond) > 0):
                supporting_tactic = cTactic.DOMAINS['supports']
            else:
                continue
            ###
            supporting_weight = weight_for_supporting(match, move, supported, weight)
            tactic = cTactic(supporting_tactic, supporting_weight, supported.field)
            priomove.tactics.append(tactic)
            excludes.append(cExcluded(priomove, tactic))

    if(len(discl_attacked) > 0):
        for dattd in discl_attacked:
            discl_attacking_weight = weight_for_discl_attacked(dattd, weight)
            tactic = cTactic(cTactic.DOMAINS['attacks'], discl_attacking_weight, dattd.field)
            priomove.tactics.append(tactic)        
            excludes.append(cExcluded(priomove, tactic))

    if(len(discl_supported) > 0):
        for dsuppd in discl_supported:
            discl_supporting_weight = weight_for_discl_supported(dsuppd, weight)
            tactic = cTactic(cTactic.DOMAINS['supports'], discl_supporting_weight, dsuppd.field)
            priomove.tactics.append(tactic)
            excludes.append(cExcluded(priomove, tactic))

    if(blocks(match, move)):
        priomove.tactics.append(cTactic(cTactic.DOMAINS['blocks'], weight))

    if(running_pawn_in_endgame(match, move)):
        running_weight = weight_for_running_pawn(match, move, weight)
        priomove.tactics.append(cTactic(cTactic.DOMAINS['is-running-pawn'], running_weight))

    if(controles_file(match, move)):
        priomove.tactics.append(cTactic(cTactic.DOMAINS['controles-file'], weight))

    if(is_progress(match, move)):
        priomove.tactics.append(cTactic(cTactic.DOMAINS['is-progress'], weight))

    if(dbggmove and dbggmove.src == move.src and dbggmove.dst == move.dst):
        priomove.prio = 1
        excludes.clear()
        return excludes

    priomove.evaluate_priority()

    return excludes

