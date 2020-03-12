from src.db.misc.security import encode, decode, get_tok
def auth_user(db, name, passwd):
    c = db.cursor()
    c.execute('select motto, id, hold from user where name = ? and passwd = ?', (encode(name), passwd))
    row = c.fetchone()
    if row != None:
        return decode(row[0]), row[1], row[2]
    else:
        return None, None, None

def auth_activate(db, name, passwd, actcode):
    c = db.cursor()
    c.execute('select id from user where name is null and passwd = ?', (actcode,))
    row = c.fetchone()
    if row != None:
        c.execute('update user set name = ?, passwd = ? where id = ?', (encode(name), passwd, row[0]))
        db.commit()
        return True
    else:
        return False
def update_motto(db, uid, motto):
    c = db.cursor()
    c.execute('update user set motto = ? where id = ?', (encode(motto), uid))
    db.commit()
def update_name(db, uid, name):
    c = db.cursor()
    c.execute('update user set name = ? where id = ?', (encode(name), uid))
    db.commit()
def update_passwd(db, uid, passwd, passwd_new):
    c = db.cursor()
    c.execute('update user set passwd = ? where id = ? and passwd = ?', (passwd_new, uid, passwd))
    db.commit()
def update_visible(db, uid, v):
    c = db.cursor()
    c.execute('update user set visible = ? where id = ?', (v, uid))
    db.commit()

# Friend operations
def get_friend_code(db, uid):
    c = db.cursor()
    c.execute('select share from user where id = ?', (uid,))
    return c.fetchone()
def gen_friend_code(db, uid):
    c = db.cursor()
    # gen random token
    token = get_tok()
    # dup check
    c.execute('select count(*) from user where share = ?', (token,))
    if 0 == c.fetchone()[0]:
        # store to db
        ### Pitfall : duplication
        c.execute('update user set share = ? where id = ?', (token, uid))
        db.commit()

def new_friend(db, token, uid):
    c = db.cursor()
    # verify token
    c.execute('select id from user where share = ?', (token,))
    iid = c.fetchone()
    # narcissistic check(subscribe myself)
    if None != iid and uid != iid[0]:
        iid = iid[0]
        # void token
        c.execute('update user set share = null where id = ?', (iid,))
        # old friend check(duplication)
        c.execute('select count(*) from user_bond where uid = ? and iid = ?', (uid, iid))
        if None != c.fetchone()[0]:
            c.execute('insert into user_bond(uid, iid) values(?, ?)', (uid, iid))
            # add user bond
        db.commit()
def get_friend(db, uid):
    c = db.cursor()
    c.execute('select user_bond.iid, name from user join user_bond where user.id = iid and uid = ?', (uid,))
    return [[id, decode(name)] for id, name in c.fetchall()]
    
