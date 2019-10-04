from flask import Flask
from flask import Flask, request, session, abort, render_template, url_for, flash, redirect

from spell import app
from spell import bcrypt
from spell.spell_forms import Login, Spell, TwoFactor, Register
from spell.userman import Users

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
    print(form.username.data)
    if session.get('logged_in') :
        return redirect(url_for('spell'))
    else:
        if ( "click" in request.form ):
            if ( request.form['click'] == "Log In"):
                if form.validate_on_submit():
                    if ( form.username.data in Users.password ) :
                        try:
                            test_pw = bcrypt.check_password_hash(Users.password[form.username.data], form.password.data)
                        except:
                            test_pw = False
                    else :
                        test_pw = False

                    if ( form.username.data in Users.twofapassword) :
                        try:
                            test_twofapw = bcrypt.check_password_hash(Users.twofapassword[form.username.data], form.twofapassword.data)
                        except:
                            test_twofapw = False
                    else :
                        test_twofapw = False
                    
                    if ( test_pw and test_twofapw ):
                        session['logged_in'] = True
                        flash('User ,' + form.username.data +", successful logged in.", "result")
                        return redirect(url_for('spell'))
                    else:
                        if not test_pw :
                            flash("Incorrect username and/or password was supplied.", "result")

                        if not test_twofapw :
                            flash("Two-factor authentication failure was detected.", "result")
            else:
                print ("Here - register")
                return redirect(url_for('register'))
                
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = Register()
    print(form.username.data)
    if session.get('logged_in') :
        return redirect(url_for('spell'))
    else:
        print ( request.form )
        if ( "click" in request.form ):
            if ( request.form['click'] == "Log In"):
                return redirect(url_for('login'))
            else:
                if form.validate_on_submit():
                    if not Users.create_user(form.username.data, form.password.data, form.twofapassword.data):
                        flash ("User, " + form.username.data + ", registration failure. User already exists.", "success")
                    else:
                        flash ("User, " + form.username.data + ", was successfully registered.", "success")    
    print (form.errors)
    print ("Here-endloop")       
    return render_template('register.html', title='Register', form=form)

@app.route('/spell', methods=['GET','POST'])
def spell():
    form = Spell()
    if not session.get('logged_in') :
        return home()
    else:
        if ( "click" in request.form ):
            if ( request.form['click'] == "Log Out"):
                return redirect(url_for('logout'))
            else:
                print("spell", vars(form), form.submit, request.form)
                flash("Works", "results")
                
    return render_template('spell.html', title="Spell Checker", form=form)

@app.route('/2factor', methods=['GET', 'POST'])
def twofactor():
    form=TwoFactor()
    print (session)
    if (  not session.get('2factor') ):
        return home()
    else:
        #print("Here - else" + form.validate_on_submit())
        #form.current_user = Users.current_user
        if form.validate_on_submit():
            print("Here")
            if ( form.password.data == app.config['2faPW'] ):
                session['logged_in'] = True
                flash('User ,' + session['2factor'] +", successful logged in via 2FA.")
                session['2factor'] = ""
                return redirect(url_for('spell'))
            else:
                Users.current_user = ""
                flash("Login via Two-factor failed.")
                return redirect(url_for('login'))
    
    return render_template('twofalogin.html', title='Two Factor Login', form=form)
    #return redirect(url_for('login'))


#@app.route("/")
#@app.route("/home")
#@app.route("/login", methods=['GET', 'POST'])
#def login():
    #form = Login()
    #if form.validate_on_submit():
    #    print(form.username.data)
    #    if Users.password[form.username.data] == form.password.data : 
    #        flash('You have been logged in!', 'success')
    #        return redirect(url_for('login'))
    #    else:
    #        flash('Login Unsuccessful.  Please check username and password')

    #return render_template('login2.html', title='Login', form=form)