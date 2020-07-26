"""
This app functions as a REST api endpoint

Have the ability to utilize API keys -- or use VPN to limit to internal traffic
"""
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
from databases.db import db, User


# Import forms
from forms.select_data_simple import dataForm
from forms.select_data_advanced import sqlForm
from forms.registration import LoginForm, SignupForm

# Connect to the db
from connect_broadway_db import select_data_from_simple, select_data_advanced

# import utils
from utils.get_db_uri import get_db_uri

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


# ==============================================================================
# Build login rules
# =============================================================================



@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
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
        user = User.query.filter_by(email=my_data["email"]).first()

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
        existing_user = User.query.filter_by(email=my_data["email"]).first()

        # Create new user
        if existing_user is None:
            user = User(
                email = my_data["email"],
                website = my_data.get("website"),
                instagram = my_data.get("instagram")
                )
            user.set_password(my_data["password"])

            # ---------------------------------------
            del my_data # delete potentially saved pw
            # ---------------------------------------

            # Add to db
            user.save_to_db()

            # Log in as newly created user
            login_user(user)

            return redirect(url_for('index'))

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
# Build routes
# ==============================================================================


# Home
@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Home')

# ------------------------------------------------------------------------------

# Allow the user to request specific data from the app
@app.route('/get-data/',  methods=['GET', 'POST'])
@login_required
def get_data_simple():

    form = dataForm(request.form)

    if request.method == 'POST':
        if True:  #form.validate():
            my_data = {}
            for _, value in form.allFields.data.items():
                if type(value) == dict:
                    my_data.update(value)
            # get rid of the csrf token
            del my_data["csrf_token"]

            cache.set("user_query", my_data)

            return redirect('/get-data-success/')
    else:
        return render_template('get-data.html', title='Submit Data', form=form)


# ------------------------------------------------------------------------------

# Submitted query
@app.route('/get-data-success/',  methods=['GET'])
@login_required
def return_data():

    data = cache.get("user_query")

    # Success vs. Failure
    if data:

        # Retrieve the data from  user's request
        df = select_data_from_simple(my_params=data, theatre_data=True)
        cache.set("my_data", df.to_dict(orient="records"))

        # Return the response in json format
        return render_template('display-data.html',
            summary=df.describe().to_html(header="true", table_id="summary-data"),
            data=df.to_html(header="true", table_id="show-data"),
            title="Data")

    else:
         return jsonify({
                    "ERROR": "data not found."
                })


# ------------------------------------------------------------------------------

@app.route('/get-data-advanced/', methods=['GET','POST'])
@login_required
def get_data_advanced():
    """Landing page for advanced queries"""

    form = sqlForm()

    if request.method == 'POST':
        if form.validate():

            my_data = {k:v for k,v in form.allFields.data.items()}

            # get rid of the csrf token
            del my_data["csrf_token"]

            return redirect(url_for('get_data_advanced_sql',API_KEY=my_data.get("API_KEY"), query=my_data.get("query"), display_data=True))



    return render_template('get-data-advanced.html', form=form, title="Get Data Avanced")




# ------------------------------------------------------------------------------

@app.route('/get-data-advanced/sql/', methods=['GET','POST'])
@login_required
def get_data_advanced_sql():
    """submit sql, returns data"""

    API_KEY = request.args.get('API_KEY')
    query = request.args.get('query')

    # Validate the api key
    None

    # make the request
    df = select_data_advanced(query)


    if request.args.get('display_data'):
        # Make data available for download
        cache.set("my_data", df.to_dict(orient="records"))

        # Render the page
        return render_template('display-data.html',
            data=df.to_html(header="true", table_id="show-data"), title="Data")

    else:
        # return the request
        result = {
            "data": df.to_json(orient='records'),
            "orient": "records",
            "query": query,
        }

        return jsonify(result)


# ------------------------------------------------------------------------------


@app.route('/download-data/<file_format>')
@login_required
def download_data(file_format):
    """Download the data to the user..."""

    # Retrieve the data from  user's request
    data = cache.get("my_data")

    if not data:
        return jsonify({
            "ERROR": "data not found."
        })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    df = pd.DataFrame.from_records(data)

    if file_format == "csv":
        data_out = df.to_csv(index=False, encoding='utf-8')
    elif file_format == "json":
        data_out = df.to_json(orient='records')

    # Send the data out
    now = datetime.datetime.today().strftime("%Y-%m-%d")

    response = Response(
        data_out,
        mimetype=f"text/{file_format}",
        headers={"Content-Disposition": f"attachment; filename=open-broadway-data {now}.{file_format}"})

    return response


# ------------------------------------------------------------------------------


def main():
    # Threaded option to enable multiple instances for multiple user access support

    # Check if AWS...
    my_user = os.environ.get("USER")
    is_aws = True if "ec2" in my_user else False

    # Debug locally, but not on aws...
    app.run(host="0.0.0.0", debug=not is_aws)


if __name__ == '__main__':
    main()
