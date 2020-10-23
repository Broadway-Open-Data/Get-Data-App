from flask import Blueprint, render_template, flash, request
from flask_login import login_required

# app stuff
from utils import require_role
from databases.methods.broadway import get_all_people, get_all_directors

# Import my form
from forms.people import UpdateDataForm


# module stuff
from . import page
from . import accepted_roles


@page.route('/contribute/', methods=['GET', 'POST'])
@login_required
@require_role(accepted_roles)
def contribute():


    form = UpdateDataForm(request.form)

    if form.validate_on_submit():

        # get the data from the submitted form
        update_data = dict(request.form.items())
        update_data.pop("csrf_token")

        # filter null values
        update_data = {k:v.lower() for k,v in update_data.items() if v}


        # show the user (for debugging)
        flash(f'You submitted the following update_data: {update_data}')

        # Execute this command

    # Get the director data stuff
    query_params = {'role_name': 'director', 'shows_year_from': 1900, 'shows_year_to':1910}
    data = get_all_directors(query_params, output_format='html')

    return render_template('people/contribute.html', title='Contribute', form=form, data=data)
