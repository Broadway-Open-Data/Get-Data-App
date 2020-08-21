from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from databases.db import User

from forms.settings import UpdateProfileForm

page = Blueprint('update_profile', __name__, template_folder='templates')

@page.route("/settings/update-profile", methods=['GET', 'POST'])
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
