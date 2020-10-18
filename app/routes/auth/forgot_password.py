from flask import send_from_directory, redirect, url_for, \
    flash, render_template, request, jsonify
from flask_login import login_required, logout_user, login_user
from flask_mail import Message

from databases.models import User, Role
from utils.get_email_content import get_email_content

from forms.registration import ForgotPasswordForm
from forms.settings import ChangePasswordForm

from common import send_email

#  Import the blueprint page
from . import page

@page.route("/login/forgot-password", methods=['GET', 'POST'])
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

        # with page.app_context():
        email_content = get_email_content("Forgot Password", varDict={"link":"www.google.com"})
        send_email(
            recipients = [user.email],
            subject = email_content.get("emailSubject"),
            html = render_template('emails/reset_password.html', token=token)
        )

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



@page.route("/reset-password/<token>", methods=['GET', 'POST'])
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


        return redirect(url_for('index.index'))


    return render_template('login/reset-password.html',title='Reset Your Password', form=form)
