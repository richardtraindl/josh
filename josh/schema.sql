
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS player;
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
    guest_id INTEGER,
    status INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 0,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    board TEXT NOT NULL DEFAULT "wRk;wKn;wBp;wQu;wKg;wBp;wKn;wRk;wPw;wPw;wPw;wPw;wPw;wPw;wPw;wPw;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;bPw;bPw;bPw;bPw;bPw;bPw;bPw;bPw;bRk;bKn;bBp;bQu;bKg;bBp;bKn;bRk;",
    clockstart TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (guest_id) REFERENCES user (id)
);

CREATE TABLE player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    iswhite INTEGER NOT NULL,
    name TEXT NOT NULL,
    ishuman INTEGER NOT NULL,
    consumedsecs INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT fk_match FOREIGN KEY (match_id) REFERENCES match(id) ON DELETE CASCADE
);

CREATE TABLE move (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    count INTEGER NOT NULL,
    iscastling INTEGER NOT NULL,
    srcfield TEXT NOT NULL,
    dstfield TEXT NOT NULL,
    enpassfield TEXT,
    captpiece TEXT NOT NULL,
    prompiece TEXT,
    CONSTRAINT fk_match FOREIGN KEY (match_id) REFERENCES match(id) ON DELETE CASCADE
);

CREATE TABLE comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    text TEXT NOT NULL,
    CONSTRAINT fk_match FOREIGN KEY (match_id) REFERENCES match(id) ON DELETE CASCADE
);
