from flask import send_from_directory, Blueprint, redirect, url_for, \
    flash, render_template, request
from flask_login import current_user, login_required, logout_user, login_user
from forms.registration import LoginForm, SignupForm, ForgotPasswordForm

from databases.db import User

from . import page
# page = Blueprint('login', __name__, template_folder='templates')
@page.route("/logout")
@login_required
def logout():
    """Log out"""
    logout_user()
    return redirect(url_for('auth.login'))



@page.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """


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
            # Save the IP address of the user
            print(request.headers['X-Forwarded-For'])
            print(request.headers)
            # user.save_ip(request.environ.get('REMOTE_ADDR'))
            # ---------------------------------------
            del my_data # delete potentially saved pw
            # ---------------------------------------
            return redirect(url_for('index'))

        # Otherwise
        flash('Invalid username/password combination')

    return render_template(
        'login/login.html',
        form=form,
        title='Log in.',
        template='login-page'
        )

# I'd love to extend this to wrapper....
# def is_user_approved():
#     if not current_user.approved:
#         return redirect("/")

# Create a decorator...
def role_required(function):
    """Does the user have this role?"""
    def wrapper(**args):
        # Bypass if user is logged in
        for role in args:
            if current_user.roles==role:
                return redirect(url_for('index'))
