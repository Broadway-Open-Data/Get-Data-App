from flask import Blueprint, render_template
from flask_login import login_required
from utils import require_role
from . import page
from . import accepted_roles


@page.route('/contribute/')
@login_required
@require_role(accepted_roles)
def contribute():

    return render_template('people/contribute.html', title='Contribute')
