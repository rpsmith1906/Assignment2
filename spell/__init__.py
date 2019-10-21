from flask import Flask, session
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

from spell.userman import Users

app.config['host'] = "0.0.0.0"
app.config['port'] = "5000"
app.config['debug'] = "True"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#app.config['WTF_CSRF_ENABLED'] = False

from spell import urls

Users.load_users()
