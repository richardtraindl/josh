import re, os, threading, copy
from engine2.values import *
from engine2.match import *
from engine2.move import *
from engine2.calc import calc_move
from engine2.pieces.king import cKing
from engine2.debug import prnt_match_attributes, prnt_board, list_match_attributes, list_move_attributes
from engine2.helper import coord_to_index, reverse_lookup


dictionary = []
immanuels_dir = "/home/richard/.immanuel"


class Word():
    def __init__(self, name=None, code=None, info=None):
        self.name = name
        self.code = code
        self.info = info

def new_word(name, code, info):
    word = Word(name, code, info)
    dictionary.append(word)


def init_words():
    new_word("help", word_help, "this help")
    new_word("?", word_help, "this help")
    new_word("bye", word_bye, "exit")
    new_word("pause", word_pause, "pauses match")
    new_word("resume", word_resume, "resumes (paused) match")
    new_word("show", word_show, "prints debug info")
    new_word("level", word_level, "sets level, e.g. level medium")
    new_word("human", word_human, "sets player to human, e.g. human black")
    new_word("engine", word_engine, "sets player to engine, e.g. engine white")
    new_word("setup", word_setup, "start to set up a chess position")
    new_word("close", word_close, "closes setup")
    new_word("piece", word_piece, "sets a piece on the board during setups")
    new_word("mv", word_move, "moves piece(s), e.g. move e2-e4")
    new_word("undo", word_undo, "undos last move")
    new_word("list", word_list, "lists all saved matches")
    new_word("save", word_save, "saves match")
    new_word("load", word_load, "loads match with id, e.g. load 3")
    new_word("delete", word_delete, "deletes match with id, e.g. delete 3")
    new_word("debug", word_debug, "debug a function")


class CalcThread(threading.Thread):
    def __init__(self, session):
        threading.Thread.__init__(self)
        self.session = session
        self.match = copy.deepcopy(session.match)

    def run(self):
        self.session.thread_is_busy = True
        print("Thread starting...")
        second_candidate = None
        if(len(self.match.move_list) > 0 and len(self.session.candidate_list) >= 2):
            last_move = self.match.move_list[-1]
            first_candidate = self.session.candidate_list[0]
            if(first_candidate.srcx == last_move.srcx and
               first_candidate.srcy == last_move.srcy and
               first_candidate.dstx == last_move.dstx and
               first_candidate.dsty == last_move.dsty and
               first_candidate.prom_piece == last_move.prom_piece):
                second_candidate = self.session.candidate_list[1]
        candidates = calc_move(self.match, second_candidate)
        self.session.candidate_list.clear()
        if(len(candidates) > 0):
            gmove = candidates[0]
            self.session.match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
            if(len(candidates) >= 3):
                self.session.candidate_list.append(candidates[1])
                self.session.candidate_list.append(candidates[2])
            prnt_board(self.session.match, 0)
        else:
            print("no move found!")
        self.session.thread_is_busy = False


def calc_and_domove(session):
    match = session.match
    status = match.evaluate_status()
    if(session.thread_is_busy == False and 
       status == match.STATUS['open'] and 
       match.is_next_color_human() == False):
        session.thread = CalcThread(session)
        session.thread.start()
    else:
        if(status == match.STATUS['draw'] or
           status == match.STATUS['winner_white'] or 
           status == match.STATUS['winner_black']):
            print(reverse_lookup(match.STATUS, match.evaluate_status()))


def word_pause(session, params):
    match = session.match
    if(match.evaluate_status() == match.STATUS['open']):
        match.status = match.STATUS['paused']
    return True


def word_resume(session, params):
    match = session.match
    if(match.status == match.STATUS['paused'] or match.status == match.STATUS['setup']):
        match.status = match.STATUS['open']
    calc_and_domove(session)
    return True


def word_show(session, params):
    prnt_match_attributes(session.match, ", ")
    prnt_board(session.match, 0)
    return True


def word_level(session, params):
    msg = "level blitz | low | medium | high"
    if(params == "?"):
        print(msg)
        return True
    else:
        try:
            session.match.level = session.match.LEVELS[params]
            session.match.seconds_per_move = session.match.SECONDS_PER_MOVE[session.match.level]
        except KeyError:
            print("??? " + msg)
    return True


def word_human(session, params):
    msg = "human white | black | all"
    if(params == "?"):
        print(msg)
        return True
    else:
        if(params == "white"):
            session.match.white_player.is_human = True
        elif(params == "black"):
            session.match.black_player.is_human = True
        elif(params == "all"):
            session.match.white_player.is_human = True
            session.match.black_player.is_human = True
        else:
            print("??? " + msg)
    return True


