import os
import sys
# import json
import datetime
from pathlib import Path
# set the path to the root
sys.path.append(".")


# import subprocess
# import requests
import pandas as pd


from flask import Flask, Blueprint, Response, request, jsonify, render_template, flash, redirect, send_file, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse
from flask_login import LoginManager, login_user, current_user, login_required, logout_user


# import models
from databases.db import db, User, Role


# Import forms
from forms.select_data_simple import dataForm
from forms.select_data_advanced import sqlForm
from forms.registration import LoginForm, SignupForm, ForgotPasswordForm
from forms.settings import ResetPasswordForm, UpdateProfileForm

# Connect to the db
from connect_broadway_db import select_data_from_simple, select_data_advanced

# import utils
from utils.get_db_uri import get_db_uri
from utils.get_creds import get_secret_creds
# Import cache
from common.extensions import cache


# ==============================================================================
# Begin
# ==============================================================================


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri("users")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'any secret string'
csrf = CSRFProtect(app)


# Configure the cache
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': Path('/tmp')})


# Configure the db
db.init_app(app)
with app.app_context():
    db.create_all()


# Config the login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)

username, password = get_secret_creds("EMAIL")
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": username,
    "MAIL_PASSWORD": password
}
del username, password


app.config.update(mail_settings)
mail = Mail()
mail.init_app(app)





if __name__ == '__main__':
    with app.app_context():
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["zenya.bangar@gmail.com"], # replace with your email for testing
                      body="I'm testing this out...")
        mail.send(msg)














#
