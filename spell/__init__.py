from flask import Flask

app = Flask(__name__)

app.config['host'] = "0.0.0.0"
app.config['port'] = "8080"
app.config['debug'] = "True"