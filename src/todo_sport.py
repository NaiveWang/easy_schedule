from flask import Blueprint, render_template, request, redirect, flash, session

import src.db.driver as dbd
from src.conf import sess_rej, version

import src.db.todo_sport as todo

from src.db.misc.image import img2bytes

todo_sport = Blueprint('todo_sport', __name__)

@todo_sport.route('/todo_sport', methods = ['GET'])
def todo_sport_get():
    if session.get('login'):
        db = dbd.connect()
        return render_template('todo_sport.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                opened = todo.get_by_uid_opened(db, session.get('uid')),
                                instructed = todo.get_by_uid_instructed(db, session.get('uid')),
                                pending = todo.get_by_uid_pending(db, session.get('uid')))
    else:
        flash(sess_rej)
        return redirect('/login')

@todo_sport.route('/proof_todo_sport', methods = ['GET'])
def proof_todo_sport_get():
    if session.get('login'):
        db = dbd.connect()
        # check user violation
        return render_template('/proof_todo_sport.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                id = request.args['id'],
                                val = float(request.args['val']))
    else:
        flash(sess_rej)
        return redirect('/login')
@todo_sport.route('/proof_todo_sport', methods = ['POST'])
def proof_todo_sport_post():
    if session.get('login'):
        # check user volation
        db = dbd.connect()
        if dbd.check_own_by_id(db, request.form['id'], session.get('uid')):
            # proof
            if request.files['img'].read() == b'':
                todo.proof(db, float(request.form['val']), session.get('uid'), request.form['id'], request.form['proof'], int(request.form['v']))
            else:
                # check image
                img_valid, img_b = img2bytes(request.files['img'])
                if img_valid:
                    todo.proof(db, float(request.form['val']), session.get('uid'), request.form['id'], request.form['proof'], int(request.form['v']), img_b)
                else:
                    flash('Unsupported Image.')

            # return to dashboard
            return redirect('/todo_sport')
    flash('Encountering user fence violation, force log out')
    return redirect('/logout')

# request handlers
@todo_sport.route('/new_todo_sport', methods = ['POST'])
def new_todo_sport_post():
    #auth user
    if session.get('login'):
        db = dbd.connect()
        todo.create(db,
            session.get('uid'),
            request.form['iid'],
            request.form['name'] + ' : ' + request.form['unit'],
            float(request.form['goal']),
            request.form['after'],
            request.form['rate'])
        return redirect('/todo_sport')
    else:
        flash(sess_rej)
        return redirect('/login')
@todo_sport.route('/peek_todo_sport', methods = ['GET'])
def peek_todo_sport_get():
    if session.get('login'):
        db = dbd.connect()
        # check user permission by todo (base info)
        if dbd.check_upermission_todo(db, session.get('uid'), request.args['id']):
            # get special data
            info = todo.get_info(db, request.args['id'])
            if None ==  info:
                # type error
                flash('Todo Type Violation.')
                return redirect('/todo_sport')
            else:
                dep = None if info[4] == -1 else dbd.get_todo_with_type(db, info[4])
                return render_template('peek_todo_sport.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                powdump = dbd.dump_pow_todo_fence(db, request.args['id']),
                                info = info,
                                dep = dep)
        else:
            flash('Permission Denied / No Book Todo Found')
            return redirect('/todo_sport')
    else:
        flash(sess_rej)
        return redirect('/login')
