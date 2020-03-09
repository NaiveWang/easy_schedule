from flask import Flask
from flask_misaka import Misaka

from src.misc import misc
from src.manage import manage
from src.user import user
from src.credit import credit

from src.todo_book import todo_book

import os

app = Flask(__name__)
app.register_blueprint(misc)
app.register_blueprint(manage)
app.register_blueprint(user)
app.register_blueprint(credit)

app.register_blueprint(todo_book)
app.secret_key = os.urandom(12)
Misaka(app)


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5000, debug=True)
