from flask import Flask
from flask import Flask, request, session, abort, render_template, url_for, flash, redirect

from spell import app
from spell import bcrypt
from spell.spell_forms import Login, Spell, TwoFactor, Register
from spell.userman import Users

import subprocess

@app.route('/')
def home():
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('spell'))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('User successfully logged out.')
    return home()

@app.route('/login', methods=['GET','POST'])
def login():
    form = Login()
    messages = []

    if session.get('logged_in') :
        return redirect(url_for('spell'))
    else:
        if ( "click" in request.form ) :
            if ( request.form['click'] == "Log In" ) :
                login = True
            else:
                return redirect(url_for('register'))
        else:
            login = False

        if ( login ) or ( request.method == "POST" ):
            if form.validate_on_submit():
                if ( form.username.data in Users.password ) :
                    try:
                        test_pw = bcrypt.check_password_hash(Users.password[form.username.data], form.password.data)
                    except:
                        test_pw = False
                else :
                    test_pw = False

                if ( form.username.data in Users.twofapassword) :
                    if ( Users.twofapassword[form.username.data] != form.twofapassword.data ):
                         test_twofapw = False
                    else:
                         test_twofapw = True
                else:
                    test_twofapw = True

                    
                if ( test_pw and test_twofapw ):
                    session['logged_in'] = True
                    messages.append('User ,' + form.username.data +", successful logged in.")
                    return render_template('spell.html', title="Spell Checker", form=Spell(), len=len(messages), messages=messages)
                else:
                    if not test_pw :
                        messages.append("Incorrect username and/or password was supplied.")

                    if not test_twofapw :
                        messages.append("Two-factor authentication failure was detected.")

                    return render_template('login.html', title='Login', form=form, len=len(messages), messages=messages)
            return render_template('login.html', title='Login', form=form)
                
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form=Register()
    message=""
    if session.get('logged_in') :
        return redirect(url_for('spell'))
    else:
        print("Here")
        if ( request.method == "POST" ) :
            if ( "click" in request.form ) and ( request.form['click'] == "Log In") :
                return redirect(url_for('login'))
            else:
                print("Here2")
                if form.validate_on_submit():
                    if not Users.create_user(form.username.data, form.password.data, form.twofapassword.data):
                        message = "User, " + form.username.data + ", registration failure. User already exists."
                    else:
                        message = "User, " + form.username.data + ", was successfully registered."
                    return render_template('register.html', title='Register', form=form, message=message)
    return render_template('register.html', title='Register', form=form)

@app.route('/spell_check', methods=['GET','POST'])
def spell():
    form = Spell()
    if not session.get('logged_in') :
        return home()
    else:
        if ( "click" in request.form ):
            if ( request.form['click'] == "Log Out"):
                return redirect(url_for('logout'))
            else:
                cmd = ["spell/bin/spell_flask", "-", "spell/bin/wordlist.txt"]
                input = form.content.data.encode('utf-8')
                results = subprocess.run(cmd, stdout=subprocess.PIPE, input=input).stdout.decode('utf-8')
                
                if results:
                	flash(results, "results")
                
    return render_template('spell.html', title="Spell Checker", form=form)
