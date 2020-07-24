import os
import json
import sys
import datetime
import uuid
# Correct the path
sys.path.append("././")


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db import db , UserModel
from utils.get_db_uri import get_db_uri


# ------------------------------------------------------------------------------


# Create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri("users")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()


print("*****\nDONE! All data is living in the database.\n*****")
