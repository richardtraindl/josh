
import random

from ..match import *
from ..board import cBoard
from ..move import *
from ..helper import coord_to_index


class cOpenings:
    MAXDEPTH = 2
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

    node = cNode(cBoard.BASE, \
                 ["e2-e4", "d2-d4", "c2-c4", "g1-f3", "g2-g3", "d2-d3"])
    openings.add_node(node, 0)

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
    
    return openings


def retrieve_move(match):
    candidates = None
    prevfields = cBoard.BASE
    if(match.movecnt() >= cOpenings.MAXDEPTH):
        print("### depth not supported ###")
        return candidates

    openings = populate_openings()
    stage = openings.stages[match.movecnt()]
    if(match.movecnt() == 0):
        candidates = stage[0].candidates
    else:
        move = match.minutes[-1]
        for node in stage:
            if(node.fields == match.board.fields):
                candidates = node.candidates
                prevfields = node.fields
                break

    if(candidates is None):
        print("### No opening move found ###")
        return candidates

    idx = random.randint(0, len(candidates) - 1)
    candidate = candidates[idx]
    print(candidate)
    src = coord_to_index(candidate[:2])
    dst = coord_to_index(candidate[3:])
    return cMove(prevfields, src, dst, PIECES['blk'])


def fill_openings_old():
    root = cNode(None, "")
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "g1-f3", "g8-f6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "g1-f3", "b8-c6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "g1-f3", "d7-d6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "g1-f3", "e7-e6"]) 
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "b1-c3", "g8-f6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "b1-c3", "b8-c6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "b1-c3", "d7-d6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "b1-c3", "e7-e6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "f1-c4", "g8-f6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "f1-c4", "b8-c6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "f1-c4", "d7-d6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "f1-c4", "e7-e6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e5", "f1-c4", "f8-c5"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "g1-f3", "b8-c6"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "g1-f3", "d7-d6"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "g1-f3", "e7-e6"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "g1-f3", "g7-g6"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "d2-d4", "c5-d4"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "f1-c4", "b8-c6"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "f1-c4", "d7-d6"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "f1-c4", "e7-e6"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "b1-c3", "b8-c6"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "b1-c3", "d7-d6"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "b1-c3", "e7-e6"])
    cNode.populate_moves(root, ["e2-e4", "c7-c5", "b1-c3", "g7-g6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e6", "d2-d4", "d7-d5"])
    cNode.populate_moves(root, ["e2-e4", "e7-e6", "d2-d4", "d7-d6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e6", "g1-f3", "d7-d5"])
    cNode.populate_moves(root, ["e2-e4", "e7-e6", "g1-f3", "d7-d6"])
    cNode.populate_moves(root, ["e2-e4", "e7-e6", "b1-c3", "d7-d5"])
    cNode.populate_moves(root, ["e2-e4", "e7-e6", "b1-c3", "d7-d6"])
    cNode.populate_moves(root, ["e2-e4", "d7-d6", "d2-d4", "e7-e5"])
    cNode.populate_moves(root, ["e2-e4", "d7-d6", "d2-d4", "e7-e6"]) 
    cNode.populate_moves(root, ["e2-e4", "d7-d6", "g1-f3", "e7-e6"]) 
    cNode.populate_moves(root, ["e2-e4", "d7-d6", "f1-c4", "e7-e6"]) 
    cNode.populate_moves(root, ["e2-e4", "d7-d6", "b1-c3", "e7-e6"]) 
    cNode.populate_moves(root, ["d2-d4", "d7-d5", "c2-c4", "d5-c4"]) 
    cNode.populate_moves(root, ["d2-d4", "d7-d5", "g1-f3"]) 
    cNode.populate_moves(root, ["d2-d4", "d7-d5", "c1-f4"]) 
    cNode.populate_moves(root, ["d2-d4", "d7-d6", "e2-e4"]) 
    cNode.populate_moves(root, ["d2-d4", "d7-d6", "c2-c4"]) 
    cNode.populate_moves(root, ["d2-d4", "d7-d6", "g1-f3"]) 
    cNode.populate_moves(root, ["d2-d4", "d7-d6", "c1-f4"]) 
    cNode.populate_moves(root, ["d2-d4", "e7-e6", "e2-e4", "d7-d5"])
    cNode.populate_moves(root, ["d2-d4", "e7-e6", "c2-c4", "d7-d5"]) 
    cNode.populate_moves(root, ["d2-d4", "e7-e6", "g1-f3"])
    cNode.populate_moves(root, ["d2-d4", "e7-e6", "c1-f4"]) 
    cNode.populate_moves(root, ["d2-d4", "g8-f6", "c2-c4"])
    cNode.populate_moves(root, ["d2-d4", "g8-f6", "g1-f3"])
    cNode.populate_moves(root, ["d2-d4", "g8-f6", "c1-f4"])
    cNode.populate_moves(root, ["c2-c4", "e7-e5", "b1-c3"]) 
    cNode.populate_moves(root, ["c2-c4", "e7-e5", "d2-d3"]) 
    cNode.populate_moves(root, ["c2-c4", "e7-e5", "g2-g3"]) 
    cNode.populate_moves(root, ["c2-c4", "c7-c5", "b1-c3"]) 
    cNode.populate_moves(root, ["c2-c4", "c7-c5", "g1-f3"]) 
    cNode.populate_moves(root, ["c2-c4", "c7-c5", "g2-g3"]) 
    cNode.populate_moves(root, ["c2-c4", "c7-c5", "e2-e3"]) 
    cNode.populate_moves(root, ["c2-c4", "g8-f6", "d2-d4"])
    cNode.populate_moves(root, ["c2-c4", "g8-f6", "b1-c3"]) 
    cNode.populate_moves(root, ["c2-c4", "g8-f6", "g1-f3"]) 
    cNode.populate_moves(root, ["c2-c4", "g8-f6", "g2-g3"])
    cNode.populate_moves(root, ["c2-c4", "d7-d6", "d2-d4"]) 
    cNode.populate_moves(root, ["c2-c4", "d7-d6", "b1-c3"]) 
    cNode.populate_moves(root, ["c2-c4", "d7-d6", "g1-f3"]) 
    cNode.populate_moves(root, ["c2-c4", "d7-d6", "g2-g3"]) 
    cNode.populate_moves(root, ["c2-c4", "g7-g6", "d2-d4"]) 
    cNode.populate_moves(root, ["c2-c4", "g7-g6", "g1-f3"]) 
    cNode.populate_moves(root, ["c2-c4", "g7-g6", "b1-c3"]) 
    cNode.populate_moves(root, ["c2-c4", "g7-g6", "g2-g3"]) 
    cNode.populate_moves(root, ["g1-f3", "d7-d5", "d2-d4"]) 
    cNode.populate_moves(root, ["g1-f3", "d7-d5", "d2-d3"]) 
    cNode.populate_moves(root, ["g1-f3", "d7-d5", "g2-g3"]) 
    cNode.populate_moves(root, ["g1-f3", "c7-c5", "e2-e4"]) 
    cNode.populate_moves(root, ["g1-f3", "c7-c5", "c2-c4"]) 
    cNode.populate_moves(root, ["g1-f3", "c7-c5", "g2-g3"]) 
    cNode.populate_moves(root, ["g1-f3", "c7-c5", "d2-d4"]) 
    cNode.populate_moves(root, ["g1-f3", "g8-f6", "d2-d4"]) 
    cNode.populate_moves(root, ["g1-f3", "g8-f6", "c2-c4"]) 
    cNode.populate_moves(root, ["g1-f3", "g8-f6", "g2-g3"]) 
    cNode.populate_moves(root, ["g1-f3", "d7-d6", "e2-e4"]) 
    cNode.populate_moves(root, ["g1-f3", "d7-d6", "d2-d4"]) 
    cNode.populate_moves(root, ["g1-f3", "d7-d6", "c2-c4"]) 
    cNode.populate_moves(root, ["g1-f3", "d7-d6", "g2-g3"]) 
    cNode.populate_moves(root, ["g1-f3", "e7-e6", "e2-e4"]) 
    cNode.populate_moves(root, ["g1-f3", "e7-e6", "d2-d4"]) 
    cNode.populate_moves(root, ["g1-f3", "e7-e6", "c2-c4"]) 
    cNode.populate_moves(root, ["g1-f3", "e7-e6", "g2-g3"]) 
    cNode.populate_moves(root, ["g2-g3", "g7-g6", "f1-g2"])            
    cNode.populate_moves(root, ["g2-g3", "e7-e5", "f1-g2"]) 
    cNode.populate_moves(root, ["g2-g3", "d7-d5", "f1-g2"]) 
    cNode.populate_moves(root, ["g2-g3", "c7-c5", "f1-g2"]) 
    cNode.populate_moves(root, ["g2-g3", "f8-g6", "f1-g2"])
    return root

