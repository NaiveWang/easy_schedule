import src.db.todo as base
from src.db.misc.security import encode, decode
tid = 3

def add_todo(db, todoid, start, end):
    c = db.cursor()
    c.execute('insert into todo_sport(id, start, end, val) values(?, ?, ?, ?)',
    (todoid, start, end, start))

def create(db, uid, iid,  name, page_start, page_end, after, rate=1):
    # create a todo
    todoid = base.create(db, uid, iid, tid, encode(name), rate, after)
    # create a todo book
    add_todo(db, todoid, page_start, page_end)
    db.commit()
def proof(db, val, uid, todoid, note, visible):
    # check if valid
    c = db.cursor()
    c.execute('select val, end, rate, name from todo_book join todo where iid = ? and todo.id = todo_book.id and todo_book.id = ?',(uid, todoid))
    row = c.fetchone()
    #print(row)
    if None == row or val <= row[0] or val > row[1]:
        return False
    # valid, update value
    c.execute('update todo_book set val = ? where id = ?', (val, todoid))
    # check if it has been finished

    if val == row[1]:
        # value equals to end
        # update todo to finished
        c.execute('update todo set is_finished = 1 where id = ?', (todoid,))
        # release pending todos
        c.execute('update todo set dependency = -1 where dependency = ?', (todoid,))

    # update credit
    c.execute('update user set hold = hold + ? where id = ?', (row[2] * (val - row[0]), uid))
    # proof
    c.execute('select name from user where id = ?', (uid,))
    name = decode(c.fetchone()[0])
    c.execute('insert into pow(uid, todoid, note, proof, is_public, timestamp) values(?, ?, ?, ?, ?, datetime("now", "localtime"))',
        (uid, todoid, encode(note), encode(name+': '+decode(row[3])+' from %d to %d with %lf credit'%(row[0], val, row[2] * (val - row[0]))), visible))
    db.commit()
