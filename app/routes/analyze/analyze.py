from flask import redirect, url_for, \
    flash, render_template, request, jsonify
from flask_login import login_required, current_user

import pandas as pd

# flasks stuff
from forms.select_data_simple import dataForm
from common.extensions import cache
import utils

# ------------------------------------------------------------------------------

from . import page

# Allow the user to request specific data from the app
@page.route('/get-data/',  methods=['GET', 'POST'])
@login_required
def get_data_simple():

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/")

    form = dataForm(request.form)

    if request.method == 'POST':
        if True:  #form.validate():
            my_data = {}
            for _, value in form.allFields.data.items():
                if type(value) == dict:
                    my_data.update(value)
            # get rid of the csrf token
            del my_data["csrf_token"]

            cache.set("user_query", my_data)

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

        # Retrieve the data from  user's request
        df = utils.select_data_from_simple(my_params=user_query, theatre_data=True)
        cache.set("my_data", df.to_dict(orient="records"))

        summary = utils.summarize_broadway_shows(df, detail_level)

        # Return the response in json format
        return render_template('analyze/display-data.html', summary=summary,
            data=df.to_html(header="true", table_id="show-data"),
            title="Data")

    else:
         return jsonify({
                    "ERROR": "data not found."
                })
