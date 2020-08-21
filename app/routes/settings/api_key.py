from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from databases.db import User

from forms.settings import ResetApiKey


page = Blueprint('api_key', __name__, template_folder='templates')


@page.route("/settings/api-key", methods=['GET', 'POST'])
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
