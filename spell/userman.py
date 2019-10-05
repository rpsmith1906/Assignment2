#!/usr/bin/python3

from flask import Flask
from spell import bcrypt
import os.path


class Users():
    email = dict()
    password = {}
    twofapassword = {}

    def load_users():
        if os.path.isfile("spell/security/users"):
            Users.file = open("spell/security/users","r")
            for line in Users.file:
                username, password, twofapassword = line.split(':', 2)
                Users.password[username] = password
                Users.twofapassword[username] = twofapassword
            Users.file.close()

    def create_user(username, password, twofapassword):
        print(username, Users.password)
        if (not username in Users.password):
            Users.file = open("spell/security/users","a")
            Users.password[username] = bcrypt.generate_password_hash(password).decode('utf-8')
            Users.twofapassword[username] = bcrypt.generate_password_hash(twofapassword).decode('utf-8')

            Users.file.write(username+":"+Users.password[username]+":"+Users.twofapassword[username]+"\n") 
            Users.file.close()
            return ( True )
        else:
            return ( False)


    def query(username):
         print(Users.password)
         print(Users.email)
         print(list(Users.password.values()))
         
         if ( not username in Users.email.values() ):
            return ( False )
    