def word_engine(session, params):
    msg = "engine white | black | all"
    if(params == "?"):
        print(msg)
        return True
    else:
        if(params == "white"):
            session.match.white_player.is_human = False
        elif(params == "black"):
            session.match.black_player.is_human = False
        elif(params == "all"):
            session.match.white_player.is_human = False
            session.match.black_player.is_human = False
        else:
            print("??? " + msg)
    return True


def word_move(session, params):
    match = session.match
    match.status = match.evaluate_status()
    if(match.status != match.STATUS['open']):
        print("??? " + reverse_lookup(match.STATUS, match.status))
        return True
    elif(match.is_next_color_human() == False):
        print("??? wrong color")
        return True

    prom_piece = "blk"

    matchobj = re.search(r"^\s*(?P<src>[a-hA-H][1-8])\s*[-xX]*\s*(?P<dst>[a-hA-H][1-8])\s*$", params)
    if(matchobj):
        srcx, srcy = coord_to_index(matchobj.group("src"))
        dstx, dsty = coord_to_index(matchobj.group("dst"))
    else:
        matchobj = re.search(r"^\s*(?P<src>[a-hA-H][1-8])\s*[-xX]*\s*(?P<dst>[a-hA-H][1-8])\s*[-,;]*\s*(?P<prom>\w+)\s*$", params)
        if(matchobj):
            srcx, srcy = coord_to_index(matchobj.group("src"))
            dstx, dsty = coord_to_index(matchobj.group("dst"))
            prom_piece = matchobj.group("prom")

            valid = False
            for piece in PIECES:
                if(piece == prom_piece):
                    valid = True
                    break
            if(valid == False):
                return True
        else:
            matchobj = re.search(r"^\s*(?P<short>[0oO][-][0oO])\s*$", params)
            if(matchobj):
                if(match.next_color() == COLORS['white']):
                    srcx = match.board.wKg_x
                    srcy = match.board.wKg_y
                else:
                    srcx = match.board.bKg_x
                    srcy = match.board.bKg_y
                dstx = srcx + 2
                dsty = srcy
            else:
                matchobj = re.search(r"^\s*(?P<long>[0oO][-][0oO][-][0oO])\s*$", params)
                if(matchobj):
                    if(match.next_color() == COLORS['white']):
                        srcx = match.board.wKg_x
                        srcy = match.board.wKg_y
                    else:
                        srcx = match.board.bKg_x
                        srcy = match.board.bKg_y
                    dstx = srcx - 2
                    dsty = srcy
                else:
                    return True

    if(match.is_move_valid(srcx, srcy, dstx, dsty, PIECES[prom_piece])[0]):
        match.do_move(srcx, srcy, dstx, dsty, PIECES[prom_piece])
        prnt_board(match, 0)
    else:
        print("invalid move!")

    return True


def word_undo(session, params):
    match = session.match
    if(len(params) > 0):
        count = abs(int(params))
    else:
        count = 1
    for i in range(count):
        match.undo_move()
    prnt_board(match, 0)
    if(match.evaluate_status() == match.STATUS['open']):
        match.status = match.STATUS['paused']
    return True


def word_list(session, params):
    filennames = os.listdir(immanuels_dir)
    print("[ ", end="")
    for filenname in filennames:
        if(filenname == "counter.txt"):
            continue
        else:
            print(filenname.replace(".txt", " "), end="")
    print("]")
    return True


def word_save(session, params):
    match = session.match
    counter = None
    if not os.path.isdir(immanuels_dir):
        os.makedirs(immanuels_dir)
    try:
        fobject = open(immanuels_dir + "/counter.txt", "r")
        data = fobject.read()
        fobject.close()
        counter = int(data)
        counter += 1
    except FileNotFoundError:
        counter = 1
    
    fobject = open(immanuels_dir + "/counter.txt", "w")
    fobject.write(str(counter))
    fobject.close()    
    #----------------------------
    fobject = open(immanuels_dir + "/" + str(counter) + ".txt", "w")

    attributes = list_match_attributes(session.match)
    for classattr in attributes:
        fobject.write(classattr.label + ":" + str(classattr.attribute) + ";")

    strboard = "board:"
    for y in range(8):
        for x in range(8):
            strboard += reverse_lookup(PIECES, match.board.readfield(x, y))
    fobject.write(strboard + ";")

    fobject.write("movelistcnt:" + str(len(match.move_list)) + ";")
    for move in match.move_list:
        attributes = list_move_attributes(move)
        for classattr in attributes:
            if(classattr.label == "match"):
                fobject.write(classattr.label + ":" + "None" + ";")
            else:
                fobject.write(classattr.label + ":" + str(classattr.attribute) + ";")
    #----------------------------
    fobject.close()
    return True


