
import random

from ..match import *
from ..board import cBoard
from ..move import *
from ..helper import coord_to_index


class cOpenings:
    MAXDEPTH = 4
    def __init__(self):
        self.stages =  [[],[],[],[]]

    def add_node(self, node, depth):
        if(depth >= 0 and depth < self.MAXDEPTH):
            self.stages[depth].append(node)
# class end


class cNode:
    def __init__(self, fields, candidates):
        self.fields = fields
        self.candidates = candidates
# class end


def populate_openings():
    openings = cOpenings()

    #################
    node = cNode(cBoard.BASE, \
                 ["e2-e4", "d2-d4", "c2-c4", "g1-f3", "g2-g3", "d2-d3"])
    openings.add_node(node, 0)

    #################
    #e2-e4
    node = cNode(0X42356324111101110000000000001000000000000000000099999999CABDEBAC, \
                 ["e7-e5","c7-c5","e7-e6","g8-f6","g7-g6"])
    openings.add_node(node, 1)

    #d2-d4
    node = cNode(0X42356324111011110000000000010000000000000000000099999999CABDEBAC, \
                 ["d7-d5","f7-f5","g8-f6","g7-g6","e7-e6"])
    openings.add_node(node, 1)

    #c2-c4
    node = cNode(0X42356324110111110000000000100000000000000000000099999999CABDEBAC, \
                 ["e7-e5","c7-c5","b8-c6","g8-f6","g7-g6"])
    openings.add_node(node, 1)

    #g1-f3
    node = cNode(0X42356304111111110000020000000000000000000000000099999999CABDEBAC, \
                 ["d7-d5","g8-f6","g7-g6","c7-c5","b8-c6"])
    openings.add_node(node, 1)

    #g2-g3
    node = cNode(0X42356324111111010000001000000000000000000000000099999999CABDEBAC, \
                 ["e7-e5","d7-d5","c7-c5","g8-f6","g7-g6"])
    openings.add_node(node, 1)

    #d2-d3
    node = cNode(0X42356324111011110001000000000000000000000000000099999999CABDEBAC, \
                 ["e7-e5","d7-d5","c7-c5","g8-f6","g7-g6"])
    openings.add_node(node, 1)
    #################

    #################
    #e2-e4, e7-e5
    node = cNode(0X42356324111101110000000000001000000090000000000099990999CABDEBAC, \
                 ["g1-f3", "b1-c3", "f1-c4"])
    openings.add_node(node, 2)

    #e2-e4, c7-c5
    node = cNode(0X42356324111101110000000000001000009000000000000099099999CABDEBAC, \
                 ["g1-f3", "d2-d4", "f1-c4", "b1-c3"])
    openings.add_node(node, 2)
    
    #e2-e4, e7-e6
    node = cNode(0X42356324111101110000000000001000000000000000900099990999CABDEBAC, \
                 ["d2-d4", "g1-f3", "b1-c3"])
    openings.add_node(node, 2)
 
    #"e2-e4, d7-d6
    node = cNode(0X42356324111101110000000000001000000000000009000099909999CABDEBAC, \
                 ["d2-d4", "g1-f3", "f1-c4", "b1-c3"])
    openings.add_node(node, 2)
    
    #d2-d4, d7-d5
    node = cNode(0X42356324111011110000000000010000000900000000000099909999CABDEBAC, \
                 ["c2-c4", "g1-f3", "c1-f4"])
    openings.add_node(node, 2)

    #d2-d4, f7-f5
    node = cNode(0X42356324111011110000000000010000000009000000000099999099CABDEBAC, \
                 ["c2-c4", "g1-f3", "g2-g3", "e2-e4"])
    openings.add_node(node, 2)

    #d2-d4, d7-d6
    node = cNode(0X42356324111011110000000000010000000000000009000099909999CABDEBAC, \
                 ["e2-e4", "c2-c4", "g1-f3", "c1-f4"])
    openings.add_node(node, 2)

    #d2-d4, e7-e6
    node = cNode(0X42356324111011110000000000010000000000000000900099990999CABDEBAC, \
                 ["e2-e4", "c2-c4", "g1-f3", "c1-f4"])
    openings.add_node(node, 2)

    #d2-d4, g8-f6
    node = cNode(0X423563241110111100000000000100000000000000000A0099999999CABDEB0C, \
                 ["c2-c4", "g1-f3", "c1-f4"])
    openings.add_node(node, 2)

    #c2-c4, e7-e5
    node = cNode(0X42356324110111110000000000100000000090000000000099990999CABDEBAC, \
                 ["b1-c3", "d2-d3", "g2-g3"])
    openings.add_node(node, 2)

    #c2-c4, c7-c5
    node = cNode(0X42356324110111110000000000100000009000000000000099099999CABDEBAC, \
                 ["b1-c3", "g1-f3", "g2-g3", "e2-e3"])
    openings.add_node(node, 2)

    #c2-c4, g8-f6
    node = cNode(0X423563241101111100000000001000000000000000000A0099999999CABDEB0C, \
                 ["d2-d4", "b1-c3", "g1-f3", "g2-g3"])
    openings.add_node(node, 2)

    #c2-c4, d7-d6
    node = cNode(0X42356324110111110000000000100000000000000009000099909999CABDEBAC, \
                 ["d2-d4", "b1-c3", "g1-f3", "g2-g3"])
    openings.add_node(node, 2)

    #c2-c4, g7-g6
    node = cNode(0X42356324110111110000000000100000000000000000009099999909CABDEBAC, \
                 ["d2-d4", "g1-f3", "b1-c3", "g2-g3"])
    openings.add_node(node, 2)

    #g1-f3, d7-d5
    node = cNode(0X42356304111111110000020000000000000900000000000099909999CABDEBAC, \
                 ["d2-d4", "d2-d3", "g2-g3"])
    openings.add_node(node, 2)

    #g1-f3, c7-c5
    node = cNode(0X42356304111111110000020000000000009000000000000099099999CABDEBAC, \
                 ["e2-e4", "c2-c4", "g2-g3", "d2-d4"])
    openings.add_node(node, 2)

    #g1-f3, g8-f6
    node = cNode(0X423563041111111100000200000000000000000000000A0099999999CABDEB0C, \
                 ["d2-d4", "c2-c4", "g2-g3"])
    openings.add_node(node, 2)

    #g1-f3, d7-d6
    node = cNode(0X42356304111111110000020000000000000000000009000099909999CABDEBAC, \
                 ["e2-e4", "d2-d4", "c2-c4", "g2-g3"])
    openings.add_node(node, 2)

    #g1-f3, e7-e6
    node = cNode(0X42356304111111110000020000000000000000000000900099990999CABDEBAC, \
                 ["e2-e4", "d2-d4", "c2-c4", "g2-g3"])
    openings.add_node(node, 2)

    #g2-g3, g7-g6
    node = cNode(0X42356324111111010000001000000000000000000000009099999909CABDEBAC, ["f1-g2"])
    openings.add_node(node, 2)

    #g2-g3, e7-e5
    node = cNode(0X42356324111111010000001000000000000090000000000099990999CABDEBAC, ["f1-g2"])
    openings.add_node(node, 2)

    #g2-g3, d7-d5
    node = cNode(0X42356324111111010000001000000000000900000000000099909999CABDEBAC, ["f1-g2"])
    openings.add_node(node, 2)

    #g2-g3, c7-c5
    node = cNode(0X42356324111111010000001000000000009000000000000099099999CABDEBAC, ["f1-g2"])
    openings.add_node(node, 2)

    #g2-g3, f8-g6
    node = cNode(0X423563241111110100000010000000000000000000000A0099999999CABDEB0C, ["f1-g2"])
    openings.add_node(node, 2)

    #d2-d3, e7-e5
    node = cNode(0X42356324111011110001000000000000000090000000000099990999CABDEBAC, \
                 ["e2-e4, c2-c4", "g1-f3"])
    openings.add_node(node, 2)

    #d2-d3, d7-d5
    node = cNode(0X42356324111011110001000000000000000900000000000099909999CABDEBAC, \
                 ["g1-f3, g2-g3", "e2-e3"])
    openings.add_node(node, 2)

    #d2-d3, c7-c5
    node = cNode(0X42356324111011110001000000000000009000000000000099099999CABDEBAC, \
                 ["e2-e4", "g1-f3"])
    openings.add_node(node, 2)

    #d2-d3, g8-f6
    node = cNode(0X423563241110111100010000000000000000000000000A0099999999CABDEB0C, \
                 ["e2-e4", "c2-c4", "g1-f3"])
    openings.add_node(node, 2)

    #d2-d3, g7-g6
    node = cNode(0X42356324111011110001000000000000000000000000009099999909CABDEBAC, \
                 ["c2-c4", "e2-e4", "g1-f3"])
    openings.add_node(node, 2)
    #################

    #################
    #d2-d4, f7-f5, e2-e4
    node = cNode(0X42356324111001110000000000011000000009000000000099999099CABDEBAC, \
                 ["g8-f6"])
    openings.add_node(node, 3)

    return openings


def retrieve_move(match):
    candidates = None
    prevfields = cBoard.BASE
    if(match.movecnt() >= cOpenings.MAXDEPTH):
        print("### openings: depth not supported ###")
        return candidates

    openings = populate_openings()
    stage = openings.stages[match.movecnt()]
    if(match.movecnt() == 0):
        if(stage[0].fields == match.board.fields):
            candidates = stage[0].candidates
    else:
        move = match.minutes[-1]
        for node in stage:
            if(node.fields == match.board.fields):
                candidates = node.candidates
                prevfields = node.fields
                break

    if(candidates is None):
        print("### openings: no opening move found ###")
        return candidates

    idx = random.randint(0, len(candidates) - 1)
    candidate = candidates[idx]
    src = coord_to_index(candidate[:2])
    dst = coord_to_index(candidate[3:])
    return cMove(prevfields, src, dst, PIECES['blk'])

