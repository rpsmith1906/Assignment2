#!/usr/bin/python3

from flask import Flask
from spell import bcrypt
import os.path


class Users():
    email = dict()
    password = {}
    twofapassword = {}

    def load_users():
        print ("Here")
        if os.path.isfile("spell/security/users"):
            print ("Found file")
            Users.file = open("spell/security/users","r+")
            for line in Users.file:
                username, password, email = line.split(':', 2)
                Users.email[username] = email  
                Users.password[username] = password
                Users.twofapassword[username] = bcrypt.generate_password_hash("999-999-9999").decode('utf-8')
                print (username,password,email)
                print("Here")
        else:
            print ("Open File")
            Users.file = open("spell/security/users","w")

       #     while ( line = file.readlines()):
        #        print (line)
          

    def create_user(username, password, email):
        #email = dict()
        #password = {}
        if (not username in Users.email.values()):
            print(username)
            Users.email[username] = email  
            Users.password[username] = bcrypt.generate_password_hash(password).decode('utf-8')
            print ("Write to File")
            Users.file.write(username+":"+Users.password[username]+":"+email+"\n") 


    def query(username):
         print(Users.password)
         print(Users.email)
         print(list(Users.password.values()))
         
         if ( not username in Users.email.values() ):
            return ( False )
    