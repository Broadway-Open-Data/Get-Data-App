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
from db import db, User, Role, FormMessage
from utils.get_db_uri import get_db_uri


# ------------------------------------------------------------------------------


# Create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri("users")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()


Create roles manually through here
my_role = Role(
    name = "data.viewer",
    description = "General access to the platform."
    )



# Be sure to double check if the roles exist...
with app.app_context():
    my_role.save_to_db()



# Try creating a user with a role
# with app.app_context():
#     user = User(
#         email = "yb@runport.io2",
#         website = "runport.io",
#         )
#     user.set_password("runport.io")
#
#     # Set the default role
#     default_role = Role.get_by_name(name='general')
#     user.roles.append(default_role)
    # user.save_to_db()
