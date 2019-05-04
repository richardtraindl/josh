
from .values import *
from .helper import reverse_lookup, index_to_coord


class cMove:
    def __init__(self, match=None, count=None, srcx=None, srcy=None, dstx=None, dsty=None, \
                 enpassx=None, enpassy=None, srcpiece=None, captpiece=None, prompiece=None):
        self.match = match
        self.count = count
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.enpassx = enpassx
        self.enpassy = enpassy
        self.srcpiece = srcpiece
        self.captpiece = captpiece
        self.prompiece = prompiece

    def is_castling(self):
        if((self.srcpiece == PIECES['wKg'] or self.srcpiece == PIECES['bKg']) and 
           abs(self.srcx - self.dstx) > 1):
            return True
        else:
            return False

    def format_move(self):
        if(self.is_castling()):
            if(self.dstx == 6):
                return "0-0"
            else:
                return "0-0-0"
        elif(self.prompiece):
            if(self.captpiece == PIECES['blk']):
                hyphen = "-"
            else:
                hyphen = "x"
            fmtmove = index_to_coord(self.srcx, self.srcy) + hyphen + \
                      index_to_coord(self.dstx, self.dsty) + " " + \
                      reverse_lookup(PIECES, self.prompiece)
            return fmtmove
        elif(self.enpassx and self.enpassy):
            fmtmove = index_to_coord(self.srcx, self.srcy) + "x" + \
                      index_to_coord(self.dstx, self.dsty) + " e.p."
            return fmtmove
        else:
            if(self.captpiece == PIECES['blk']):
                hyphen = "-"
            else:
                hyphen = "x"
            fmtmove = index_to_coord(self.srcx, self.srcy) + hyphen + \
                      index_to_coord(self.dstx, self.dsty)
            return fmtmove
            
    def prnt_move(self, headmsg, tailmsg):
        print(headmsg + 
            index_to_coord(self.srcx, self.srcy) + "-" +
            index_to_coord(self.dstx, self.dsty), end="")

        if(self.prompiece != PIECES['blk']):
            print(" " + reverse_lookup(PIECES, self.prompiece), end="")
        print(tailmsg, end="")

# class end


class cGenMove(object):
    def __init__(self, match=None, srcx=None, srcy=None, dstx=None, dsty=None, prompiece=None):
        self.match = match
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.prompiece = prompiece

    def format_genmove(self):
        piece = self.match.board.readfield(self.srcx, self.srcy)
        dstpiece = self.match.board.readfield(self.dstx, self.dsty)
        hyphen = "-"

        if(self.prompiece and self.prompiece != PIECES['blk']):
            trailing = ", " + reverse_lookup(PIECES, self.prompiece)
        else:
            trailing = ""

        fmtmove = index_to_coord(self.srcx, self.srcy) + \
                  hyphen + \
                  index_to_coord(self.dstx, self.dsty) + \
                  trailing
        return fmtmove

# class end


class cTactic:
    def __init__(self, tactic=None, subtactic=None):
        self.tactic = tactic
        self.subtactic = subtactic
# class end

