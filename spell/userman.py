#!/usr/bin/python3

from flask import Flask
from spell import bcrypt
from spell import db
import os.path

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    twofapassword = db.Column(db.String(10))

    def __repr__(self):
        return '<User %r>' % self.username

class Users():
    email = dict()
    password = {}
    twofapassword = {}

    def load_users():
        if os.path.isfile("spell/security/users"):
            Users.file = open("spell/security/users","r")
            for line in Users.file:
                username, password, twofapassword, trash = line.rstrip().split(':', 3)
                Users.password[username] = password
                if twofapassword != "-" :
                    Users.twofapassword[username] = twofapassword
            Users.file.close()

    def create_user(username, password, twofapassword):
        if (not username in Users.password):
            Users.file = open("spell/security/users","a")
            Users.password[username] = bcrypt.generate_password_hash(password).decode('utf-8')
            Users.twofapassword[username] = twofapassword

            if len(twofapassword) == 0:
                Users.file.write(username+":"+Users.password[username]+":-:\n") 
            else:
                Users.file.write(username+":"+Users.password[username]+":"+Users.twofapassword[username]+":\n") 

            Users.file.close()
            return ( True )
        else:
            return ( False)


    def query(username):
         if ( not username in Users.email.values() ):
            return ( False )
    
