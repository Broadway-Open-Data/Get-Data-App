from flask import Blueprint, render_template
from flask_login import login_required
from utils import require_role
from . import page


# name
accepted_roles = [
    'admin-master'
    'admin-master-2'
    'data.admin'
    'data.editor'
    'data.viewer'
    'user-approval.admin'
    'user-approval.editor'
]




@page.route("/")
@login_required
@require_role(role=accepted_roles)
def admin():
    """Only allow admin users"""
    # Otherwise, proceed
    return render_template('admin/admin.html',title='Admin')

















#
