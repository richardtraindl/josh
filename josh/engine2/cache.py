import os

immanuels_dir = "/home/richard/.immanuel"

def save_cache(match):
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
