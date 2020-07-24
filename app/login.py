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
from flask import Flask, Blueprint, Response, request, jsonify, render_template, flash, redirect, send_file, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

# import models
from databases.db import db, UserModel

# Read further here https://flask-login.readthedocs.io/en/latest/
from forms.registration import LoginForm, SignupForm

# Utils
from utils.get_db_uri import get_db_uri

# Import cache
from common.extensions import cache


# ------------------------------------------------------------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri("users")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'any secret string'
csrf = CSRFProtect(app)

# Configure the cache
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': '/tmp'})

# Configure the db
db.init_app(app)
with app.app_context():
    db.create_all()


# Config the login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



# ==============================================================================
# Build login rules
# =============================================================================


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return UserModel.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


@app.route("/logout")
@login_required
def logout():
    """Log out"""
    logout_user()
    return redirect(url_for('login'))



# ==============================================================================
# Build login routes
# =============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # continue
    form = LoginForm(request.form)

    # Validate login attempt
    if form.validate_on_submit():

        # Get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}

        # If the user is in the db
        user = UserModel.query.filter_by(email=my_data["email"]).first()

        if user and user.check_password(password=my_data["password"]):
            login_user(user)
            # ---------------------------------------
            del my_data # delete potentially saved pw
            # ---------------------------------------
            return redirect(url_for('index'))

        # Otherwise
        flash('Invalid username/password combination')
        return redirect(url_for('login'))
    return render_template(
        'login.html',
        form=form,
        title='Log in.',
        template='login-page'
        )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.
    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm(request.form)

    # Validate sign up attempt
    if form.validate_on_submit(): #request.method == 'POST'

        # get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}

        # If the user is in the db
        existing_user = UserModel.query.filter_by(email=my_data["email"]).first()

        # Create new user
        if existing_user is None:
            user = UserModel(
                email = my_data["email"],
                website = email.get("website"),
                instagram = email.get("instagram")
                )
            user.set_password(my_data["password"])

            # ---------------------------------------
            del my_data # delete potentially saved pw
            # ---------------------------------------

            # Add to db
            user.save_to_db()

            # Log in as newly created user
            login_user(user)

            # return redirect(url_for('index'))
            return jsonify({"hi":"you good"})

        flash('A user already exists with that email address.')

    return render_template(
        'signup.html',
        title='Create an Account.',
        form=form,
        template='sign-page',
    )


@app.route("/settings")
@login_required
def settings():
    """
    Allow a user to change their password and stuff
    """

    return render_template(
        'settings.html',
        title='Settings'
    )


# ==============================================================================
# Build login callback
# ==============================================================================

# Home
@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Home')





# ------------------------------------------------------------------------------




if __name__ == '__main__':

    # Threaded option to enable multiple instances for multiple user access support

    # Check if AWS...
    my_user = os.environ.get("USER")
    is_aws = True if "ec2" in my_user else False

    # Debug locally, but not on aws...
    app.run(host="0.0.0.0", debug=not is_aws)
