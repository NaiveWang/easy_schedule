from flask import Blueprint, render_template, request, redirect, flash, session
import src.db.driver as dbd
import src.db.user as dbu
from src.conf import sess_rej, version

friend = Blueprint('friend', __name__)

@friend.route('/friend', methods = ['GET'])
def friend_get():
    if session.get('login'):
        db = dbd.connect()
        return render_template('friend.html',
                                uinfo = dbd.get_uinfo(db, session.get('uid')),
                                version = version,
                                friend = dbu.get_friend(db, session.get('uid')))
    else:
        flash(sess_rej)
        return redirect('/login')
