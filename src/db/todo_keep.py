import time

import src.db.todo as base
from src.db.misc.security import encode, decode


tid = 2



def add_todo(db, todoid, open, close, span, repeat, is_loop):
    c = db.cursor()
    c.execute('insert into todo_keep(id, open, close, span, repeat, is_loop) values(?, ?, ?, ?, ?, ?)',
    (todoid, open, close, span, repeat, is_loop))

def create(db, uid, iid, name, after, rate, open, close, span, repeat, is_loop):
    # create a todo
    todoid = base.create(db, uid, iid, tid, encode(name), rate, after)
    # create a todo book
    add_todo(db, todoid, open, close, span, repeat, is_loop)
    db.commit()

def proof(db, uid, todoid, note, visible):
    c = db.cursor()
    # validate instructor and non-finished
    c.execute('select span, val_span, repeat, val_repeat, open, close, rate, name, is_loop from todo_keep join todo where iid = ? and val_span <> span and val_repeat <> repeat and todo.id = todo_keep.id and todo_keep.id = ?',(uid, todoid))
    row = c.fetchone()
    #print(row)
    if None == row:
        return False
    # check tim
    span, val_span, repeat, val_repeat, open, close, rate, name, is_loop = row
    curr = int(time.strftime('%H%M'))
    if curr < open or curr > close:
        return False
    # check if finished
    if val_repeat + 1 == repeat:
        # daily finished
        if val_span + 1 == span:
            # all finished
            if 0 != is_loop:
                # loop, update to zero
                c.execute('update todo_keep set val_span = 0, val_repeat = val_repeat + 1 where id = ?', (todoid,))
            else:
                # non-loop, set to finished
                c.execute('update todo_keep set val_span = val_span + 1, val_repeat = val_repeat + 1 where id = ?', (todoid,))
                c.execute('update todo set is_finished = 1 where id = ?', (todoid,))

            # release dependency anyway
            c.execute('update todo set dependency = -1 where dependency = ?', (todoid,))
            # add credit
            c.execute('update user set hold = hold + ? where id = ?', (rate, uid))
        else:
            # only daily finished
            c.execute('update todo_keep set val_span = val_span + 1, val_repeat = val_repeat + 1 where id = ?', (todoid,))
    else:
        # regular update
        c.execute('update todo_keep set val_repeat = val_repeat + 1 where id = ?', (todoid,))
    # proof
    c.execute('select name from user where id = ?', (uid,))
    uname = decode(c.fetchone()[0])
    if val_span + 1 == span and val_repeat + 1 == repeat:
        # daily finished
        c.execute('insert into pow(uid, todoid, note, proof, is_public, timestamp) values(?, ?, ?, ?, ?, datetime("now", "localtime"))', (
                uid, todoid, encode(note), encode('Keep Proof by '+uname+': '+decode(name)+'day %d of %d, daily %d of %d with %lf credits.'%(val_span+1, span, val_repeat+1, repeat, rate)), visible
                ))
    else:
        # half way done
        c.execute('insert into pow(uid, todoid, note, proof, is_public, timestamp) values(?, ?, ?, ?, ?, datetime("now", "localtime"))', (
                uid, todoid, encode(note), encode('Keep Proof by '+uname+': '+decode(name)+'day %d of %d, daily %d of %d with no credits.'%(val_span+1, span, val_repeat+1, repeat)), visible
                ))
    db.commit()
    return True

def get_by_uid_inprogress(db, uid):
    c = db.cursor()
    c.execute('select todo.id, name, span, val_span, repeat, val_repeat, open, close from todo join todo_keep where dependency = -1 and span <> val_span and repeat <> val_repeat and todo.id = todo_keep.id and tid = ? and iid = ?', (tid, uid))
    return [[id, decode(name), span, val_span, repeat, val_repeat, open, close] for id, name, span, val_span, repeat, val_repeat, open, close in c.fetchall()]
def get_by_uid_pending(db, uid):
    c = db.cursor()
    c.execute('select todo.id, name, span, val_span, repeat, val_repeat from todo join todo_keep where dependency <> -1 and todo.id = todo_keep.id and tid = ? and uid = ?', (tid, uid))
    return [[id, decode(name), span, val_span, repeat, val_repeat] for id, name, span, val_span, repeat, val_repeat in c.fetchall()]
def get_by_uid_instructed(db, uid):
    c = db.cursor()
    c.execute('select todo.id, name, span, val_span, repeat, val_repeat from todo join todo_keep where dependency = -1 and span <> val_span and repeat <> val_repeat and todo.id = todo_keep.id and tid = ? and uid <> iid and uid = ?', (tid, uid))
    return [[id, decode(name), span, val_span, repeat, val_repeat] for id, name, span, val_span, repeat, val_repeat in c.fetchall()]
def get_by_uid_finished(db, uid):
    c = db.cursor()
    c.execute('select todo.id, name, span, val_span, repeat, val_repeat from todo join todo_keep where dependency = -1 and span = val_span and todo.id = todo_keep.id and tid = ? and uid = ?', (tid, uid))
    return [[id, decode(name), span, val_span, repeat, val_repeat] for id, name, span, val_span, repeat, val_repeat in c.fetchall()]
def get_by_uid_finished_daily(db, uid):
    c = db.cursor()
    c.execute('select todo.id, name, span, val_span, repeat, val_repeat from todo join todo_keep where dependency = -1 and span <> val_span and repeat = val_repeat and todo.id = todo_keep.id and tid = ? and uid = ?', (tid, uid))
    return [[id, decode(name), span, val_span, repeat, val_repeat] for id, name, span, val_span, repeat, val_repeat in c.fetchall()]

def daily_refresh(db):
    c = db.cursor()
    # reset slacker
    c.execute('update todo_keep set val_span = 0 where span <> val_span and repeat <> val_repeat')
    # reset for today
    c.execute('update todo_keep set val_repeat = 0')
    db.commit()
