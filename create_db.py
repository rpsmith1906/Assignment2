#!/usr/bin/python3

import spell
import os

from spell import app, db, bcrypt, file

#os.unlink(file)
#pw_hash = bcrypt.generate_password_hash("test").decode('utf-8')
#print (pw_hash)
#pw_hash = bcrypt.generate_password_hash("afdjlkfjakljfalkjadskljadslfjdsalk").decode('utf-8')
#print (pw_hash)
#print ( len(pw_hash))
db.create_all()
