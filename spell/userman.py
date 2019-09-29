#!/usr/bin/python3
    
import os.path

class Users():
    email = dict()
    password = {}

    def load_users():
        print ("Here")
        if os.path.isfile("spell/security/users"):
            Users.file = open("spell/security/users","r+")
            for line in Users.file:
                username, password, email = line.split(':', 2)
                Users.email[username] = email  
                Users.password[username] = password
                print (username,password,email)
                print("Here")
        else:
            Users.file = open("spell/security/users","w")

       #     while ( line = file.readlines()):
        #        print (line)
          

    def create_user(username, password, email):
        #email = dict()
        #password = {}
        if (not username in Users.email.values()):
            print(username)
            Users.email[username] = email  
            Users.password[username] = password
            Users.file.write(username+":"+password+":"+email+"\n") 


    def query(username):
         print(Users.password)
         print(Users.email)
         print(list(Users.password.values()))
         
         if ( not username in Users.email.values() ):
            return ( False )
    