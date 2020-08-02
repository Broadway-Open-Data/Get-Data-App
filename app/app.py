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
from databases.db import db, User, Role

# Import forms
from forms.select_data_simple import dataForm
from forms.select_data_advanced import sqlForm
from forms.registration import LoginForm, SignupForm, ForgotPasswordForm
from forms.settings import ChangePasswordForm, UpdateProfileForm, RequestApiKey, ResetApiKey
from forms.admin import AuthenticateUsersForm

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

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Configure the db
db.init_app(app)
with app.app_context():
    db.create_all()

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Config the login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

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

app.config.update(mail_settings)
mail = Mail()
mail.init_app(app)
# silence the email logger
app.extensions['mail'].debug = 0


# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Register blueprints
from routes import format
# Unsucessful in changing the app architecture / layout of dirs
app.register_blueprint(format.page)


# ==============================================================================
# Build login rules
# =============================================================================


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

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

# I'd love to extend this to wrapper....
# def is_user_approved():
#     if not current_user.approved:
#         return redirect("/not-yet-approved")

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
            login_user(user,remember=True)
            user.login_counter()
            # ---------------------------------------
            del my_data # delete potentially saved pw
            # ---------------------------------------
            return redirect(url_for('index'))

        # Otherwise
        flash('Invalid username/password combination')
        return redirect(url_for('/login'))
    return render_template(
        'login/login.html',
        form=form,
        title='Log in.',
        template='login-page'
        )

# ------------------------------------------------------------------------------

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
            login_user(user,remember=True)

            return redirect(url_for('index'))

        flash('A user already exists with that email address.')

    return render_template(
        'login/signup.html',
        title='Create an Account.',
        form=form,
        template='sign-page',
    )


# ------------------------------------------------------------------------------

@app.route("/login/forgot-password", methods=['GET', 'POST'])
def forgot_password():
    """
    Allow a user to recover their password from their email
    """
    form = ForgotPasswordForm(request.form)

    # Validate sign up attempt
    if form.validate_on_submit():

        # get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}
        user = User.find_user_by_email(email = my_data["email"])
        token = user.get_secret_token(30)

        with app.app_context():
            email_content = get_email_content("Forgot Password", varDict={"link":"www.google.com"})
            msg = Message(
                recipients = [user.email],
                subject = email_content.get("emailSubject"),
                html = render_template('emails/reset_password.html', token=token)
                )
            # Send the email
            mail.send(msg)
        # Increase the count for password reset
        user.request_pw_reset_counter()
        flash(f"An email has been sent to \"{user.email}\" to recover the current account\n\n\
            (Just joking... This is in development and will be in operation soon...)")

    else:
        for fieldName, errorMessages in form.allFields.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}")
    # Send the template...
    return render_template('login/forgot-password.html', title='Forgot Password', form=form)



@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    """Password recovery"""

    # Does the user exist?
    user = User.verify_secret_token(token=token)


    if not user:
        return jsonify({"Error":"Reset link isn't valid"})

    # Get the data
    form = ChangePasswordForm(request.form)

    if form.validate_on_submit():
        # get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}

        # Update the user
        user.set_password(my_data["new_password"])
        user.save_to_db()
        user.login_counter()

        # ---------------------------------------
        del my_data # delete potentially saved pw
        # ---------------------------------------

        # Log in as newly created user
        login_user(user,remember=True)


        return redirect(url_for('index'))


    return render_template('login/reset-password.html',title='Reset Your Password', form=form)



# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


@app.route("/settings")
@login_required
def settings():
    """
    Allow a user to change their password and stuff
    """

    return render_template('settings/settings.html',title='Settings')

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


@app.route("/settings/change-password",  methods=['GET', 'POST'])
@login_required
def change_password():
    """Change your password"""
    form = ChangePasswordForm(request.form)

    # Validate sign up attempt
    if form.validate_on_submit():

        # get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}

        # Update the user
        user = User.find_user_by_id(current_user.id)
        user.set_password(my_data["new_password"])
        user.save_to_db()

        # ---------------------------------------
        del my_data # delete potentially saved pw
        # ---------------------------------------
        flash('Password is successfully updated.')
    else:
        for fieldName, errorMessages in form.allFields.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}")
    # Send the template...
    return render_template('settings/change-password.html',title='Change Password', form=form)


# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

@app.route("/settings/update-profile", methods=['GET', 'POST'])
@login_required
def update_profile():
    """Update your profile"""
    form = UpdateProfileForm(request.form)

    # Validate sign up attempt
    if form.validate_on_submit():

        # get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}

        # Update the user
        user = User.find_user_by_id(current_user.id)
        user.update_info(my_data)
        user.save_to_db()

        flash('Profile is successfully updated.')

    # Update the current fields
    else:
        for fieldName, errorMessages in form.allFields.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}")

    # Continue here...
    form.allFields.email.data = current_user.email
    form.allFields.website.data = current_user.website
    form.allFields.instagram.data = current_user.instagram
    return render_template('settings/update-profile.html',title='Update Profile', form=form)


# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

@app.route("/settings/api-key", methods=['GET', 'POST'])
@login_required
def api_key():
    """Allow a user to generate an api key"""
    if current_user.api_key:
        form = ResetApiKey(request.form)
    else:
        form = RequestApiKey(request.form)

    # Validate sign up attempt
    if form.validate_on_submit():
        user = User.find_user_by_id(current_user.id)

        api_key = user.generate_api_key()
        flash("SUCCESS:\tYour api key is registered.")

    # finally
    return render_template('settings/api-key.html',title='Api Key', form=form)


# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Use https://pythonhosted.org/Flask-Principal/
@app.route("/admin")
@login_required
def admin():
    """Only allow admin users"""
    if not current_user.is_admin():
        return redirect("/")
    # Otherwise, proceed
    return render_template('admin/admin.html',title='Admin')



@app.route("/admin/approve-users", methods=['GET', 'POST'])
@login_required
def approve_users():
    """
    Authenticate users
    ---
    Only proceed if the user exists.
        – Try to approve user
        – If user is already approved, will not try to re-approve
            – Sends an email with confirmation link
        – If user is already unapproved, will not re-unapprove
            – Sends an email with notification
    """
    if not current_user.is_admin():
        return redirect("/")
    # Otherwise, proceed


    form = AuthenticateUsersForm(request.form)

    # Validate sign up attempt
    if form.validate_on_submit():

        # get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}

        # Update the user
        user = User.find_user_by_email(my_data["userEmail"])
        if user:
            if my_data["approve"]:
                _approved_state = user.approve()

                if _approved_state:
                    flash('APPROVED:\t\t{} is successfully APPROVED.'.format(my_data["userEmail"]))

                    # Send an email to verify their account
                    token = user.get_secret_token(60*24*3) #Allow token to expire in 3 days
                    email_content = get_email_content("Approved")
                    msg = Message(
                        recipients = [user.email],
                        subject = email_content.get("emailSubject"),
                        html = render_template('emails/approved.html', token=token)
                        )
                    mail.send(msg)
                else:
                    flash('OOPSIES:\t{} is already approved.'.format(my_data["userEmail"]))

            elif my_data["un_approve"]:
                _approved_state= user.unapprove()
                if _approved_state:
                    flash('UNAPPROVED:\t{} is successfully UNAPPROVED.'.format(my_data["userEmail"]))
                else:
                    flash('OOPSIES:\t{} is already unapproved.'.format(my_data["userEmail"]))
        else:
            flash('{} is not a user. Verify that this is the user\'s actual email address.'.format(my_data["userEmail"]))
    # Update the current fields
    else:
        for fieldName, errorMessages in form.allFields.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}")


    # Format the data for the page...
    select_st = User.query.filter_by(approved=False).all()
    if len(select_st)>=1:
        raw_data = [x.__data__() for x in select_st]

        # format
        df = pd.DataFrame.from_records(raw_data)
        data = df.sort_values(by=["created_at"], ascending=[True])\
                .to_html(header="true", table_id="show-data")
    else:
        data = "<pre>No data available.<br>All users are approved!</pre>"
    # Continue here...
    return render_template('admin/approve-users.html',title='Approve Users', form=form, data=data)


@app.route("/admin/inspect-users", methods=['GET', 'POST'])
@login_required
def inspect_users():
    """
    Authenticate users
    ---
    Only proceed if the user exists.
        – Try to approve user
        – If user is already approved, will not try to re-approve
            – Sends an email with confirmation link
        – If user is already unapproved, will not re-unapprove
            – Sends an email with notification
    """
    if not current_user.is_admin():
        return redirect("/")
    # Otherwise, proceed
    select_st = User.query.limit(100).all()

    raw_data = [x.__data__() for x in select_st]

    # format
    df = pd.DataFrame.from_records(raw_data)
    data = df.sort_values(by=["created_at"], ascending=[True])\
            .to_html(header="true", table_id="show-data")

    return render_template('admin/inspect-users.html',title='Inspect Users', data=data)


@app.route("/verify-account/<token>", methods=['GET', 'POST'])
def verify_account(token):
    """Verify your account"""

    # Does the user exist?
    user = User.verify_secret_token(token=token)


    if not user:
        return jsonify({"Error":"Link isn't valid"})

    user.authenticate()
    login_user(user,remember=True)
    user.login_counter()
    flash("SUCCESS:\t\tYou have verified your account!")

    return redirect('/')





# ==============================================================================
# Build routes
# ==============================================================================


# Home
@app.route('/')
@login_required
def index():
    print(url_for('admin', _external=True))

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/not-yet-approved")

    return render_template('index.html', title='Home')


@app.route('/not-yet-approved')
@login_required
def not_yet_approved():
    return render_template('not-yet-approved.html', title='Not Yet Approved')

# ------------------------------------------------------------------------------

# Allow the user to request specific data from the app
@app.route('/get-data/',  methods=['GET', 'POST'])
@login_required
def get_data_simple():

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/not-yet-approved")

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

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/not-yet-approved")

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

@app.route('/get-data-advanced/', methods=['GET','POST'])
@login_required
def get_data_advanced():
    """Landing page for advanced queries"""

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/not-yet-approved")


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

@app.route('/get-data-advanced/sql/', methods=['GET','POST'])
@login_required
def get_data_advanced_sql():
    """submit sql, returns data"""

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/not-yet-approved")


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

    # Serve in development server if local
    if not is_aws():
        # The reloader has not yet run - open the browser
        if not os.environ.get("WERKZEUG_RUN_MAIN"):
            webbrowser.open_new('http://0.0.0.0:5010/')
        # Otherwise, continue as normal
        app.run(host="0.0.0.0", port=5010)

    else:
        waitress.serve(app, host="0.0.0.0", port=5010)



if __name__ == '__main__':
    main()
