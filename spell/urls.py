from flask import Flask
from flask import Flask, request, session, abort, render_template, url_for, flash, redirect
from spell import app
from spell.spell_forms import Login, Spell
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
    return home()

@app.route('/login', methods=['GET','POST'])
def login():
    form = Login()
    print (request)
    if session['logged_in'] == True :
        return redirect(url_for('spell'))
    else:
        print("Here", form.username.data, form.validate_on_submit())
        if form.validate_on_submit():
            if ( form.username.data in Users.password ):
                print("password in file")
                if (form.password.data == Users.password[form.username.data]):
                    print ("Password is correct")
                    session['logged_in'] = True
                    return redirect(url_for('spell'))
            
            flash('Check Username and/or Password!')
            print ("Here")
        print (form)
    return render_template('login3.html', title='Login', form=form)

@app.route('/spell', methods=['GET','POST'])
def spell():
    print ("Spell Checker")
    if ( session['logged_in'] == False):
        return home()
    return render_template('spell.html')
    


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