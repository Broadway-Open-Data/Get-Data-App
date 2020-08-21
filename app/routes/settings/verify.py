from flask import Blueprint, jsonify, flash, redirect
from flask_login import login_required, login_user
from databases.db import User

page = Blueprint('verify_account', __name__, template_folder='templates')

@page.route("/verify-account/<token>", methods=['GET', 'POST'])
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
