from flask import Blueprint, render_template, make_response, request, redirect, flash, session


import src.db.driver as dbd
import src.db.user as dbu

from src.conf import sess_rej, version

hub = Blueprint('hub', __name__)


@hub.route('/hub', methods = ['GET'])
def hub_get():
    if session.get('login'):
        db = dbd.connect()
        return render_template('hub.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                powdump = dbd.dump_pow_me_fence(db, session.get('uid')),
                                userdump = dbd.dump_user_visible_hub(db))
    else:
        flash(sess_rej)
        return redirect('/login')

@hub.route('/peek_proof', methods = ['GET'])
def peek_proof_get():
    if session.get('login'):
        db = dbd.connect()
        # check user premission
        # get the content
        proof = dbd.get_pow_user_fence(db, session.get('uid'), request.args['id'])
        if not proof:
            flash('Permission Denied / No Proof Found')
            return redirect('/hub')
        return render_template('peek_proof.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                proof = proof)
    else:
        flash(sess_rej)
        return redirect('/login')
@hub.route('/peek_user', methods = ['GET'])
def peek_user_get():
    if session.get('login'):
        db = dbd.connect()
        # check user premission

        u = dbd.get_user_visible(db, request.args['id'])
        if not u:
            flash('Permission Denied / No Proof Found')
        # get the content
        return render_template('peek_user.html',
                                uinfo = dbd.get_uinfo(db, request.args['id']),
                                version = version,
                                u = u,
                                powdump = dbd.dump_pow_user_fence(db, request.args['id']),
                                todotump_finished = dbd.dump_todo_user_finished(db, request.args['id']),
                                todotump_progress = dbd.dump_todo_user_progress(db, request.args['id']))
    else:
        flash(sess_rej)
        return redirect('/login')
