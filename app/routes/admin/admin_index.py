from flask import Blueprint, render_template
from flask_login import login_required
from utils import require_role
from . import page


@page.route("/")
@login_required
@require_role(role="admin-master")
def admin():
    """Only allow admin users"""
    # Otherwise, proceed
    return render_template('admin/admin.html',title='Admin')
