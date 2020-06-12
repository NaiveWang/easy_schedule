import sqlite3
from src.db.misc.security import encode, decode, hash
# this file is a database driver

# connect database

db = 'db.db3'
def connect():
    return sqlite3.connect(db)
def close(db):
    db.close()

# in friend group\self\visible
def check_upermission_user(db, uid, userid):
    c = db.cursor()

    c.execute('select count(*) from user_bond where uid = ? and iid = ?', (uid, userid))
    is_friend = c.fetchone()[0]
    c.execute('select count(*) from user where visible <> 0 and id = ?', (userid,))
    is_visible = c.fetchone()[0]
    if 0 == is_friend and int(uid) != int(userid) and 0 == is_visible:
        print('false')
        return False
    else:
        return True
def check_upermission_todo(db, uid, todoid):
    c = db.cursor()
    c.execute('select count(*) from user_bond join todo where user_bond.uid = ? and user_bond.iid = todo.uid and todo.id = ?', (uid, todoid))
    is_friend = c.fetchone()[0]
    # instructor is granted by default
    c.execute('select count(*) from todo where (uid = ? and id = ?) or (iid = ? and id = ?)', (uid, todoid, uid, todoid))
    is_myself = c.fetchone()[0]
    c.execute('select count(*) from user join todo where visible <> 0 and todo.uid = user.id and todo.id = ?', (todoid,))
    is_visible = c.fetchone()[0]
    if 0 == is_friend and 0 == is_myself and 0 == is_visible:
        return False
    else:
        return True
def check_upermission_pow(db, uid, powid):
    c = db.cursor()
    c.execute('select count(*) from user_bond join pow where user_bond.uid = ? and user_bond.iid = pow.uid and pow.id = ? and is_public <> 0', (uid, powid))
    is_friend = c.fetchone()[0]
    c.execute('select count(*) from pow where uid = ? and id = ?', (uid, powid))
    is_myself = c.fetchone()[0]
    c.execute('select count(*) from user join pow where visible <> 0 and pow.uid = user.id and pow.id = ?', (powid,))
    is_visible = c.fetchone()[0]
    if 0 == is_friend and 0 == is_myself and 0 == is_visible:
        return False
    else:
        return True

def get_uinfo(db, uid):
    c = db.cursor()
    c.execute('select name, motto, hold from user where id = ?', (uid,))
    name, motto, hold = c.fetchone()
    return decode(name), decode(motto), hold



def get_pow(db, pid):
    c = db.cursor()
    # check
    c.execute('select proof, note, timestamp from pow where id = ?', (pid,))
    row = c.fetchone()
    if None == row:

        return False
    proof, note, timestamp = row
    return decode(proof), decode(note), timestamp, hash(proof), hash(note)

def get_todo_with_type(db, todoid):
    c = db.cursor()
    c.execute('select todo.name, todo_t.name from todo join todo_t where todo_t.id = todo.tid and todo.id = ?', (todoid,))

    name, tname = c.fetchone()
    return decode(name), tname

def dump_todo_user_progress(db, uid):
    c = db.cursor()
    c.execute('select todo.id, todo_t.name, todo.name from todo join todo_t where todo.tid = todo_t.id and is_finished = 0 and uid = ?', (uid,))
    return [[id, tname, decode(name)] for id, tname, name in c.fetchall()]
def dump_todo_user_finished(db, uid):
    c = db.cursor()
    c.execute('select todo.id, todo_t.name, todo.name from todo join todo_t where todo.tid = todo_t.id and is_finished <> 0 and uid = ?', (uid,))
    return [[id, tname, decode(name)] for id, tname, name in c.fetchall()]
def dump_pow_user_fence(db, uid):
    c = db.cursor()
    c.execute('select id, proof, timestamp from pow where uid = ?', (uid,))
    return [[id, decode(proof), timestamp] for id, proof, timestamp in c.fetchall()]
def dump_pow_me_fence(db, uid):
    c = db.cursor()
    # by default only fetch first 30
    c.execute('select distinct(pow.id), proof, timestamp from pow join user_bond where (pow.uid = ?) or (pow.uid = user_bond.iid and user_bond.uid = ? and is_public <> 0) order by pow.id desc limit 30', (uid, uid))
    return [[id, decode(proof), timestamp] for id, proof, timestamp in c.fetchall()]
def dump_pow_todo_fence(db, todoid):
    c = db.cursor()
    c.execute('select id, proof, timestamp from pow where is_public <> 0 and todoid = ?', (todoid,))
    return [[id, decode(proof), timestamp] for id, proof, timestamp in c.fetchall()]
def dump_user(db):
    c = db.cursor()
    c.execute('select name, motto from user where name is not null')
    return [[decode(name), motto] for name, motto in c.fetchall()]

def dump_user_visible(db):
    c = db.cursor()
    c.execute('select name, motto from user where name is not null and visible = 1')
    return [[decode(name), decode(motto)] for name, motto in c.fetchall()]
def get_user(db, uid):
    c = db.cursor()
    c.execute('select name, motto from user where id = ?', (uid,))
    u = c.fetchone()
    if None ==  u:
        return False

    return decode(u[0]), decode(u[1])

def dump_user_visible_hub(db):
    c = db.cursor()
    c.execute('select id, name from user where name is not null and visible = 1')
    return [[id, decode(name)] for id, name in c.fetchall()]
def get_type(db):
    c = db.cursor()
    c.execute('select id, name from todo_t')
    return dict(c.fetchall())
