from flask import Blueprint, render_template
from flask_login import login_required
from utils import require_role

# Import my form
from forms.query_people import Query

# Module stuff
from . import page
from . import accepted_roles


@page.route('/query/')
@login_required
@require_role(accepted_roles)
def query():

    form = Query()
    return render_template('people/query.html', title='Query', form=form)
