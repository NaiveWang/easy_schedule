from flask import Blueprint, render_template, request, redirect, flash, session

import src.db.driver as dbd
from src.conf import sess_rej, version

credit = Blueprint('credit', __name__)


@credit.route('/', methods = ['GET'])
def root_get():
    if session.get('login'):
        db = dbd.connect()
        credits = session.get('credit')
        return render_template('dashboard.html',
                            uinfo = dbd.get_uinfo(db, session.get('uid')),
                            version = version,
                            credit_avaliable = dbd.credit_get_avaliable(db, session.get('uid'), credits),
                            credit_pending = dbd.credit_get_pending(db, session.get('uid')),
                            credit_finished = dbd.credit_get_finished(db, session.get('uid')),
                            credit_inprogress = dbd.credit_get_inprogress(db, session.get('uid'), credits))

    else:
        flash(sess_rej)
        return redirect('/login')

# Credit op
@credit.route('/new_credit', methods = ['GET'])
def new_credit_get():
    if session.get('login'):
        db = dbd.connect()
        return render_template('/new_credit.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                before  = dbd.get_user_avali_credit(db, session.get('uid')))
    else:
        flash(sess_rej)
        return redirect('/login')

@credit.route('/new_credit', methods = ['POST'])
def new_credit_post():
    if session.get('login'):
        # create
        db = dbd.connect()
        dbd.credit_create(db, session.get('uid'), request.form['name'], request.form['price'], request.form['after'])
        return redirect('/')
    else:
        flash(sess_rej)
        return redirect('/login')
@credit.route('/spend_credit', methods = ['GET'])
def spend_credit_post():
    if session.get('login'):
        db = dbd.connect()
        dbd.credit_spend(db, session.get('uid'), request.args['id'])
        return redirect('/')
    else:
        flash(sess_rej)
        return redirect('/login')
