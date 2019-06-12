import sys
from . dictionary import *


class Session:
    def __init__(self, match=None):
        self.thread = None
        self.thread_is_busy = False
        self.match = match
        self.candidate_list = []


def interpret(session, inputstr):
    inputstr = inputstr.strip()
    if(len(inputstr) == 0):
        return True

    tokens = inputstr.split(" ", 1)
    if(len(tokens) == 2):
        params = tokens[1]
    else:
        params = ""

    for dword in dictionary:
        if(dword.name == tokens[0].lower()):
            return dword.code(session, params)
    print("???")
    return True


def forth():
    session = Session(cMatch())
    init_words()

    while(True):
        calc_and_domove(session)
        inputstr = input("OK ")
        if(interpret(session, inputstr) == False):
            break
