
from .values import *
from .match import *
from .move import *
from .helper import *


def prnt_minutes(match):
    count = 1
    print("------------------------------------------------------")
    for move in match.minutes[1:]:
        print(str(count) + ":" + 
              index_to_coord(move.src, move.src) + " " +
              index_to_coord(move.dst, move.dst) + " " +
              reverse_lookup(PIECES, move.prompiece))
        count += 1
    print("------------------------------------------------------")


class ClassAttr:
    def __init__(self, attribute=None, label=None):
        self.attribute = attribute
        self.label = label

def list_match_attributes(match):
    attributes = []
    attributes.append(ClassAttr(match.created_at, "created_at"))
    attributes.append(ClassAttr(match.status, "status"))
    attributes.append(ClassAttr(match.score, "score"))
    attributes.append(ClassAttr(match.level, "level"))
    attributes.append(ClassAttr(match.board.fields, "board.fields"))
    attributes.append(ClassAttr(match.board.wKg, "board.wKg"))
    attributes.append(ClassAttr(match.board.bKg, "board.bKg"))
    attributes.append(ClassAttr(match.board.wKg_first_move_on, "board.wKg_first_move_on"))
    attributes.append(ClassAttr(match.board.bKg_first_move_on, "board.bKg_first_move_on"))
    attributes.append(ClassAttr(match.board.wRkA_first_move_on, "board.wRkA_first_move_on"))
    attributes.append(ClassAttr(match.board.wRkH_first_move_on, "board.wRkH_first_move_on"))
    attributes.append(ClassAttr(match.board.bRkA_first_move_on, "board.bRkA_first_move_on"))
    attributes.append(ClassAttr(match.board.bRkH_first_move_on, "board.bRkH_first_move_on"))
    return attributes


def prnt_match_attributes(match, delimiter):
    classattrs = list_match_attributes(match)

    print("------------------------------------------------------")

    for classattr in classattrs:
        print(classattr.label + ":" + str(classattr.attribute) + delimiter, end="\n")

    print("------------------------------------------------------")


    
BLANK  = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020" ] * 4

KING   = [ u"\u0020\u0020\u2584\u2588\u2584\u0020\u0020",
           u"\u0020\u2584\u0020\u2588\u0020\u2584\u0020",
           u"\u0020\u2588\u2588\u2588\u2588\u2588\u0020",
           u"\u0020\u2580\u2580\u2580\u2580\u2580\u0020"]

QUEEN   = [ u"\u2584\u0020\u2584\u0020\u2584\u0020\u2584",
            u"\u0020\u2588\u0020\u2588\u0020\u2588\u0020",
            u"\u0020\u0020\u2588\u2588\u2588\u0020\u0020",
            u"\u0020\u0020\u2580\u2580\u2580\u0020\u0020"]

ROOK   = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020",
           u"\u0020\u2588\u2584\u2588\u2584\u2588\u0020",
           u"\u0020\u0020\u2588\u2588\u2588\u0020\u0020",
           u"\u0020\u2580\u2580\u2580\u2580\u2580\u0020"]

BISHOP   = [ u"\u0020\u0020\u0020\u2584\u0020\u0020\u0020",
             u"\u0020\u0020\u2584\u2588\u2584\u0020\u0020",
             u"\u0020\u2584\u2588\u2588\u2588\u2584\u0020",
             u"\u0020\u2580\u2580\u2580\u2580\u2580\u0020"]

KNIGHT   = [ u"\u0020\u0020\u0020\u2584\u0020\u0020\u0020", 
             u"\u0020\u0020\u2588\u2580\u2588\u0020\u0020",
             u"\u0020\u2580\u0020\u0020\u2588\u2588\u0020",
             u"\u0020\u0020\u0020\u2580\u2580\u2580\u2580"] 

PAWN     = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020",
             u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020",
             u"\u0020\u0020\u2584\u2588\u2584\u0020\u0020",
             u"\u0020\u2580\u2580\u2580\u2580\u2580\u0020"]

WHITE_TEXT = "\033[37m"
BLACK_TEXT = "\033[30m"
WHITE_BACK = "\033[47m"
BROWN_BACK = "\033[43m"
BLUE_BACK  = "\033[44m"
BOLD_ON    = "\033[1m"
BOLD_OFF   = "\033[2m"
MAGIC      = "\033[3m"
RESET_ALL  = "\033[0m"

def prnt_row(pieces):
    for i in range(4):
        for k in range(8):
            piece = pieces[k][0]
            backcolor = pieces[k][1]

            if(cMatch.color_of_piece(piece) == COLORS['white']):
                forecolor = "white"
            else:
                forecolor = "black"

            if(piece == PIECES['blk']):
                piecemap = BLANK
            elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                piecemap = PAWN
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                piecemap = KNIGHT
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                piecemap = BISHOP
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                piecemap = ROOK
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                piecemap = QUEEN
            else:
                piecemap = KING

            if(k == 7):
                endstr = "\n"
            else:
                endstr = ""

            offset = i * 9


            if(forecolor == "white"):
                if(backcolor == "white"):
                    print(WHITE_BACK + WHITE_TEXT + BOLD_ON + piecemap[i] + RESET_ALL, end=endstr)
                else:
                    print(BLUE_BACK + WHITE_TEXT + BOLD_ON + piecemap[i] + RESET_ALL, end=endstr)
            else:
                if(backcolor == "white"):
                    print(WHITE_BACK + BLACK_TEXT + piecemap[i] + RESET_ALL, end=endstr)
                else:
                    print(BLUE_BACK + BLACK_TEXT + piecemap[i] + RESET_ALL, end=endstr)


def prnt_board(match):
    pieces = []
    for y in range(7, -1, -1):
        for x in range(8):
            if((y % 2 + x) % 2 == 1):
                backcolor = "white"
            else:
                backcolor = "black"
            pieces.append([match.board.getfield(x + y * 8), backcolor])
        prnt_row(pieces)
        pieces.clear()


def list_move_attributes(move):
    attributes = []
    attributes.append(ClassAttr(move.prevfields, "prevfields"))
    attributes.append(ClassAttr(move.src, "src"))
    attributes.append(ClassAttr(move.dst, "dst"))
    attributes.append(ClassAttr(move.prompiece, "prompiece"))
    return attributes


def import_from_fields(fields=0x0):
    match = cMatch()
    match.board.fields = fields
    for idx in range(64):
        piece = match.board.getfield(idx)
        if(piece == PIECES['wKg']):
            match.board.wKg = idx
            continue
        if(piece == PIECES['bKg']):
            match.board.bKg = idx
    if(match.board.verify()):
        return match
    else:
        return None



