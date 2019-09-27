#!/usr/bin/python3

from flask import Flask, render_template, url_for, flash, redirect
#from flask-wtf import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET KEY'] = ''
@app.route("/")
def home():
     return "<h1>Home Page</h1>"
     return render_template()


@app.route("/about")
def about():
     return "<h1> About Page</h1>"

@app.route("/register")
def register():
	form = RegistrationForm()
	return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080, debug=True)
