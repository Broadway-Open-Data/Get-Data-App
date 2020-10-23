import os
from flask import redirect, url_for, \
    flash, render_template, request, jsonify
from flask_login import login_required, current_user

import pandas as pd

# flasks stuff
from databases.models.users import User
import databases.methods as db_methods
# import databases.methods.broadway as broadway_methods

from forms import sqlForm
from common.extensions import cache
import utils

# ------------------------------------------------------------------------------

from . import page


@page.route('/get-data', methods=['GET','POST'])
@login_required
def get_data_advanced():
    """Landing page for advanced queries"""

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/")

    data_schema = db_methods.broadway.get_db_schema()

    # generate the erd?
    save_path = 'app/static/images/databases-ERD/broadway.png'
    if not os.path.isfile(save_path):
        db_methods.get_db_ERD('broadway', save_path=save_path)

    form = sqlForm()

    if request.method == 'POST':

        if form.validate():
            my_data = {k:v for k,v in form.allFields.data.items()}

            # get rid of the csrf token
            del my_data["csrf_token"]

            return redirect(url_for('advanced.get_data_advanced_sql',
                API_KEY=my_data.get("API_KEY"),
                query=my_data.get("query"),
                detail_level=2,
                display_data=True)
                )

    # Update the form
    form.allFields.query.data = "select * from shows where show_type='musical' and year >2000;"
    form.allFields.API_KEY.data = current_user.api_key

    return render_template('advanced/get-data.html', data_schema=data_schema, form=form, title="Get Data Avanced")




# ------------------------------------------------------------------------------

@page.route('/get-data/sql', methods=['GET','POST'])
@login_required
def get_data_advanced_sql():
    """submit sql, returns data"""

    # Don't allow non-approved users
    if not current_user.approved:
        return redirect("/")


    API_KEY = request.args.get('API_KEY')
    query = request.args.get('query')
    # Get the detail level
    detail_level = request.args.get("detail_level")
    detail_level = int(detail_level) # must be an int


    # Validate the api key
    decoded = User.validate_api_key(API_KEY)

    if not decoded:
        result = {
            "error": "Your api key was not accepted. Register for one or reset yours under settings."
        }
        return jsonify(result)

    # If it was accepted, make the request
    df = utils.select_data_advanced(query)

    if request.args.get('display_data'):
        # Make data available for download
        cache.set("my_data", df.to_dict(orient="records"))

        summary = utils.summarize_broadway_shows(df, detail_level)

        # Render the page
        return render_template('analyze/display-data.html', summary=summary,
            data=df.to_html(header="true", table_id="show-data", na_rep='', bold_rows=False, index_names=False, render_links=True, classes='freeze-header'), title="Data")

    else:
        # return the request
        result = {
            "data": df.to_json(orient='records'),
            "orient": "records",
            "query": query,
        }

        return jsonify(result)
