
#include <string>
#include "./helper.cpp"

using namespace std;

class cMove{
    private:
        int prevfields;
        int src;
        int dst;
        int prompiece;

    public:
        int getPrevfield(idx){
            return this.prevfields >> ((63 - idx) * 4)) & 0xF
        };

        string format(){
            piece = this.getPrevfield(this.src);
            if(piece == PIECE_WKG || piece == PIECES_BKG){
                if(this.src - this.dst == -2){
                    return "0-0";
                if(this.src - this.dst == 2):
                    return "0-0-0";
            dstpiece = this.getPrevfield(this.dst)
            if(dstpiece == PIECES_BLK){
                hyphen = "-";
            }
            else{
                hyphen = "x";
            }
            trailing = "";
            if(piece == PIECES_WPW || piece == PIECES_BPW){
                if(this.prompiece != NULL and this.prompiece != PIECES_BLK){
                    trailing = ", " + reverse_lookup(PIECES, this.prompiece);
                }
                else{
                    if(dstpiece == PIECES_BLK && (this.src % 8) != (this.dst % 8)){
                        trailing = " e.p.";
                    }
                }
            }
            return index_to_coord(this.src) + hyphen + index_to_coord(this.dst) + trailing;
        };
}


class cTactic{
    private:
        int domain;
        int weight;
        int addition;

    public:
        const MapStrInt DOMAINS = {
            {'defends-check' :         10},
            {'captures' :              20},
            {'attacks-king' :          30},
            {'attacks' :               40},
            {'supports' :              50},
            {'supports-running-pawn' : 60},
            {'flees' :                 70},
            {'forks' :                 80},
            {'threatens-fork' :        90},
            {'defends-fork' :          100},
            {'unpins' :                110},
            {'blocks' :                120},
            {'promotes' :              130}, 
            {'is-tactical-draw' :      140},
            {'prev-candidate' :        150},
            {'is-running-pawn' :       160}, 
            {'controles-file' :        170},
            {'castles' :               180},
            {'is-progress' :           190},
            {'opposition' :            200},
            {'approach-opp-king' :     210},
            {'is-undefined' :          220}
        };

        const MapStrInt WEIGHTS = {
            {'stormy' : 1},
            {'better-deal' : 2},
            {'good-deal' : 3},
            {'downgraded' : 4},
            {'upgraded' : 5},
            {'bad-deal' : 6}
        };

        const MapStrInt DOMAINS_TO_PRIOS = {
            // ### level 1 ###
            {DOMAINS['promotes'] :               90},
            {DOMAINS['captures'] :               91},
            {DOMAINS['is-running-pawn'] :        92},
            {DOMAINS['is-tactical-draw'] :       93},
            {DOMAINS['defends-check']  :         94},
            {DOMAINS['prev-candidate']  :        95},
            // ### level 2 ###
            {DOMAINS['castles'] :                200},
            {DOMAINS['attacks-king'] :           201},
            {DOMAINS['forks'] :                  202}, 
            {DOMAINS['threatens-fork'] :         203},
            {DOMAINS['defends-fork'] :           204}, 
            {DOMAINS['unpins'] :                 205}, 
            {DOMAINS['supports-running-pawn'] :  206}, 
            {DOMAINS['flees'] :                  207}, 
            {DOMAINS['blocks'] :                 208},
            {DOMAINS['controles-file'] :         209}, 
            {DOMAINS['is-progress'] :            210},
            {DOMAINS['supports'] :               211},
            {DOMAINS['attacks'] :                212},
            {DOMAINS['opposition'] :             213},
            {DOMAINS['approach-opp-king'] :      214},
            // ### level 3 ###
            {DOMAINS['is-undefined'] :           500}
        };

        const MapStrInt WEIGHTS_TO_ADJUST = {
            {WEIGHTS['stormy'] : -70}},
            {WEIGHTS['better-deal'] : -10},
            {WEIGHTS['good-deal'] : 0},
            {WEIGHTS['upgraded'] : 0},
            {WEIGHTS['downgraded'] : 60},
            {WEIGHTS['bad-deal'] : 130}
        };
};


class cPrioMove:
    private:
        cMove move
        // tactics = []
        int prio = PRIOS['prio3']

    public:
        const MapStrInt PRIOS = {
            {'prio0', 100},
            {'prio1', 200},
            {'prio2', 250},
            {'prio3', 300} 
        };

    def evaluate_priority(self):
        count = 0
        self.prio = self.PRIOS['prio3']
        for tactic in self.tactics:
            newprio = cTactic.DOMAINS_TO_PRIOS[tactic.domain] + \
                      cTactic.WEIGHTS_TO_ADJUST[tactic.weight]
            self.prio = min(self.prio, newprio)
            if(tactic.weight <= cTactic.WEIGHTS['downgraded']):
                count += 2
        self.prio -= count

    def downgrade(self, domain):
        for tactic in self.tactics:
            if(tactic.domain == domain):
                if(tactic.weight == cTactic.WEIGHTS['stormy'] or
                   tactic.weight == cTactic.WEIGHTS['better-deal'] or
                   tactic.weight == cTactic.WEIGHTS['good-deal']):
                    tactic.weight = cTactic.WEIGHTS['downgraded']
                return

    def upgrade(self, domain):
        for tactic in self.tactics:
            if(tactic.domain == domain):
                if(tactic.weight != cTactic.WEIGHTS['stormy'] and 
                   tactic.weight != cTactic.WEIGHTS['better-deal'] and 
                   tactic.weight != cTactic.WEIGHTS['good-deal']):
                    tactic.weight = cTactic.WEIGHTS['upgraded']
                    return

    def fetch_weight(self, domain):
        for tactic in self.tactics:
            if(tactic.domain == domain):
                return tactic.weight
        return None

    def has_domain(self, domain):
        for tactic in self.tactics:
            if(tactic.domain == domain):
                return True
        return False

    def has_weight(self, weight):
        for tactic in self.tactics:
            if(tactic.weight == weight):
                return True
        return False

    def has_tactic_ext(self, tactic):
        for tactitem in self.tactics:
            if(tactitem.domain == tactic.domain and tactitem.weight == tactic.weight):
                return True
        return False

    def is_tactic_stormy(self):
        for tactic in self.tactics:
            if(tactic.weight == cTactic.WEIGHTS['stormy'] or
               ((tactic.domain == cTactic.DOMAINS['promotes'] or
                 tactic.domain == cTactic.DOMAINS['captures']) and 
                (tactic.weight == cTactic.WEIGHTS['better-deal'] or
                 tactic.weight == cTactic.WEIGHTS['good-deal']))):
                return True
        return False

    def concat_fmttactics(self):
        str_tactics = ""
        length = len(self.tactics)
        i = 1
        for tactic in self.tactics:
            if(i < length):
                str_end = " | "
            else:
                str_end = "\n"
            weight_str = " * " + reverse_lookup(cTactic.WEIGHTS, tactic.weight)
            str_tactics += reverse_lookup(cTactic.DOMAINS, tactic.domain) + weight_str  + str_end
            i += 1
        return str_tactics
# class end
