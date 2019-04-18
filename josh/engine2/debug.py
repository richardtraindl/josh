from .match import *
from .move import *
from .helper import *


def prnt_minutes(match):
    count = 1
    print("------------------------------------------------------")
    for move in match.move_list[1:]:
        print(str(count) + ":" + 
              index_to_coord(move.srcx, move.srcy) + " " +
              index_to_coord(move.dstx, move.dsty) + " " +
              reverse_lookup(PIECES, move.prompiece))
        count += 1
    print("------------------------------------------------------")


class ClassAttr:
    def __init__(self, attribute=None, label=None):
        self.attribute = attribute
        self.label = label

def list_match_attributes(match):
    attributes = []
    attributes.append(ClassAttr(match.status, "status"))
    attributes.append(ClassAttr(match.score, "score"))
    attributes.append(ClassAttr(match.level, "level"))
    attributes.append(ClassAttr(match.board.white_movecnt_short_castling_lost, "board.white_movecnt_short_castling_lost"))
    attributes.append(ClassAttr(match.board.white_movecnt_long_castling_lost, "board.white_movecnt_long_castling_lost"))
    attributes.append(ClassAttr(match.board.black_movecnt_short_castling_lost, "board.black_movecnt_short_castling_lost"))
    attributes.append(ClassAttr(match.board.black_movecnt_long_castling_lost, "board.black_movecnt_long_castling_lost"))
    attributes.append(ClassAttr(match.board.wKg_x, "board.wKg_x"))
    attributes.append(ClassAttr(match.board.wKg_y, "board.wKg_y"))
    attributes.append(ClassAttr(match.board.bKg_x, "board.bKg_x"))
    attributes.append(ClassAttr(match.board.bKg_y, "board.bKg_y"))
    attributes.append(ClassAttr(match.board.wQu_cnt, "board.wQu_cnt"))
    attributes.append(ClassAttr(match.board.bQu_cnt, "board.bQu_cnt"))
    attributes.append(ClassAttr(match.board.wOfficer_cnt, "board.wOfficer_cnt"))
    attributes.append(ClassAttr(match.board.bOfficer_cnt, "board.bOfficer_cnt"))
    return attributes


def prnt_match_attributes(match, delimiter):
    classattrs = list_match_attributes(match)
    print("------------------------------------------------------")
    for classattr in classattrs:
        print(classattr.label + ":" + str(classattr.attribute) + delimiter, end="\n")
    print("------------------------------------------------------")


def prnt_matches_diff(match1, match2):
    if(match1.status != match2.status):
        print("status " + str(match2.status))
    if(match1.score != match2.score):
        print("score " + str(match2.score))
    if(match1.level != match2.level):
        print("level " + str(match2.level))
    if(match1.movecnt() != match2.movecnt()):
        print("movecnt " + str(match1.movecnt()) + " " + str(match2.movecnt()))
    if(match1.board.white_movecnt_short_castling_lost != match2.board.white_movecnt_short_castling_lost):
        print("white_mvcnt_sh_castling_lost " + str(match2.board.white_movecnt_short_castling_lost))
    if(match1.board.white_movecnt_long_castling_lost != match2.board.white_movecnt_long_castling_lost):
        print("black_mvcnt_sh_castling_lost " + str(match2.board.white_movecnt_long_castling_lost))
    if(match1.board.black_movecnt_short_castling_lost != match2.board.black_movecnt_short_castling_lost):
        print("white_mvcnt_lg_castling_lost " + str(match2.board.black_movecnt_short_castling_lost))
    if(match1.board.black_movecnt_long_castling_lost != match2.board.black_movecnt_long_castling_lost):
        print("black_mvcnt_lg_castling_lost " + str(match2.board.black_movecnt_long_castling_lost))
    if(match1.board.wKg_x != match2.board.wKg_x):
        print("wKg_x " + str(match2.board.wKg_x))
    if(match1.board.wKg_y != match2.board.wKg_y):
        print("wKg_y " + str(match2.board.wKg_y))
    if(match1.board.bKg_x != match2.board.bKg_x):
        print("bKg_x " + str(match2.board.bKg_x))
    if(match1.board.bKg_y != match2.board.bKg_y):
        print("bKg_y " + str(match2.board.bKg_y))
    if(match1.board.wQu_cnt != match2.board.wQu_cnt):
        print("wQu_cnt " + str(match2.board.wQu_cnt))
    if(match1.board.bQu_cnt != match2.board.bQu_cnt):
        print("bQu_cnt " + str())
    if(match1.board.wOfficer_cnt != match2.board.wOfficer_cnt):
        print("wOfficer_cnt " + str(match2.board.wOfficer_cnt))
    if(match1.board.bOfficer_cnt != match2.board.bOfficer_cnt):
        print("bOfficer_cnt " + str(match2.board.bOfficer_cnt))

    
BLANK_BG  = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020" ] * 4

