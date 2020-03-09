import sqlite3
from src.db.misc.security import encode, decode
# this file is a database driver

# connect database

db = 'db.db3'

def connect():
    return sqlite3.connect(db)
def close(db):
    db.close()

def dump_pow(db):
    c = db.cursor()
    c.execute('select proof, note, timestamp from pow')
    return [[decode(proof), decode(note), timestamp] for proof, note, timestamp in c.fetchall()]

def dump_pow_user_fence(db, uid):
    c = db.cursor()
    c.execute('select proof, note, timestamp from pow where uid = ? or is_public = 1', (uid,))
    return [[decode(proof), decode(note), timestamp] for proof, note, timestamp in c.fetchall()]
def dump_user(db):
    c = db.cursor()
    c.execute('select name, motto from user where name is not null')
    return [[decode(name), motto] for name, motto in c.fetchall()]
def dump_user_visible(db):
    c = db.cursor()
    c.execute('select name, motto from user where name is not null and visible = 1')
    return [[decode(name), decode(motto)] for name, motto in c.fetchall()]
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