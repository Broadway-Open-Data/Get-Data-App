import sys
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
# from utils.get_db_uri import get_db_uri


# ------------------------------------------------------------------------------


# Create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri("users")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()


# # Create roles manually through here
# my_role = Role(
#     name = "data.viewer",
#     description = "General access to the platform."
#     )
#
#
#
# # Be sure to double check if the roles exist...
# with app.app_context():
#     my_role.save_to_db()



# Try creating a user with a role
with app.app_context():
    user = User.find_user_by_email('yaakovbressler@gmail.com')

    print(user.has_role('data.viewers'))

    # # Set the default role
    # my_role = Role.get_by_name(name='data.admin')
    # user.add_role(my_role)
    #
    # if my_role in user.roles:
    #     print("already in")
    # else:
    #     user.roles.append(my_role)
    #     user.save_to_db()
    # for x in user.roles:
    #     print(x)










#
