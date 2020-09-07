from flask import send_from_directory, flash, redirect, render_template, request
from flask_login import current_user, login_required
from flask_mail import Mail, Message

from forms.admin import CreateRoles, AssignRoles
from databases.db import db, User

import pandas as pd

from . import page


@page.route("/create-roles", methods=['GET', 'POST'])
@login_required
def create_roles():
    """
    Assigne and manage roles
    ---
    """
    if not current_user.is_admin():
        return redirect("/")
    # Otherwise, proceed


    form = CreateRoles(request.form)

    # Validate sign up attempt
    if form.validate_on_submit():

        # get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}
        flash('Your data is: {}'.format(my_data))

    return render_template('admin/create-roles.html',title='Create Roles', form=form)


@page.route("/assign-roles", methods=['GET', 'POST'])
@login_required
def assignroles():
    """
    Assigne and manage roles
    ---
    """
    if not current_user.is_admin():
        return redirect("/")
    # Otherwise, proceed


    form = AssignRoles(request.form)

    # Validate sign up attempt
    if form.validate_on_submit():

        # get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}
        flash('Your data is: {}'.format(my_data))

    return render_template('admin/assign-roles.html',title='Assign Roles', form=form)
