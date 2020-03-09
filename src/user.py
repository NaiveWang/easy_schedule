from flask import Blueprint, render_template, request, redirect, flash, session

import src.db.driver as dbd
import src.db.user as dbu
from src.conf import sess_rej, version
from src.db.misc.security import hash

user = Blueprint('user', __name__)

####$ User Session Man
# user login
@user.route('/login', methods = ['GET'])
def login_get():
    return render_template('login.html', version = version)
@user.route('/login', methods = ['POST'])
def login_post():
    name = request.form['name']
    passwd = hash(request.form['passwd'])
    db = dbd.connect()
    motto, uid, credit = dbu.auth_user(db, name, passwd)
    if motto != None:
        # success, get session
        session['login'] = True
        session['user'] = name
        session['uid'] = uid
        session['auth'] = passwd
        session['motto'] = motto
        session['credit'] = credit
        resp = redirect('/')

        return resp
    else:
        flash('Login failed.')
        return redirect('/login')
# user logout
@user.route('/logout', methods = ['GET'])
def logout_get():
    session['login'] = False
    return redirect('/login')
# activate
@user.route('/activate', methods = ['GET'])
def activate_get():
    return render_template('activate.html', version = version)
@user.route('/activate', methods = ['POST'])
def activate_post():
    name = request.form['name']
    passwd = hash(request.form['passwd'])
    actcode = request.form['actcode']
    db = dbd.connect()
    if dbu.auth_activate(db, name, passwd, actcode):
        return redirect('/login')
    else:
        flash('Activation Failed.')
        return redirect('/activate')
# user config
@user.route('/me', methods = ['GET'])
def me_get():
    if session.get('login'):
        db = dbd.connect()

        return render_template('me.html',
                                user = session.get('user'),
                                motto = session.get('motto'),
                                credit = session.get('credit'),
                                version = version,
                                token = dbu.get_friend_code(db, session.get('uid')))
    else:
        flash(sess_rej)
        return redirect('/login')
@user.route('/me_visible', methods = ['POST'])
def me_visible_post():
    if session.get('login'):
        db = dbd.connect()
        dbu.update_visible(db, session.get('uid'), request.form['v'])
        return redirect('/me')
    else:
        flash(sess_rej)
        return redirect('/login')
@user.route('/me_wassup', methods = ['POST'])
def me_wassup_post():
    if session.get('login'):
        #update wassup
        db = dbd.connect()
        dbu.update_motto(db, session.get('uid'), request.form['motto'])
        #update cookie
        session['motto'] = request.form['motto']
        return redirect('/me')
    else:
        flash(sess_rej)
        return redirect('/login')
@user.route('/me_passcode', methods = ['POST'])
def me_passcode_post():
    hashnew = hash(request.form['passwdn'])
    hashold = hash(request.form['passwd'])
    if session.get('login') and hashold == session.get('auth'):
        #change passcode
        db = dbd.connect()
        dbu.update_passwd(db, session.get('uid'), hashold, hashnew)
        # update cookie
        # we assume the user is being violated anyway
        flash('Password Changed, please login again with new password.')
        return redirect('/logout')
    else:
        flash('Wrong password, force log out.')
        return redirect('/logout')
@user.route('/me_gen_tok', methods = ['POST'])
def me_gen_tok_post():
    if session.get('login'):
        db = dbd.connect()
        dbu.gen_friend_code(db, session.get('uid'))
        return redirect('/me')
    else:
        flash(sess_rej)
        return redirect('/login')
@user.route('/me_add_friend', methods = ['POST'])
def me_add_friend_post():
    if session.get('login'):
        db = dbd.connect()
        dbu.new_friend(db, request.form['token'], session.get('uid'))
        return redirect('/me')
    else:
        flash(sess_rej)
        return redirect('/login')
