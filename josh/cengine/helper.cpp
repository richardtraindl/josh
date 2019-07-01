
#include <map>
#include <string>

using namespace std;

typedef map<string, int> MapStrInt;
typedef map<int, int> MapIntInt;
typedef map<int, string> MapIntStr;

int coord_to_index(coord){
    if((int)coord[0] > (int)'H'){
        int x = (int)coord[0] - (int)'a');
    }
    else{
        int x = (int)coord[0] - (int)'A';
    }
    int y = (int)coord[1] - (int)'1';
    return (x + y * 8);
};

int index_to_coord(idx){
    int x = idx % 8;
    int y = idx // 8;
    char col = (x + (int)'a');
    char row = (y + (int)'1');
    coord = col + row;
    return coord;
};
