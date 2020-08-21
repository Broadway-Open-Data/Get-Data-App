from flask import send_from_directory, Blueprint, redirect, url_for, \
    flash, render_template, request
from flask_login import login_required, logout_user, login_user
from forms.registration import LoginForm, SignupForm, ForgotPasswordForm

from databases.db import User, Role



page = Blueprint('signup', __name__, template_folder='templates')
@page.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.
    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm(request.form)

    # Validate sign up attempt
    if form.validate_on_submit(): #request.method == 'POST'

        # get data & remove the token
        my_data = form.data
        del my_data["csrf_token"]

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

            # Set the default role
            default_role = Role.get_by_name(name='general')
            user.roles.append(default_role)
            user.save_to_db()

            # Now create the signup messag
            user.save_signup_message(my_data["message"])

            # ---------------------------------------
            del my_data # delete potentially saved pw
            # ---------------------------------------

            # Log in as newly created user
            login_user(user,remember=True)

            return redirect(url_for('index'))

        flash('A user already exists with that email address.')

    elif form.errors.items():
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(err)

    return render_template(
        'login/signup.html',
        title='Create an Account.',
        form=form,
        template='sign-page',
    )
