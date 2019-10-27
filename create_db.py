#!/usr/bin/python3

import spell
import os

from spell import app
from spell import db
from spell import file

os.unlink(file)
db.create_all()