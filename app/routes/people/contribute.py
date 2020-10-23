from flask import Blueprint, render_template
from flask_login import login_required

# app stuff
from utils import require_role
from databases.methods.broadway import get_all_people, get_all_directors

# module stuff
from . import page
from . import accepted_roles


@page.route('/contribute/')
@login_required
@require_role(accepted_roles)
def contribute():


    # Get the director data stuff
    query_params = {'role_name': 'director', 'shows_year_from': 1900, 'shows_year_to':1910}
    data = get_all_directors(query_params, output_format='html')

    return render_template('people/contribute.html', title='Contribute', data=data)
