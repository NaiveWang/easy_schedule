import src.db.todo as base
from src.db.misc.security import encode, decode
tid = 3

def add_todo(db, todoid, goal):
    c = db.cursor()
    # val is initialized to 0 at DB end
    c.execute('insert into todo_sport(id, goal) values(?, ?)',
    (todoid, goal))

def create(db, uid, iid, name, goal, after, rate=1):
    # create a todo
    todoid = base.create(db, uid, iid, tid, encode(name), rate, after)
    # create a todo book
    add_todo(db, todoid, goal)
    db.commit()
def proof(db, val, uid, todoid, note, visible):
    # check if valid
    c = db.cursor()
    c.execute('select val, goal, rate, name from todo_sport join todo where iid = ? and todo.id = todo_sport.id and todo_sport.id = ?',(uid, todoid))
    row = c.fetchone()
    #print(row)
    if None == row:
        return False
    # valid, update value
    c.execute('update todo_sport set val = val + ? where id = ?', (val, todoid))
    # check if it has been finished

    if val + row[0] >= row[1]:
        # value overflow
        # update todo to finished
        c.execute('update todo set is_finished = 1 where id = ?', (todoid,))
        # release pending todos
        c.execute('update todo set dependency = -1 where dependency = ?', (todoid,))

    # update credit
    c.execute('update user set hold = hold + ? where id = ?', (row[2] * val, uid))
    # proof
    c.execute('select name from user where id = ?', (uid,))
    name = decode(c.fetchone()[0])
    c.execute('insert into pow(uid, todoid, note, proof, is_public, timestamp) values(?, ?, ?, ?, ?, datetime("now", "localtime"))',
        (uid, todoid, encode(note), encode('Sport Proof by: '+name+': '+decode(row[3])+' from %lf to %lf with %lf credit'%(row[0], row[0] + val, row[2] * val)), visible))
    db.commit()
def get_by_uid_opened(db, uid):
    c = db.cursor()
    c.execute('select todo.id, name, val, goal from todo join todo_sport where dependency = -1 and todo.id = todo_sport.id and tid = ? and iid = ?', (tid, uid))
    return [[id, decode(name), val, goal] for id, name, val, goal in c.fetchall()]
def get_by_uid_pending(db, uid):
    c = db.cursor()
    c.execute('select todo.id, name, val, goal from todo join todo_sport where dependency <> -1 and todo.id = todo_sport.id and tid = ? and iid = ?', (tid, uid))
    return [[id, decode(name), val, goal] for id, name, val, goal in c.fetchall()]
def get_by_uid_instructed(db, uid):
    c = db.cursor()
    c.execute('select todo.id, name, val, goal from todo join todo_sport where dependency = -1  and todo.id = todo_sport.id and tid = ? and uid <> iid and uid = ?', (tid, uid))
    return [[id, decode(name), val, goal] for id, name, val, goal in c.fetchall()]
