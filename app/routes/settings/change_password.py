from flask import render_template, flash, request
from flask_login import login_required, current_user

from databases.models.users import User

from forms import ChangePasswordForm

from . import page

@page.route("/change-password",  methods=['GET', 'POST'])
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
