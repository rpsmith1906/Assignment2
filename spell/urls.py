from flask import Flask
from flask import Flask, request, session, abort, render_template, url_for, flash, redirect
from spell import app
from spell.spell_forms import Login, Spell, TwoFactor
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
    form = Login()
    print (form)
    flash('User successfully logged out.')
    return home()

@app.route('/login', methods=['GET','POST'])
def login():
    form = Login()
    Users.current_user = form.username.data
    if session['logged_in'] == True :
        return redirect(url_for('spell'))
    else:
        if form.validate_on_submit():
            if ( form.username.data in Users.password ):
                if (form.password.data == Users.password[form.username.data]):
                    Users.current_user = form.username.data
                    session['2factor'] = True
                    return redirect(url_for('twofactor'))
            
            flash('Check Username and/or Password!')
    return render_template('login3.html', title='Login', form=form)

@app.route('/spell', methods=['GET','POST'])
def spell():
    form = Spell()
    if ( session['logged_in'] == False):
        return home()
    else:
        if ( "click" in request.form ):
            if ( request.form['click'] == "Log Out"):
                form = Login()
                return redirect(url_for('logout'))
            else:
                print("spell", vars(form), form.submit, request.form)
    return render_template('spell.html', title="Spell Checker", form=form)

@app.route('/2factor', methods=['GET', 'POST'])
def twofactor():
    form=TwoFactor()
  
    if ( not Users.current_user ) or ( session['logged_in'] == True ):
        return home()
    else:
        form.current_user = Users.current_user
        if form.validate_on_submit():
            if ( form.password.data == app.config['2faPW'] ):
                session['logged_in'] = True
                form=Spell()
                flash('User ,' + Users.current_user +", successful logged in via 2FA.")
                return redirect(url_for('spell'))
            else:
                Users.current_user = ""
                form=Login()
                flash("Login via 2FA was unsuccessful.")
                return redirect(url_for('login'))
                        
    return render_template('twofalogin.html', title='Two Factor Login', form=form)


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