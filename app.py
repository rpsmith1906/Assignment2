#!/usr/bin/python3

from spell import app
from spell.userman import Users

if __name__ == '__main__':
     print( app.config['WTF_CSRF_ENABLED'] )
     app.run(host=app.config['host'], port=app.config['port'], debug=app.config['debug'])
     
