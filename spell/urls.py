from flask import render_template, url_for, flash, redirect
from spell import app
from spell.spell_forms import Login


@app.route("/")
@app.route("/home")
@app.route("/login")
def login():
    form = Login()
    if form.validate_on_submit():
        flash(f'You have been logged in!', 'success')

    return render_template('login.html', title='Login', form=form)