class cPrioMove:
    PRIO = {
        'prio0' : 100,
        'prio1' : 150,
        'prio2' : 200,
        'prio3' : 250 }

    TACTICS = {
        'defends-check' :         10,
        'captures' :              20,
        'attacks-king' :          30,
        'attacks' :               40,
        'supports' :              50,
        'supports-running-pawn' : 60,
        'supports-unattacked' :   70,
        'flees' :                 80,
        'forks' :                 90,
        'threatens-fork' :        100,
        'defends-fork' :          110,
        'unpins' :                120,
        'blocks' :                130,
        'promotes' :              140, 
        'is-tactical-draw' :      150,
        'prev-candidate' :        160,
        'is-running-pawn' :       170, 
        'controles-file' :        180,
        'castles' :               190,
        'is-progress' :           200,
        'is-undefined' :          210 }

    SUB_TACTICS = {
        'stormy' : 1,
        'better-deal' : 2,
        'good-deal' : 3,
        'downgraded' : 4,
        'upgraded' : 5,
        'bad-deal' : 6 }

    TACTICS_TO_PRIO = {
        ### level 1 ###
        TACTICS['promotes'] :               90,
        TACTICS['captures'] :               91,
        TACTICS['is-running-pawn'] :        92,
        TACTICS['is-tactical-draw'] :       93,
        TACTICS['defends-check']  :         94,
        TACTICS['prev-candidate']  :        95,
        ### level 2 ###
        TACTICS['castles'] :                200,
        TACTICS['attacks-king'] :           201,
        TACTICS['forks'] :                  202, 
        TACTICS['threatens-fork'] :         203,
        TACTICS['defends-fork'] :           204, 
        TACTICS['unpins'] :                 205, 
        TACTICS['supports-running-pawn'] :  206, 
        TACTICS['flees'] :                  207, 
        TACTICS['blocks'] :                 208,
        TACTICS['controles-file'] :         209, 
        TACTICS['is-progress'] :            210,
        TACTICS['supports'] :               211,
        TACTICS['attacks'] :                212,
        TACTICS['supports-unattacked'] :    213,
        ### level 3 ###
        TACTICS['is-undefined'] :           500 }

    SUB_TACTICS_TO_ADJUST = {
        SUB_TACTICS['stormy'] : -70,
        SUB_TACTICS['better-deal'] : -10,
        SUB_TACTICS['good-deal'] : 0,
        SUB_TACTICS['upgraded'] : 0,
        SUB_TACTICS['downgraded'] : 60,
        SUB_TACTICS['bad-deal'] : 130 }

    def __init__(self, gmove=None, prio=PRIO['prio3']):
        self.gmove = gmove
        self.tactics = []
        self.prio = prio

    def evaluate_priorities(self, piece, dstpiece):
        count = 0
        self.prio = self.PRIO['prio3']
        if(self.tactics):
            for tactitem in self.tactics:
                if(tactitem.tactic == self.TACTICS['captures']):
                    adjust = PIECES_RANK[piece] + (PIECES_RANK[dstpiece] * -1)
                else:
                    adjust = 0
                prio_new = self.TACTICS_TO_PRIO[tactitem.tactic] + \
                           self.SUB_TACTICS_TO_ADJUST[tactitem.subtactic] + \
                           adjust
                self.prio = min(self.prio, prio_new)
                if(tactitem.subtactic <= self.SUB_TACTICS['downgraded']):
                    count += 2
            self.prio -= count

    def downgrade(self, domain_tactic):
        for tactic in self.tactics:
            if(tactic.tactic == domain_tactic):
                if(tactic.subtactic == self.SUB_TACTICS['stormy'] or
                   tactic.subtactic == self.SUB_TACTICS['better-deal'] or
                   tactic.subtactic == self.SUB_TACTICS['good-deal']):
                    tactic.subtactic = self.SUB_TACTICS['downgraded']
                return

    def upgrade(self, domain_tactic):
        for tactic in self.tactics:
            if(tactic.tactic == domain_tactic):
                if(tactic.subtactic != self.SUB_TACTICS['stormy'] and 
                   tactic.subtactic != self.SUB_TACTICS['better-deal'] and 
                   tactic.subtactic != self.SUB_TACTICS['good-deal']):
                    tactic.subtactic = self.SUB_TACTICS['upgraded']
                    return

    def fetch_subtactic(self, domain_tactic):
        for tactitem in self.tactics:
            if(tactitem.tactic == domain_tactic):
                return tactitem.subtactic
        return None

    def has_domain_tactic(self, domain_tactic):
        for tactitem in self.tactics:
            if(tactitem.tactic == domain_tactic):
                return True
        return False

    def has_subtactic(self, subtactic):
        for tactitem in self.tactics:
            if(tactitem.subtactic == subtactic):
                return True
        return False

    def has_tactic_ext(self, tactic):
        for tactitem in self.tactics:
            if(tactitem.tactic == tactic.tactic and tactitem.subtactic == tactic.subtactic):
                return True
        return False

    def is_tactic_stormy(self):
        for tactitem in self.tactics:
            if(tactitem.subtactic == self.SUB_TACTICS['stormy'] or
               ((tactitem.tactic == self.TACTICS['promotes'] or
                 tactitem.tactic == self.TACTICS['captures']) and 
                (tactitem.subtactic == self.SUB_TACTICS['better-deal'] or
                 tactitem.subtactic == self.SUB_TACTICS['good-deal']))):
                return True
        return False

    def concat_tactics(self, delimiter):
        str_tactics = ""
        length = len(self.tactics)
        i = 1
        for tactitem in self.tactics:
            str_tactics += reverse_lookup(self.TACTICS, tactitem.tactic)
            str_tactics += " * " + reverse_lookup(self.SUB_TACTICS, tactitem.subtactic)
            if(i < length):
                str_tactics += delimiter
            i += 1
        return str_tactics

    def prnt_tactics(self):
        length = len(self.tactics)
        i = 1
        for tactitem in self.tactics:
            if(i < length):
                str_end = " | "
            else:
                str_end = "\n"
            subtactic_str = " * " + reverse_lookup(self.SUB_TACTICS, tactitem.subtactic)
            print(reverse_lookup(self.TACTICS, tactitem.tactic) + subtactic_str, end=str_end)
            i += 1

# class end


