
#include <map>
#include <string>

using namespace std;

typedef map<string, int> MapStrInt;
typedef map<int, int> MapIntInt;
typedef map<int, string> MapIntStr;

int coord_to_index(coord){
    if(ord(coord[0]) > ord('H')){
        x = ord(coord[0]) - ord('a');
    }
    else{
        x = ord(coord[0]) - ord('A');
    }
    y = ord(coord[1]) - ord('1');
    return (x + y * 8);
};

int index_to_coord(idx){
    x = idx % 8;
    y = idx // 8;
    col = chr(x + ord('a'));
    row = chr(y + ord('1'));
    coord = str(col + row);
    return coord;
};
