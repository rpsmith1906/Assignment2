from flask import Flask, session
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

from spell.userman import Users

app.config['host'] = "0.0.0.0"
app.config['port'] = "6780"
app.config['debug'] = "True"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['2faPW'] = "test"
Users.current_user = ""

from spell import urls

Users.load_users()
