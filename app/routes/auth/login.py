from flask import send_from_directory, Blueprint, redirect, url_for, \
    flash, render_template
from flask_login import current_user, login_required, logout_user


page = Blueprint('login', __name__, template_folder='templates')
@page.route("/logout")
@login_required
def logout():
    """Log out"""
    logout_user()
    return redirect(url_for('login'))

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
