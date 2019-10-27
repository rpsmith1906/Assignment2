from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'

from spell.userman import Users
from spell.userman import User

app.config['host'] = "0.0.0.0"
app.config['port'] = "5000"
app.config['debug'] = "True"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#app.config['WTF_CSRF_ENABLED'] = False

from spell import urls

Users.load_users()
