from spell import app
from spell.userman import Users

if __name__ == '__main__':
     app.run(host=app.config['host'], port=app.config['port'], debug=app.config['debug'])
     #Users.load_users()
     #Users.create_user("robert", "abc123", "rpsmith@ibm.com")
     #Users.query("rpsmith@ibm.com")
     #Users.file.close()