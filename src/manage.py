from flask import Blueprint, render_template, request, redirect, flash, session
import src.db.driver as dbd
from src.conf import sess_rej, version

manage = Blueprint('manage', __name__)

@manage.route('/manage', methods = ['GET'])
def manage_get():
    if session.get('login'):
        db = dbd.connect()
        return render_template('manage.html',
                                user = session.get('user'),
                                motto = session.get('motto'),
                                credit = session.get('credit'),
                                version = version,
                                todo = dbd.dump_todo_user(db, session.get('uid')),
                                credito = dbd.dump_credit_user(db, session.get('uid')),
                                pow = dbd.dump_pow_user(db, session.get('uid')),
                                bond = dbd.dump_bond_user(db, session.get('uid')))
    else:
        flash(sess_rej)
        return redirect('/login')
@manage.route('/trash_todo', methods = ['GET'])
def trash_todo_get():
    if session.get('login'):
        db = dbd.connect()
        if '0' == request.args['r']:
            dbd.set_trash_todo(db, request.args['id'], session.get('uid'), 1)
        else:
            dbd.set_trash_todo(db, request.args['id'], session.get('uid'), 0)
        return redirect('/manage')
    else:
        flash(sess_rej)
        return redirect('/login')
@manage.route('/trash_credit', methods = ['GET'])
def trash_credit_get():
    if session.get('login'):
        db = dbd.connect()
        if '0' == request.args['r']:
            dbd.set_trash_credit(db, request.args['id'], session.get('uid'), 1)
        else:
            dbd.set_trash_credit(db, request.args['id'], session.get('uid'), 0)
        return redirect('/manage')
    else:
        flash(sess_rej)
        return redirect('/login')
@manage.route('/trash_pow', methods = ['GET'])
def trash_pow_get():
    if session.get('login'):
        db = dbd.connect()
        if '0' == request.args['r']:
            print(request.args)
            dbd.set_trash_pow(db, request.args['id'], session.get('uid'), 1)
        else:
            dbd.set_trash_pow(db, request.args['id'], session.get('uid'), 0)
        return redirect('/manage')
    else:
        flash(sess_rej)
        return redirect('/login')

@manage.route('/del_pow', methods = ['GET'])
def del_pow_get():
    if session.get('login'):
        db = dbd.connect()
        dbd.delete_pow(db, request.args['id'], session.get('uid'))
        return redirect('/manage')
    else:
        flash(sess_rej)
        return redirect('/login')
@manage.route('/del_credit', methods = ['GET'])
def del_credit_get():
    if session.get('login'):
        db = dbd.connect()
        dbd.delete_credit(db, request.args['id'], session.get('uid'))
        return redirect('/manage')
    else:
        flash(sess_rej)
        return redirect('/login')
@manage.route('/del_todo', methods = ['GET'])
def del_todo_get():
    if session.get('login'):
        db = dbd.connect()
        dbd.delete_todo(db, request.args['id'], session.get('uid'))
        return redirect('/manage')
    else:
        flash(sess_rej)
        return redirect('/login')
@manage.route('/del_bond', methods = ['GET'])
def del_bond_get():
    if session.get('login'):
        db = dbd.connect()
        dbd.delete_bond(db, request.args['id'], session.get('uid'))
        return redirect('/manage')
    else:
        flash(sess_rej)
        return redirect('/login')
