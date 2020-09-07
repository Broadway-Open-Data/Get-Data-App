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

# Import the actual app
from app import create_app, register_blueprint

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
from forms.select_data_advanced import sqlForm
from forms.registration import LoginForm, SignupForm, ForgotPasswordForm
from forms.settings import ChangePasswordForm, UpdateProfileForm, RequestApiKey, ResetApiKey
from forms.admin import AuthenticateUsersForm, CreateRoles, AssignRoles

# Connect to the db
from connect_broadway_db import select_data_from_simple, select_data_advanced

# Import cache
from common import cache
import utils


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
        = utils.get_secret_creds("EMAIL")

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
        register_blueprint(self.app)
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

        summary = utils.data_summary.summarize_broadway_shows(df, detail_level)

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





# ------------------------------------------------------------------------------






# ------------------------------------------------------------------------------
from werkzeug.serving import run_simple

def main():
    # Threaded option to enable multiple instances for multiple user access support

    # Serve in development server if local
    if not utils.is_aws():
        # The reloader has not yet run - open the browser
        if not os.environ.get("WERKZEUG_RUN_MAIN"):
            webbrowser.open_new('http://0.0.0.0:5010/')

        # Otherwise, continue as normal
        run_simple(hostname="0.0.0.0", port=5010, application=my_app.app)


    else:
        waitress.serve(my_app.app, host="0.0.0.0", port=5010)



if __name__ == '__main__':
    main()
