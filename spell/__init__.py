from flask import Flask
from spell.userman import Users

app = Flask(__name__)

app.config['host'] = "0.0.0.0"
app.config['port'] = "8080"
app.config['debug'] = "True"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['2faPW'] = "test"
Users.current_user = ""

from spell import urls

Users.load_users()