def create(db, uid, iid, tid, name, rate, after):
    c = db.cursor()
    c.execute('insert into todo(uid, iid, tid, name, rate, dependency) values(?, ?, ?, ?, ?, ?)', (uid, iid, tid, name, rate, after))
    #db.commit()
    return c.lastrowid
def delete(db, todoid):
    c = db.cursor()
    c.execute('delete from todo where id = ?', (todoid,))
    db.commit()
def get_by_uid(db, uid):
    c = db.cursor()
    c.execute('select id, todo_t.name, name, rate from todo join todo_t where todo_t.id = tid and uid = ?', (uid,))
