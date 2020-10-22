from flask import Blueprint, render_template, flash, request
from flask_login import login_required
from utils import require_role

# Import my form
from forms.query_people import Query

# Module stuff
from . import page
from . import accepted_roles

# Import db stuff
from databases.methods.broadway import get_all_people

def dict_without_empty_values(d):
    return


@page.route('/query/', methods=['GET', 'POST'])
@login_required
@require_role(accepted_roles)
def query():

    form = Query(request.form)

    if form.validate_on_submit():

        # get the data from the submitted form
        query_data = dict(request.form.items())
        query_data.pop("csrf_token")

        # filter null values
        query_data = {k:v.lower() for k,v in query_data.items() if v}


        # show the user (for debugging)
        flash(f'You submitted the following query: {query_data}')

        # Now make a request to get this data from the db
        # Import a db method!
        data = get_all_people(query_data)

    else:
        data = {}

    return render_template('people/query.html', title='Query', form=form, data=data)
