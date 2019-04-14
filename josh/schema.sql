
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS move;
DROP TABLE IF EXISTS comment;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE match (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    status INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 0,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    white_player_name TEXT NOT NULL,
    white_player_is_human INTEGER NOT NULL DEFAULT 0,
    black_player_name TEXT NOT NULL,
    black_player_is_human INTEGER NOT NULL DEFAULT 1,
    board TEXT NOT NULL DEFAULT "wRk;wKn;wBp;wQu;wKg;wBp;wKn;wRk;wPw;wPw;wPw;wPw;wPw;wPw;wPw;wPw;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;bPw;bPw;bPw;bPw;bPw;bPw;bPw;bPw;bRk;bKn;bBp;bQu;bKg;bBp;bKn;bRk;",
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE move (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    count INTEGER NOT NULL,
    move_type INTEGER NOT NULL,
    srcx INTEGER NOT NULL,
    srcy INTEGER NOT NULL,
    dstx INTEGER NOT NULL,
    dsty INTEGER NOT NULL,
    e_p_fieldx INTEGER,
    e_p_fieldy INTEGER,
    captured_piece INTEGER NOT NULL,
    prom_piece INTEGER NOT NULL,
    fifty_moves_count INTEGER NOT NULL,
    FOREIGN KEY (match_id) REFERENCES match (id)
);

CREATE TABLE comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    text TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES match (id)
);

