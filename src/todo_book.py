from flask import Blueprint, render_template, request, redirect, flash, session

import src.db.driver as dbd
from src.conf import sess_rej, version

import src.db.todo_book as todo

todo_book = Blueprint('todo_book', __name__)

@todo_book.route('/todo_book', methods = ['GET'])
def todo_book_get():
    if session.get('login'):
        db = dbd.connect()
        return render_template('todo_book.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                todo_books = todo.get_by_uid_todo(db, session.get('uid')),
                                finished_books = todo.get_by_uid_finished(db, session.get('uid')),
                                pending_books = todo.get_by_uid_pending(db, session.get('uid')),
                                instructed_books = todo.get_by_uid_instructed(db, session.get('uid')))
    else:
        flash(sess_rej)
        return redirect('/login')

@todo_book.route('/proof_todo_book', methods = ['GET'])
def proof_todo_book_get():
    if session.get('login'):
        db = dbd.connect()
        # check user violation
        return render_template('/proof_todo_book.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                id = request.args['id'],
                                val = int(request.args['val']),
                                end = request.args['end'])
    else:
        flash(sess_rej)
        return redirect('/login')
@todo_book.route('/proof_todo_book', methods = ['POST'])
def proof_todo_book_post():
    if session.get('login'):
        # check user volation
        db = dbd.connect()
        if dbd.check_own_by_id(db, request.form['id'], session.get('uid')):
            # proof
            todo.proof(db, int(request.form['val']), session.get('uid'), request.form['id'], request.form['proof'], int(request.form['v']))
            # return to dashboard
            return redirect('/todo_book')
    flash('Encountering user fence violation, force log out')
    return redirect('/logout')

# request handlers
@todo_book.route('/new_todo_book', methods = ['POST'])
def new_todo_book_post():
    #auth user
    if session.get('login'):
        db = dbd.connect()
        todo.create(db,
            session.get('uid'),
            request.form['iid'],
            request.form['name'],
            request.form['start'],
            request.form['end'],
            request.form['after'],
            request.form['rate'])
        return redirect('/todo_book')
    else:
        flash(sess_rej)
        return redirect('/login')
@todo_book.route('/peek_todo_book', methods = ['GET'])
def peek_todo_book_get():
    if session.get('login'):
        db = dbd.connect()
        # check user permission by todo (base info)
        return render_template('peek_todo_book.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                powdump = dbd.dump_pow_todo_fence(db, request.args['id']))
    else:
        flash(sess_rej)
        return redirect('/login')
