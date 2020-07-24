"""
In testing right now...
"""
import os
import sys
import json
import datetime
# set the path to the root
sys.path.append(".")

import flask
from flask import Flask, Response, request, jsonify, render_template, flash, redirect, send_file, url_for, flash
from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager, login_user, current_user, login_required
# import models
from databases.models import User

# Read further here https://flask-login.readthedocs.io/en/latest/
from forms.login_form import LoginForm


from utils.get_db_uri import get_db_uri
# Import cache
from common.extensions import cache


# ------------------------------------------------------------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri("broadway")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'any secret string'
csrf = CSRFProtect(app)

# Configure the cache
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': '/tmp'})



# Config the login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# ==============================================================================
# Build login callback
# ==============================================================================

@login_manager.user_loader
def load_user(user_id):
    return User.get(email)


# ------------------------------------------------------------------------------
login_manager.login_view = 'login'

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        # if not logged in or password not correct
        if user is None or not user.check_password(form.password.data):
            flask.flash('Invalid username or password')
            return redirect(url_for('login'))

        # Otherwise, log in the user
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    else:
        return flask.render_template('login.html', form=form)


    #
    #     # Login and validate the user.
    #     # user should be an instance of your `User` class
    #     # login_user(user)
    #
    #     flask.flash('Logged in successfully.')
    #
    #     next = flask.request.args.get('next')
    #     # is_safe_url should check if the url is safe for redirects.
    #     # See http://flask.pocoo.org/snippets/62/ for an example.
    #     # if not is_safe_url(next):
    #     #     return abort(400)
    #
    #


#
# @app.route("/settings")
# @login_required
# def settings():
#     pass
#
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':

    # Threaded option to enable multiple instances for multiple user access support

    # Check if AWS...
    my_user = os.environ.get("USER")
    is_aws = True if "ec2" in my_user else False

    # Debug locally, but not on aws...
    app.run(host="0.0.0.0", debug=not is_aws)
