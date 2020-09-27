from flask import send_from_directory, flash, redirect, request, current_app
from flask_login import login_required
from flask import render_template
from flask_mail import Mail, Message

from forms.admin import AuthenticateUsersForm
from databases.db import db, User
from utils import get_email_content

from common import send_email
import pandas as pd

from utils import require_role
from . import page


@page.route("/approve-users", methods=['GET', 'POST'])
@login_required
@require_role(role="admin-master")
def approve_users():
    """
    Authenticate users
    ---
    Only proceed if the user exists.
        – Try to approve user
        – If user is already approved, will not try to re-approve
            – Sends an email with confirmation link
        – If user is already unapproved, will not re-unapprove
            – Sends an email with notification
    """

    # Otherwise, proceed

    form = AuthenticateUsersForm(request.form)

    # Validate sign up attempt
    if form.validate_on_submit():

        # get data
        my_data = {k:v for k,v in form.allFields.data.items() if k not in ["csrf_token"]}

        # Update the user
        user = User.find_user_by_email(my_data["userEmail"])
        if user:
            if my_data["approve"]:
                _approved_state = user.approve()

                if _approved_state:
                    flash('APPROVED:\t\t{} is successfully APPROVED.'.format(my_data["userEmail"]))

                    # Send an email to verify their account
                    token = user.get_secret_token(60*24*3) #Allow token to expire in 3 days
                    email_content = get_email_content("Approved")

                    send_email(
                        recipients = [user.email],
                        subject = email_content.get("emailSubject"),
                        html = render_template('emails/approved.html', token=token)
                    )
                else:
                    flash('OOPSIES:\t{} is already approved.'.format(my_data["userEmail"]))

            elif my_data["un_approve"]:
                _approved_state = user.unapprove()
                if _approved_state:
                    flash('UNAPPROVED:\t{} is successfully UNAPPROVED.'.format(my_data["userEmail"]))
                else:
                    flash('OOPSIES:\t{} is already unapproved.'.format(my_data["userEmail"]))

            elif my_data["delete"]:
                user.delete_from_db()
                flash('Deleting:\t{}!'.format(my_data["userEmail"]))
        else:
            flash('{} is not a user. Verify that this is the user\'s actual email address.'.format(my_data["userEmail"]))
    # Update the current fields
    else:
        for fieldName, errorMessages in form.allFields.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}")


    # Format the data for the page...
    select_st = """
        SELECT
            user.id as id,
            email,
            user.created_at,
            approved,
            approved_at,
            website,
            instagram,
            message
        FROM
            user
        LEFT JOIN
            message ON user.id = message.user_id
        WHERE
            user.created_at <= CURRENT_TIMESTAMP -30
            OR
            approved=0
        ;
        """
    df = pd.read_sql(select_st, db.engine)
    data = df.sort_values(by=["created_at"], ascending=[True])\
            .to_html(header="true", table_id="show-data")


    return render_template('admin/approve-users.html',title='Approve Users', form=form, data=data)


# -------------------------------------------------------------------------------

@page.route("/inspect-users", methods=['GET', 'POST'])
@login_required
@require_role(role="admin-master")
def inspect_users():
    """
    Authenticate users
    ---
    Only proceed if the user exists.
        – Try to approve user
        – If user is already approved, will not try to re-approve
            – Sends an email with confirmation link
        – If user is already unapproved, will not re-unapprove
            – Sends an email with notification
    """

    # It'll be better to use the ORM instead of raw sql...
    # Otherwise, proceed
    select_st = """
        SELECT
            user.id as id,
            email,
            role.name as role,
            user.created_at,
            approved,
            approved_at,
            website,
            instagram,
            message,
            unapproved_at,
            authenticated,
            authenticated_at,
            login_count,
            request_pw_reset_count,
            api_key_count,
            n_api_requests
        FROM
            user
        LEFT JOIN
            message ON user.id = message.user_id
        LEFT JOIN
            roles_users ON user.id = roles_users.user_id
        LEFT JOIN
            role ON roles_users.role_id = role.id
        WHERE
            user.created_at <= CURRENT_TIMESTAMP -14
            OR
            user.approved='false'
        ;
        """

    df = pd.read_sql(select_st, db.engine)

    data = df.sort_values(by=["created_at"], ascending=[True], ignore_index=True)\
            .to_html(header="true", table_id="show-data")
            # \
            # .reset_index(drop=True)

    return render_template('admin/inspect-users.html',title='Inspect Users', data=data)
