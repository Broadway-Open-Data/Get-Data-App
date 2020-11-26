from flask import send_from_directory, flash, redirect, render_template, request
from flask_login import login_required

from forms import CreateRoles, AssignRoles
from databases.models.users import User, Role

from utils import require_role
from . import page

import pandas as pd



@page.route("/create-roles", methods=['GET', 'POST'])
@login_required
@require_role("admin-master")
def create_roles():
    """
    Assigne and manage roles
    ---
    """
    form = CreateRoles(request.form)

    # Validate sign up attempt
    if form.validate_on_submit():

        # get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}
        flash('Your data is: {}'.format(my_data))

    return render_template('admin/create-roles.html',title='Create Roles', form=form)


@page.route("/assign-roles", methods=['GET', 'POST'])
@login_required
@require_role("admin-master")
def assignroles():
    """
    Assigne and manage roles
    ---
    """

    form = AssignRoles(request.form)

    available_roles = Role.query.with_entities(Role.name).all()

    # Validate sign up attempt
    if form.validate_on_submit():

        # get data + enforce lowercase values
        my_data = {k:v.lower() for k,v in form.allFields.data.items() if k not in ["csrf_token"]}
        flash('Your data is: {}'.format(my_data))

        # Add or remove the role here
        my_user = User.find_user_by_email(my_data['userEmail'])
        my_user.assign_role(my_data['roleName'], assign_or_unassign=my_data['assign'])
        print("new updated roles: ", my_user.roles)

    return render_template('admin/assign-roles.html',title='Assign Roles', form=form, available_roles=available_roles)
