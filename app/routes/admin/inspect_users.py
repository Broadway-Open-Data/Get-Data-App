import pandas as pd
from flask_login import current_user, login_required
from flask import render_template, send_from_directory, Blueprint
from databases.db import db


page = Blueprint('admin/inspect-users', __name__, template_folder='templates')
@page.route("/admin/inspect-users", methods=['GET', 'POST'])
@login_required
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
    if not current_user.is_admin():
        return redirect("/")

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
