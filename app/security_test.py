import os
import sys
# import json
import datetime
from pathlib import Path
# set the path to the root
sys.path.append(".")


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

# import models
from databases.db import db, User, Role, roles_users


# import utils
from utils.get_db_uri import get_db_uri

# Import cache
from common.extensions import cache

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri("users")
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

# Create database connection object
db = SQLAlchemy(app)



# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    # db.session.commit()

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