def check_own_by_id(db, todoid, iid):
    c = db.cursor()
    c.execute('select uid from todo where iid = ? and id = ?', (iid, todoid))
    if None != c.fetchone():
        return True
    else:
        return False

# for dependency use
def get_nfinished_by_uid(db, uid):
    c = db.cursor()
    c.execute('select id, name from todo where is_finished = 0 and uid = ?', (uid,))
    return [[id, decode(name)] for id, name in c.fetchall()]
def get_user_avali_credit(db, uid):
    c = db.cursor()
    c.execute('select id, name from credit where is_spent = 0 and uid = ?', (uid,))
    return [[id, decode(name)] for id, name in c.fetchall()]
# credit

def credit_create(db, uid, name, price, after):
    c = db.cursor()
    c.execute('insert into credit(uid, name, price, dependency) values(?, ?, ?, ?)', (uid, encode(name), price, after))
    db.commit()
def credit_get_finished(db, uid):
    c = db.cursor()
    c.execute('select name, price, timestamp from credit where is_spent <> 0 and uid = ?', (uid,))
    return [[decode(name), price, timestamp] for name, price, timestamp in c.fetchall()]
def credit_get_pending(db, uid):
    c = db.cursor()
    c.execute('select name, price from credit where dependency <> -1 and uid = ?', (uid,))
    return [[decode(name), price] for name, price in c.fetchall()]
def credit_get_avaliable(db, uid, hold):
    c = db.cursor()
    c.execute('select id, name, price from credit where dependency = -1 and is_spent = 0 and ? >= price and uid = ?', (hold, uid))
    return [[id, decode(name), price] for id, name, price in c.fetchall()]
def credit_get_inprogress(db, uid, hold):
    c = db.cursor()
    c.execute('select name, price, ? from credit where dependency = -1 and ? < price and uid = ?', (hold, hold, uid))
    return [[decode(name), price, u] for name, price, u in c.fetchall()]
def credit_spend(db, uid, cid):
    c = db.cursor()
    # get user credit
    c.execute('select hold from user where id = ?', (uid,))
    credit = c.fetchone()[0]
    # check user credit is enough (get credit)
    c.execute('select price from credit where id = ?', (cid,))
    cost = c.fetchone()[0]
    if credit >=  cost:
        # loot user
        c.execute('update user set hold = hold - ? where id = ?', (cost, uid))
        # mark credit to spent
        c.execute('update credit set is_spent = 1, timestamp = datetime("now", "localtime") where id = ?', (cid,))
        # cond : check dependency
        c.execute('update credit set dependency = -1 where dependency = ?', (cid,))
        db.commit()

# used for man page
def dump_todo_user(db, uid):
    c = db.cursor()
    c.execute('select id, name, trash from todo where uid = ?', (uid,))
    return [[id, decode(name), trash] for id, name, trash in c.fetchall()]
def dump_credit_user(db, uid):
    c = db.cursor()
    c.execute('select id, name, trash from credit where uid = ?', (uid,))
    return [[id, decode(name), trash] for id, name, trash in c.fetchall()]
def dump_pow_user(db, uid):
    c = db.cursor()
    c.execute('select id, proof, timestamp, trash from pow where uid = ?', (uid,))
    return [[id, decode(proof), timestamp, trash] for id, proof, timestamp, trash in c.fetchall()]
def dump_bond_user(db, uid):
    c = db.cursor()
    c.execute('select user_bond.id, name from user join user_bond where user.id = iid and user_bond.uid = ?', (uid,))
    return [[id, decode(name)] for id, name in c.fetchall()]
# trash stash
def set_trash_pow(db, id, uid, val):
    c = db.cursor()
    c.execute('update pow set trash = ? where uid = ? and id = ?', (val, uid, id))
    db.commit()
def set_trash_credit(db, id, uid, val):
    c = db.cursor()
    c.execute('update credit set trash = ? where uid = ? and id = ?', (val, uid, id))
    db.commit()
def set_trash_todo(db, id, uid, val):
    c = db.cursor()
    c.execute('update todo set trash = ? where uid = ? and id = ?', (val, uid, id))
    db.commit()

def delete_pow(db, id, uid):
    c = db.cursor()
    c.execute('delete from pow where trash <> 0 and uid = ? and id = ?', (uid, id))
    db.commit()
def delete_credit(db, id, uid):
    c = db.cursor()
    # proof id and trash
    c.execute('select trash, dependency from credit where uid = ? and id = ?', (uid, id))
    is_trash = c.fetchone()
    if None != is_trash and 0 != is_trash[0]:
        # pull dependency
        c.execute('update credit set dependency = ? where dependency = ?', (is_trash[1], id))
        # delete
        c.execute('delete from credit where id = ?', (id,))
        db.commit()
def delete_todo(db, id, uid):
    c = db.cursor()
    # proof id
    c.execute('select trash, dependency, todo_t.name from todo join todo_t where todo_t.id = tid and uid = ? and todo.id = ?', (uid, id))
    is_trash = c.fetchone()
    if None != is_trash and 0 != is_trash[0]:
        # pull dependency
        c.execute('update todo set dependency = ? where dependency = ?', (is_trash[1], id))
        # delete down stream
        c.execute('delete from todo_%s where id = ?'%(is_trash[2]), (id,))
        # delete
        c.execute('delete from todo where id = ?', (id,))
        db.commit()
def delete_bond(db, id, uid):
    c = db.cursor()
    c.execute('delete from user_bond where uid = ? and id = ?', (uid, id))
    db.commit()
