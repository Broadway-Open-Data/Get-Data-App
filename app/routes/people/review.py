from flask import Blueprint, render_template
from flask_login import login_required
from utils import require_role
from . import page
from . import accepted_roles


@page.route('/review/')
@login_required
@require_role(accepted_roles)
def review():

    return render_template('people/review.html', title='Review')
