from flask import Flask, send_from_directory
from flask_misaka import Misaka

from src.misc import misc
from src.manage import manage
from src.user import user
from src.friend import friend
from src.credit import credit
from src.hub import hub

from src.todo_book import todo_book
from src.todo_keep import todo_keep, keep_daily_refresh
from src.todo_sport import todo_sport



import os



app = Flask(__name__)
app.register_blueprint(misc)
app.register_blueprint(manage)
app.register_blueprint(user)
app.register_blueprint(friend)
app.register_blueprint(credit)
app.register_blueprint(hub)

app.register_blueprint(todo_book)
app.register_blueprint(todo_keep)
app.register_blueprint(todo_sport)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.secret_key = os.urandom(12)
Misaka(app)

# icon

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.errorhandler(413)
def error413(e):
    return "Buffer Protection", 413
if __name__ == "__main__":
    import scheduler
    app.run(host='0.0.0.0', port=5000, debug=True)
