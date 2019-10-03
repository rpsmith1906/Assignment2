from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError

def my_check_number(form, field):
    print(field.data)
    if len(field.data) != 12:
        raise ValidationError('Phone number must be in the format xxx-xxx-xxxx')
    for i,c in enumerate(field.data):
        print(i,c)
        if i in [3,7]:
            if c != '-':
                raise ValidationError('Phone number must be in the format xxx-xxx-xxxx')
        elif not c.isnumeric():
            raise ValidationError('Phone number must be in the format xxx-xxx-xxxx')
        

class Register(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class Login(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    twofapassword = StringField('999-999-9999', validators=[InputRequired(), my_check_number])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Spell(FlaskForm):
    content = TextAreaField('TYPE or PASTE your text here, then click the SPELL CHECK button', validators=[DataRequired()])
    submit = SubmitField('Spell Check')

class TwoFactor(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')