from flask import Blueprint, render_template, make_response, request, redirect, flash, session


import src.db.driver as dbd
import src.db.user as dbu

from src.conf import sess_rej, version

misc = Blueprint('misc', __name__)




@misc.route('/help', methods = ['GET'])
def help_get():
    if session.get('login'):
        db = dbd.connect()
        uinfo = dbd.get_uinfo(db, session.get('uid'))
    else:
        uinfo = ["#Anonymous", "我没有敌人。", "NaN"]
    readme = open('readme.md').read()
    return render_template('help.html',
                            uinfo = uinfo,
                            version = version,
                            readme = readme)

@misc.route('/hub', methods = ['GET'])
def hub_get():
    if session.get('login'):
        db = dbd.connect()
        return render_template('hub.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                powdump = dbd.dump_pow_user_fence(db, session.get('uid')),
                                userdump = dbd.dump_user_visible(db))
    else:
        flash(sess_rej)
        return redirect('/login')

@misc.route('/peek_proof', methods = ['GET'])
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
@misc.route('/new_todo', methods = ['GET'])
def new_todo_get():
    if session.get('login'):
        db = dbd.connect()
        sur = dbd.get_type(db)[int(request.args['tid'])]
        return render_template('/new_todo_'+sur+'.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                todo = dbd.get_nfinished_by_uid(db, session.get('uid')),
                                version = version,
                                uid = session.get('uid'),
                                bond = dbu.get_friend(db, session.get('uid')))
    else:
        flash(sess_rej)
        return redirect('/login')
