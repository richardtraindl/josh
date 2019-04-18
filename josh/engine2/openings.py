import random
from .match import *
from .move import *
from .helper import coord_to_index, index_to_coord


def retrieve_move(match):
    if(match.movecnt() >= DEPTH):
        print("############ depth not supported ############")
        return None

    root = fill_openings()
    node = root
    for move in match.move_list:
        str_move = index_to_coord(move.srcx, move.srcy)
        str_move += "-"
        str_move += index_to_coord(move.dstx, move.dsty)
        ok = False
        for childnode in node.children:
            #print("childnode: " + str(childnode.str_move) + " str_move: " + str_move)
            if(childnode.str_move == str_move):
                    node = childnode
                    ok = True
                    break
        if(ok):
            continue
        else:
            node = None

    if(match.movecnt() > 0 and (node is None or node is root or len(node.children) == 0)):
        print("############ No opening move found ############")
        return None
    else:
        if(match.movecnt() == 0):
            node = root
        idx = random.randint(0, len(node.children) - 1)
        candidate = node.children[idx]
        srcx, srcy = coord_to_index(candidate.str_move[:2])
        dstx, dsty = coord_to_index(candidate.str_move[3:])
        return cGenMove(match, srcx, srcy, dstx, dstx, PIECES['blk'])


DEPTH = 4


class cNode:
    def __init__(self, parent=None, str_move=""):
        self.parent = parent
        self.str_move = str_move
        self.children = []
        if(parent):
            parent.children.append(self)

    @classmethod
    def add_children(cls, parent, children):
        for child in children:
            cNode(parent, child)

    @classmethod
    def populate_moves(cls, parent, moves):
        node = parent
        for move in moves:
            found = False
            for child in node.children:
                if(child.str_move == move):
                    node = child
                    found = True
                    break
            if(found == False):
                newnode = cNode(node, move)
                node.children.append(newnode)
                node = newnode

def fill_openings():
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