def word_load(session, params):
    try:
        fobject = open(immanuels_dir + "/" + params.strip() + ".txt", "r")
    except FileNotFoundError:
        print("??? file not found: " + params.strip())
        return True

    match = cMatch()
    tokens = fobject.read().split(";")
    index = 0

    # -----------------------
    attributes = list_match_attributes(match)
    for i in range(len(attributes)):
        for classattr in attributes:
            label_len = len(classattr.label)
            if(classattr.label == tokens[index][:label_len]):
                if(classattr.label == "begin"):
                    value = datetime.now()
                elif(classattr.label == "time_start"):
                    value = 0
                else:
                    strvalue= tokens[index].replace(classattr.label + ":", "")
                    if(strvalue == "None"):
                        value = None
                    elif(strvalue == "True"):
                        value = True
                    elif(strvalue == "False"):
                        value = False
                    else:
                        try: 
                            value = int(strvalue)
                        except ValueError:
                            value = strvalue

                if(classattr.label[:6] == "board."):
                    setattr(match.board, classattr.label, value)
                else:
                    setattr(match, classattr.label, value)
                break
        index += 1
    # -----------------------

    # -----------------------
    strboard = tokens[index].replace("board:", "")
    index += 1

    for y in range(8):
        for x in range(8):
            idx = (y * 24) + (x * 3)
            strfield = strboard[idx:idx+3]
            match.board.writefield(x, y, PIECES[strfield])
    # -----------------------

    # -----------------------
    movecnt = int(tokens[index].replace("movelistcnt:", ""))
    index += 1
    for i in range(movecnt):
        move = cMove()
        attributes = list_move_attributes(move)
        for classattr in attributes:
            label_len = len(classattr.label)
            if(classattr.label == tokens[index][:label_len]):
                if(classattr.label == "match"):
                    value = match
                else:
                    strvalue= tokens[index].replace(classattr.label + ":", "")
                    if(strvalue == "None"):
                        value = None
                    elif(strvalue == "True"):
                        value = True
                    elif(strvalue == "False"):
                        value = False
                    else:
                        try: 
                            value = int(strvalue)
                        except ValueError:
                            value = strvalue
                setattr(move, classattr.label, value)
                index += 1
        match.move_list.append(move)
        index += 1
    # -----------------------

    fobject.close()
    match.update_attributes()
    session.match = match
    prnt_match_attributes(session.match, ", ")
    prnt_board(session.match, 0)
    return True


def word_delete(session, params):
    delfile = immanuels_dir + "/" + params.strip() + ".txt"
    if os.path.isfile(delfile):
        os.remove(delfile)
    else:
        print("Error: %s file not found" % delfile)
    return True


def word_setup(session, params):
    match = session.match
    match.status = match.STATUS['setup']
    match.score = 0
    match.board.clear()
    match.move_list.clear()
    prnt_match_attributes(match, ", ")
    prnt_board(match, 0)
    print("board setup started - please set pieces")
    return True


def word_close(session, params):
    match = session.match
    if(match.status == match.STATUS['setup']):
        match.update_attributes()
        if(match.board.verify() == False):
            print("invalid position")
        else:
            match.status = match.STATUS['open']
            prnt_match_attributes(session.match, ", ")
            prnt_board(match, 0)
            print("board setup finished")
    else:
        print("wrong status")
    return True


def word_piece(session, params):
    match = session.match

    if(match.status == match.STATUS['setup']):
        tokens = params.split(" ")
        if(len(tokens) != 2):
            print("??? 2 params required.")
            return True

        try:
            piece = PIECES[tokens[0]]
        except KeyError:
            print("??? 1. param error")
            return True

        x, y = coord_to_index(tokens[1])
        if(match.board.is_inbounds(x, y) == False):
            print("??? 2. param error")
            return True
        else:
            match.board.writefield(x, y, piece)
            prnt_board(match, 0)
    else:
        print("wrong status")
    return True


def word_debug(session, params):
    match = session.match
    king = cKing(match, match.board.wKg_x, match.board.wKg_y)
    print("wKg - is_king_safe: " + str(king.is_safe()))
    king = cKing(match, match.board.bKg_x, match.board.bKg_y)
    print("bKg - is_king_safe: " + str(king.is_safe()))
    return True


def word_help(session, params):
    for dword in dictionary:
        if(dword.name == "?"):
            continue
        print(dword.name + " *** " + dword.info)
    return True


def word_bye(session, params):
    if(session.thread and session.thread_is_busy):
        print("terminate calculation. please wait...")
        session.terminate = True
        session.thread.join()
        session.thread = None
    print("bye")
    return False
