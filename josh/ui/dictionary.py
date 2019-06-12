
import re, os, threading, copy
from engine.values import *
from engine.match import *
from engine.move import *
from engine.compute.calc import calc_move
from engine.pieces.king import cKing
from engine.debug import prnt_match_attributes, prnt_board, list_match_attributes, list_move_attributes
from engine.helper import coord_to_index, reverse_lookup


dictionary = []
immanuels_dir = "c:\\wse4\\tmp" #"/home/richard/.immanuel"


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
        if(len(self.match.minutes) > 0 and len(self.session.candidates) >= 2):
            last_move = self.match.minutes[-1]
            first_candidate = self.session.candidates[0]
            if(first_candidate.src == last_move.src and
               first_candidate.dst == last_move.dst and
               first_candidate.prompiece == last_move.prompiece):
                second_candidate = self.session.candidates[1]
        candidates = calc_move(self.match, second_candidate)
        self.session.candidates.clear()
        if(len(candidates) > 0):
            gmove = candidates[0]
            self.session.match.do_move(gmove.src, gmove.dst, gmove.prompiece)
            if(len(candidates) >= 3):
                self.session.candidates.append(candidates[1])
                self.session.candidates.append(candidates[2])
            prnt_board(self.session.match)
        else:
            print("no move found!")
        self.session.thread_isbusy = False


def calc_and_domove(session):
    match = session.match
    status = match.evaluate_status()
    if(session.thread_isbusy == False and session.status == 0 and
       status == match.STATUS['active'] and 
       ((match.next_color() == COLORS['white'] and session.wplayer_ishuman == False) or
        (match.next_color() == COLORS['black'] and session.bplayer_ishuman == False))):
        session.thread = CalcThread(session)
        session.thread.start()
    else:
        if(status == match.STATUS['draw'] or
           status == match.STATUS['winner_white'] or 
           status == match.STATUS['winner_black']):
            print(reverse_lookup(match.STATUS, match.evaluate_status()))


def word_pause(session, params):
    match = session.match
    if(match.evaluate_status() == match.STATUS['active'] and session.status == 0):
        session.status = 1
    return True


def word_resume(session, params):
    match = session.match
    if(session.status == 1):
        session.status = 0
    calc_and_domove(session)
    return True


def word_show(session, params):
    prnt_match_attributes(session.match, ", ")
    prnt_board(session.match)
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
            session.wplayer_ishuman = True
        elif(params == "black"):
            session.bplayer_ishuman = True
        elif(params == "all"):
            session.wplayer_ishuman = True
            session.bplayer_ishuman = True
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
            session.wplayer_ishuman = False
        elif(params == "black"):
            session.bplayer_ishuman = False
        elif(params == "all"):
            session.wplayer_ishuman = False
            session.bplayer_ishuman = False
        else:
            print("??? " + msg)
    return True


def word_move(session, params):
    match = session.match
    match.status = match.evaluate_status()
    if(match.status != match.STATUS['active']):
        print("??? " + reverse_lookup(match.STATUS, match.status))
        return True
    if(((match.next_color() == COLORS['white'] and session.wplayer_ishuman == False) or
        (match.next_color() == COLORS['black'] and session.bplayer_ishuman == False))):
        print("??? wrong color")
        return True

    prompiece = "blk"

    matchobj = re.search(r"^\s*(?P<src>[a-hA-H][1-8])\s*[-xX]*\s*(?P<dst>[a-hA-H][1-8])\s*$", params)
    if(matchobj):
        src = coord_to_index(matchobj.group("src"))
        dst = coord_to_index(matchobj.group("dst"))
    else:
        matchobj = re.search(r"^\s*(?P<src>[a-hA-H][1-8])\s*[-xX]*\s*(?P<dst>[a-hA-H][1-8])\s*[-,;]*\s*(?P<prom>\w+)\s*$", params)
        if(matchobj):
            src = coord_to_index(matchobj.group("src"))
            dst = coord_to_index(matchobj.group("dst"))
            prompiece = matchobj.group("prom")

            valid = False
            for piece in PIECES:
                if(piece == prompiece):
                    valid = True
                    break
            if(valid == False):
                return True
        else:
            matchobj = re.search(r"^\s*(?P<short>[0oO][-][0oO])\s*$", params)
            if(matchobj):
                if(match.next_color() == COLORS['white']):
                    src = match.board.wKg
                else:
                    src = match.board.bKg
                dst = src + 2
            else:
                matchobj = re.search(r"^\s*(?P<long>[0oO][-][0oO][-][0oO])\s*$", params)
                if(matchobj):
                    if(match.next_color() == COLORS['white']):
                        src = match.board.wKg
                    else:
                        src = match.board.bKg
                    dst = src - 2
                else:
                    return True

    if(match.is_move_valid(src, dst, PIECES[prompiece])[0]):
        match.do_move(src, dst, PIECES[prompiece])
        prnt_board(match)
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
    prnt_board(match)
    if(match.evaluate_status() == match.STATUS['active']):
        session.status = 1
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
        fobject = open(immanuels_dir + "\counter.txt", "r")
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
    prnt_board(session.match)
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
    session.status = 2
    match.score = 0
    match.board.clear()
    match.minutes.clear()
    prnt_match_attributes(match, ", ")
    prnt_board(match)
    print("board setup started - please set pieces")
    return True


def word_close(session, params):
    match = session.match
    if(session.status ==2):
        match.update_attributes()
        if(match.board.verify() == False):
            print("invalid position")
        else:
            session.status = 0
            prnt_match_attributes(session.match, ", ")
            prnt_board(match)
            print("board setup finished")
    else:
        print("wrong status")
    return True


def word_piece(session, params):
    match = session.match

    if(session.status == 2):
        tokens = params.split(" ")
        if(len(tokens) != 2):
            print("??? 2 params required.")
            return True

        try:
            piece = PIECES[tokens[0]]
        except KeyError:
            print("??? 1. param error")
            return True

        idx = coord_to_index(tokens[1])
        if(idx < 0 or idx > 63):
            print("??? 2. param error")
            return True
        else:
            match.board.setfield(idx, piece)
            prnt_board(match)
    else:
        print("wrong status")
    return True


def word_debug(session, params):
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