KING_BG = [ u"\u0020\u0020\u2584\u2588\u2584\u0020\u0020",
            u"\u0020\u2584\u0020\u2588\u0020\u2584\u0020",
            u"\u0020\u2588\u2588\u2588\u2588\u2588\u0020",
            u"\u0020\u2580\u2580\u2580\u2580\u2580\u0020"]

QUEEN_BG = [ u"\u2584\u0020\u2584\u0020\u2584\u0020\u2584",
             u"\u0020\u2588\u0020\u2588\u0020\u2588\u0020",
             u"\u0020\u0020\u2588\u2588\u2588\u0020\u0020",
             u"\u0020\u0020\u2580\u2580\u2580\u0020\u0020"]

ROOK_BG = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020",
            u"\u0020\u2588\u2584\u2588\u2584\u2588\u0020",
            u"\u0020\u0020\u2588\u2588\u2588\u0020\u0020",
            u"\u0020\u2580\u2580\u2580\u2580\u2580\u0020"]

BISHOP_BG = [ u"\u0020\u0020\u0020\u2584\u0020\u0020\u0020",
              u"\u0020\u0020\u2584\u2588\u2584\u0020\u0020",
              u"\u0020\u2584\u2588\u2588\u2588\u2584\u0020",
              u"\u0020\u2580\u2580\u2580\u2580\u2580\u0020"]

KNIGHT_BG = [ u"\u0020\u0020\u0020\u2584\u0020\u0020\u0020", 
              u"\u0020\u0020\u2588\u2580\u2588\u0020\u0020",
              u"\u0020\u2580\u0020\u0020\u2588\u2588\u0020",
              u"\u0020\u0020\u0020\u2580\u2580\u2580\u2580"] 

PAWN_BG   = [ u"\u0020\u0020\u0020\u0020\u0020\u0020\u0020",
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

def prnt_row(match, pieces, mode):
    if(mode == 0):
        height = 4
    else:
        height = 1
    for i in range(height):
        for k in range(8):
            piece = pieces[k][0]
            backcolor = pieces[k][1]
            if(match.color_of_piece(piece) == COLORS['white']):
                forecolor = "white"
            else:
                forecolor = "black"

            if(piece == PIECES['blk']):
                piecemap = BLANK_BG
            elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                piecemap = PAWN_BG
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                piecemap = KNIGHT_BG
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                piecemap = BISHOP_BG
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                piecemap = ROOK_BG
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                piecemap = QUEEN_BG
            else:
                piecemap = KING_BG

            if(k == 7):
                endstr = "\n"
            else:
                endstr = ""

            if(mode == 0):
                piece_txt = piecemap[i]
            else:
                piece_txt = PIECES_TEXT[piece]
            if(forecolor == "white"):
                if(backcolor == "white"):
                    print(WHITE_BACK + WHITE_TEXT + BOLD_OFF + piece_txt + RESET_ALL, end=endstr)
                else:
                    print(BLUE_BACK + WHITE_TEXT + BOLD_OFF + piece_txt + RESET_ALL, end=endstr)
            else:
                if(backcolor == "white"):
                    print(WHITE_BACK + BLACK_TEXT + piece_txt + RESET_ALL, end=endstr)
                else:
                    print(BLUE_BACK + BLACK_TEXT + piece_txt + RESET_ALL, end=endstr)

def prnt_board(match, mode=1):
    pieces = []
    for y in range(7, -1, -1):
        for x in range(8):
            if((y % 2 + x) % 2 == 1):
                backcolor = "white"
            else:
                backcolor = "black"
            pieces.append([match.board.readfield(x, y), backcolor])
        prnt_row(match, pieces, mode)
        pieces.clear()


def list_move_attributes(move):
    attributes = []
    attributes.append(ClassAttr(move.match, "match"))
    attributes.append(ClassAttr(move.count, "count"))
    attributes.append(ClassAttr(move.iscastling, "iscastling"))
    attributes.append(ClassAttr(move.srcx, "srcx"))
    attributes.append(ClassAttr(move.srcy, "srcy"))
    attributes.append(ClassAttr(move.dstx, "dstx"))
    attributes.append(ClassAttr(move.dsty, "dsty"))
    attributes.append(ClassAttr(move.enpassx, "enpassx"))
    attributes.append(ClassAttr(move.enpassy, "enpassy"))
    attributes.append(ClassAttr(move.captpiece, "captpiece"))
    attributes.append(ClassAttr(move.prompiece, "prompiece"))
    return attributes


    """if(gmove.srcx == 7 and gmove.srcy == 0 and  gmove.dstx == 3 and gmove.dsty == 0):
        print("yyyyyyyyyyyyyyy: " + str(PIECES_RANK[piece]) + " " + str(PIECES_RANK[lowest_enemy_on_dstfield]))
        print("xxxxxxxxxxxxxxx: " + str(len(frdlytouches_on_dstfield)) + " " + str(len(enmytouches_on_dstfield)))"""
