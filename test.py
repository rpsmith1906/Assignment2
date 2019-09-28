#!/usr/bin/python3
    
class Users():
    email = dict()
    password = {}

    def create_user(username, password, email):
        #email = dict()
        #password = {}
        print(username)
        Users.email[username] = email  
        Users.password[username] = password 

    def query(username):
         print(Users.password)
         print(Users.email)
         print(list(Users.password.values()))
         
         if ( username in Users.email.values() ):
            print ("Found It")

if __name__ == '__main__':
     #app.run(host='0.0.0.0', port=8080, debug=True)
     Users.create_user("robert", "abc123", "rpsmith@ibm.com")
     Users.query("rpsmith@ibm.com")