from flask import Blueprint, render_template
from flask_login import login_required
from utils import require_role
from . import page

import databases.methods.broadway as broadway_methods


@page.route("/")
@login_required
@require_role(role="admin-master")
def admin():
    """Only allow admin users"""
    # Otherwise, proceed

    broadway_methods.get_all_people()
    return render_template('admin/admin.html',title='Admin')
