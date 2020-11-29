from flask import redirect, url_for, \
    flash, render_template, request, jsonify
from flask_login import login_required, current_user

import pandas as pd

# flasks stuff
from databases.methods.broadway import get_all_shows
from forms import dataForm, shows
from common.extensions import cache
import utils

# ------------------------------------------------------------------------------

from . import page

# Allow the user to request specific data from the app
@page.route('/get-data/',  methods=['GET', 'POST'])
@login_required
# Add this code (and modify it) to accept any role...
# @require_role("admin-master")
def get_data_simple():

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/")

    # form = dataForm(request.form)
    form = shows.Query(request.form)

    if request.method == 'POST':

        if form.validate_on_submit():

            # get the data from the submitted form
            query_data = dict(request.form.items())
            query_data.pop("csrf_token")


            # filter null values
            query_data = {k:v.lower() for k,v in query_data.items() if v}

            # substitute 'y' and 'n'
            # Do this the long way... (look into a map method...)
            for k,v in query_data.items():
                if v=='y':
                    query_data[k] = True
                elif v=='n':
                    query_data[k] = False

            # There probably is a better way to do this too...
            num_keys = ['show_year_from', 'show_year_to']
            for key in num_keys:
                if key in query_data.keys():
                    query_data[key] = int(query_data[key])

            # cache and redirect
            cache.set("user_query", query_data)
            return redirect('/analyze/get-data-success/')

    else:
        return render_template('analyze/get-data.html', title='Submit Data', form=form)


# ------------------------------------------------------------------------------

# Submitted query
@page.route('/get-data-success/',  methods=['GET'])
@login_required
def return_data():

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/")

    user_query = cache.get("user_query")

    # Success vs. Failure
    if user_query:

        # Start off with detail level 2
        detail_level = 2

        df = get_all_shows(user_query)

        # Retrieve the data from  user's request
        # df = utils.select_data_from_simple(my_params=user_query, theatre_data=True)
        cache.set("my_data", df.to_dict(orient="records"))

        summary = utils.summarize_broadway_shows(df, detail_level)

        # Return the response in json format
        return render_template(
            'analyze/display-data.html',
            summary=summary,
            data=df.to_html(header=True, na_rep='', bold_rows=False, index_names=False, index=False, render_links=True, classes='freeze-header'),
            title="Data")

    else:
         return jsonify({
                    "ERROR": "data not found."
                })
