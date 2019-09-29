from flask import Flask

app = Flask(__name__)

app.config['host'] = "0.0.0.0"
app.config['port'] = "8080"
app.config['debug'] = "True"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

from spell import urls