"""
This app functions as a REST api endpoint

Have the ability to utilize API keys -- or use VPN to limit to internal traffic
"""
import os
import sys
import json
import uuid
import datetime
from pathlib import Path
# set the path to the root
sys.path.append(".")

my_path = {"my_path":os.path.dirname(x) for x in sys.path if x.endswith("app")}.get("my_path")
os.environ['append_path'] = my_path

path = os.environ['append_path']
if path and path not in sys.path:
    sys.path.insert(0, path)

# Use this to open a browser if app is local
import webbrowser

import pandas as pd

from flask import Flask, Response, request, jsonify, render_template, flash, redirect, send_file, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import reqparse # Is this module needed??
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_mail import Mail, Message

# import production server
import waitress

# import models
from databases.db import db, User, Role, FormMessage

# Import forms
from forms.select_data_simple import dataForm
from forms.select_data_advanced import sqlForm
from forms.registration import LoginForm, SignupForm, ForgotPasswordForm
from forms.settings import ChangePasswordForm, UpdateProfileForm, RequestApiKey, ResetApiKey
from forms.admin import AuthenticateUsersForm, CreateRoles, AssignRoles

# Connect to the db
from connect_broadway_db import select_data_from_simple, select_data_advanced

# import utils
# sys.path.append("../utils")
from utils.core import is_aws
from utils.get_db_uri import get_db_uri
from utils.get_creds import get_secret_creds
from utils.get_email_content import get_email_content
from utils import data_summary
# Import cache
from common.extensions import cache


# ==============================================================================
# Begin
# ==============================================================================


def create_app():
    # initialize
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri("users")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # This is otherwise done through the bash profile
    if not os.environ.get("FLASK_SECRET_KEY"):
        os.environ['FLASK_SECRET_KEY'] = "some key"

    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
    app.config['DEBUG'] = not is_aws()
    os.environ['FLASK_ENV'] = 'production' if is_aws() else 'development'


    csrf = CSRFProtect(app)

    # Configure the cache
    cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': Path('/tmp')})


    # Configure the db
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


# =============================================================================


def create_mail(app):
    # Configure mail...
    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
    }
    mail_settings["MAIL_USERNAME"],\
    mail_settings["MAIL_PASSWORD"] \
        = get_secret_creds("EMAIL")

    mail_settings['MAIL_DEFAULT_SENDER'] = "Open Broadway Data <{}>".format(mail_settings["MAIL_USERNAME"])
    mail = Mail(app)
    app.config.update(mail_settings)
    app.extensions['mail'].debug = 0
    return mail



# =============================================================================

def register_login_manager(app):
    # Config the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'login'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        """Redirect unauthorized users to Login page."""
        flash('You must be logged in to view that page.')
        return redirect(url_for('login'))

    # @login_manager.user_loader
    # has_role
    login_manager.init_app(app)


# ------------------------------------------------------------------------------

def register_my_blueprints(app):
    from routes import format
    from routes.auth import login, signup, forgot_password
    from routes.admin import admin_index, manage_users, manage_roles
    from routes.settings import api_key, change_password, settings_index, update_profile, verify

    my_pages = [
        format.page,
        login.page,
        signup.page,
        forgot_password.page,
        admin_index.page,
        manage_users.page,
        manage_roles.page,
        api_key.page,
        change_password.page,
        settings_index.page,
        update_profile.page,
        verify.page
        ]

    for page in my_pages:
        app.register_blueprint(page)


# ------------------------------------------------------------------------------

def register_dash(app):
    from dashapp1.app1 import create_dashboard
    # Create the dash app
    create_dashboard(app)


# ------------------------------------------------------------------------------

# The actual stuff...
class myApp:
    app = create_app()
    mail = create_mail(app)

    def register_things(self):
        register_login_manager(self.app)
        register_my_blueprints(self.app)
        register_dash(self.app)


my_app = myApp()
my_app.register_things()

# ==============================================================================
# Build routes
# ==============================================================================


# Home
@my_app.app.route('/')
# @login_required # Not including -- the page is formatted on its own
def index():

    # Don't allow non-approved users
    # if not current_user.approved:
    #     return redirect("/not-yet-approved")

    return render_template('index.html', title='Home')


# ------------------------------------------------------------------------------

# Allow the user to request specific data from the app
@my_app.app.route('/get-data/',  methods=['GET', 'POST'])
@login_required
def get_data_simple():

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/")

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
@my_app.app.route('/get-data-success/',  methods=['GET'])
@login_required
def return_data():

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/")

    user_query = cache.get("user_query")

    # Success vs. Failure
    if user_query:

        # Get the detail level
        detail_level = user_query.pop("detail_level")
        detail_level = int(detail_level) # must be an int

        # Retrieve the data from  user's request
        df = select_data_from_simple(my_params=user_query, theatre_data=True)
        cache.set("my_data", df.to_dict(orient="records"))

        summary = data_summary.summarize_broadway_shows(df, detail_level)

        # Return the response in json format
        return render_template('display-data.html', summary=summary,
            data=df.to_html(header="true", table_id="show-data"),
            title="Data")

    else:
         return jsonify({
                    "ERROR": "data not found."
                })


# ------------------------------------------------------------------------------

@my_app.app.route('/get-data-advanced/', methods=['GET','POST'])
@login_required
def get_data_advanced():
    """Landing page for advanced queries"""

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/")


    form = sqlForm()

    if request.method == 'POST':

        if form.validate():
            my_data = {k:v for k,v in form.allFields.data.items()}

            # get rid of the csrf token
            del my_data["csrf_token"]

            return redirect(url_for('get_data_advanced_sql',API_KEY=my_data.get("API_KEY"), query=my_data.get("query"), detail_level=my_data.get("detail_level"),display_data=True))

    # Update the form
    form.allFields.query.data = "select * from shows where show_type='musical' and year >2000;"
    form.allFields.API_KEY.data = current_user.api_key

    return render_template('get-data-advanced.html', form=form, title="Get Data Avanced")




# ------------------------------------------------------------------------------

@my_app.app.route('/get-data-advanced/sql/', methods=['GET','POST'])
@login_required
def get_data_advanced_sql():
    """submit sql, returns data"""

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/")


    API_KEY = request.args.get('API_KEY')
    query = request.args.get('query')
    # Get the detail level
    detail_level = request.args.get("detail_level")
    detail_level = int(detail_level) # must be an int


    # Validate the api key
    decoded = User.validate_api_key(API_KEY)

    if not decoded:
        result = {
            "error": "Your api key was not accepted. Register for one or reset yours under settings."
        }
        return jsonify(result)

    # If it was accepted, make the request
    df = select_data_advanced(query)

    if request.args.get('display_data'):
        # Make data available for download
        cache.set("my_data", df.to_dict(orient="records"))

        summary = data_summary.summarize_broadway_shows(df, detail_level)

        # Render the page
        return render_template('display-data.html', summary=summary,
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


@my_app.app.route('/download-data/<file_format>')
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






# ------------------------------------------------------------------------------
from werkzeug.serving import run_simple

def main():
    # Threaded option to enable multiple instances for multiple user access support

    # Serve in development server if local
    if not is_aws():
        # The reloader has not yet run - open the browser
        if not os.environ.get("WERKZEUG_RUN_MAIN"):
            webbrowser.open_new('http://0.0.0.0:5010/')

        # Otherwise, continue as normal
        run_simple(hostname="0.0.0.0", port=5010, application=my_app.app)


    else:
        waitress.serve(my_app.app, host="0.0.0.0", port=5010)



if __name__ == '__main__':
    main()
