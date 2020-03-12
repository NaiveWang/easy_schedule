from flask import Blueprint, render_template, request, redirect, flash, session
import time
import src.db.driver as dbd
from src.conf import sess_rej, version

import src.db.todo_keep as todo

todo_keep = Blueprint('todo_keep', __name__)



def keep_daily_refresh():
    # update at 00:00
    todo.daily_refresh(dbd.connect())


@todo_keep.route('/todo_keep', methods = ['GET'])
def todo_keep_get():
    if session.get('login'):
        db = dbd.connect()
        return render_template('todo_keep.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                inprogress = todo.get_by_uid_inprogress(db, session.get('uid')),
                                finished = todo.get_by_uid_finished(db, session.get('uid')),
                                finished_daily = todo.get_by_uid_finished_daily(db, session.get('uid')),
                                pending = todo.get_by_uid_pending(db, session.get('uid')),
                                instructed = todo.get_by_uid_instructed(db, session.get('uid')))
    else:
        flash(sess_rej)
        return redirect('/login')

@todo_keep.route('/new_todo_keep', methods = ['POST'])
def new_todo_keep_post():
    #auth user
    if session.get('login'):
        db = dbd.connect()
        todo.create(db,
            session.get('uid'),
            request.form['iid'],
            request.form['name'],
            request.form['after'],
            request.form['rate'],
            int(request.form['open'].replace(':', '')),
            int(request.form['close'].replace(':', '')),
            request.form['span'],
            request.form['repeat'],
            request.form['is_loop'],
            )
        return redirect('/todo_keep')
    else:
        flash(sess_rej)
        return redirect('/login')
@todo_keep.route('/proof_todo_keep', methods = ['GET'])
def proof_todo_keep_get():
    if session.get('login'):
        db = dbd.connect()
        # check user violation
        return render_template('/proof_todo_keep.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                id = request.args['id'])
    else:
        flash(sess_rej)
        return redirect('/login')
@todo_keep.route('/proof_todo_keep', methods = ['POST'])
def proof_todo_keep_post():
    if session.get('login'):
        # check user volation
        db = dbd.connect()
        if dbd.check_own_by_id(db, request.form['id'], session.get('uid')):
            # proof
            if not todo.proof(db, session.get('uid'), request.form['id'], request.form['proof'], int(request.form['v'])):
                # return to dashboard
                flash('Time violation or unnecessary repeat.')
            return redirect('/todo_keep')
    flash('Encountering user fence violation, force log out')
    return redirect('/logout')
@todo_keep.route('/peek_todo_keep', methods = ['GET'])
def peek_todo_keep_get():
    if session.get('login'):
        db = dbd.connect()
        # check user permission by todo (base info)
        return render_template('peek_todo_keep.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                powdump = dbd.dump_pow_todo_fence(db, request.args['id']))
    else:
        flash(sess_rej)
        return redirect('/login')
