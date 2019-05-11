
sqldrops = (
    """DROP TABLE IF EXISTS auth_user CASCADE;""",
    """DROP TABLE IF EXISTS match CASCADE;""",
    """DROP TABLE IF EXISTS player CASCADE;""",
    """DROP TABLE IF EXISTS move CASCADE;""",
    """DROP TABLE IF EXISTS comment CASCADE;""")


sqlcreates = (
    """CREATE TABLE auth_user (id SERIAL PRIMARY KEY, \
        username VARCHAR(50) NOT NULL, \
        password VARCHAR(256) NOT NULL, UNIQUE(username));""",
    """CREATE TABLE match (id SERIAL PRIMARY KEY, \
       auth_user_id INTEGER REFERENCES auth_user(id), \
       auth_guest_id INTEGER REFERENCES auth_user(id), \
       status INTEGER NOT NULL DEFAULT 0, \
       level INTEGER NOT NULL DEFAULT 0, \
       created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
       board VARCHAR(256) NOT NULL DEFAULT 'wRk;wKn;wBp;wQu;wKg;wBp;wKn;wRk;wPw;wPw;wPw;wPw;wPw;wPw;wPw;wPw;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;blk;bPw;bPw;bPw;bPw;bPw;bPw;bPw;bPw;bRk;bKn;bBp;bQu;bKg;bBp;bKn;bRk;');""",
    """CREATE TABLE player (id SERIAL PRIMARY KEY, \
       match_id INTEGER REFERENCES match(id) ON DELETE CASCADE, \
       iswhite BOOLEAN NOT NULL, \
       name VARCHAR(50) NOT NULL, \
       ishuman BOOLEAN NOT NULL, \
       consumedsecs INTEGER NOT NULL DEFAULT 0);""",
    """CREATE TABLE move (id SERIAL PRIMARY KEY, \
        match_id INTEGER REFERENCES match(id) ON DELETE CASCADE, \
        count INTEGER NOT NULL, \
        srcfield VARCHAR(2) NOT NULL, \
        dstfield VARCHAR(2) NOT NULL, \
        enpassfield VARCHAR(2), \
        srcpiece VARCHAR(3) NOT NULL, \
        captpiece VARCHAR(3) NOT NULL, \
        prompiece VARCHAR(3));""",
    """CREATE TABLE comment (id SERIAL PRIMARY KEY, \
       match_id INTEGER REFERENCES match(id) ON DELETE CASCADE, \
       created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
       text VARCHAR(256) NOT NULL);""")
