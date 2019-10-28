#!/usr/bin/python3

from flask import Flask
from spell import bcrypt
from spell import db
import os.path

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(70), unique=True, nullable=False)
    twofapassword = db.Column(db.String(10))
    sessions = db.relationship('Log', backref='username', lazy=True)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.DateTime)
    logout = db.Column(db.DateTime)
    username_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Users():
    #password = {}
    #twofapassword = {}

    def create_user(username, password, twofapassword):
        row = User()
        row.username = username
        row.password = bcrypt.generate_password_hash(password).decode('utf-8')
        if ( len(twofapassword) > 0 ) :
            row.twofapassword = twofapassword
        
        try:
            db.session.add(row)
            db.session.commit()
            return ( True )
        except:
            db.session.rollback() 
            return( True )

    def check_user(username, password, twofapassword) :
        if ( User.query.filter_by(username=username).first() is None ) :
            return ( False )
        else:
            pw = User.query.filter_by(username=username).first().password
            print (pw)
            if ( bcrypt.check_password_hash(pw, password) ) :
                print ("Return")
                return ( False )

            print("Here")
            pw = User.query.filter_by(username=username).twofapassword.first()
            if ( len(pw) != 0 ) :
                if ( pw != twofapassword) :
                    return ( False )
            else:
                if ( len( twofapassword ) != 0 ) :
                    return ( False )
        return ( True )
