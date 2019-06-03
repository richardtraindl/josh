
def reverse_lookup(dic, value):
    for key in dic:
        if dic[key] == value:
            return key
    return None


def coord_to_index(coord):
    if(ord(coord[0]) > ord('H')):
        x = ord(coord[0]) - ord('a')
    else:
        x = ord(coord[0]) - ord('A')
    y = ord(coord[1]) - ord('1')
    return (x + y * 8)


def index_to_coord(idx):
    x = idx % 8 
    y = idx // 8
    col = chr(x + ord('a'))
    row = chr(y + ord('1'))
    coord = str(col + row)
    return coord

