from flask import Blueprint, render_template
from flask_login import login_required
from utils import require_role
from . import page
from . import accepted_roles

# Allow the user to request specific data from the app
@page.route('/view-people/')
@login_required
@require_role(accepted_roles)
def view_people():

    return render_template('people/view-people.html', title='View People')

#
#
# # ------------------------------------------------------------------------------


# from flask import redirect, url_for, \
#     flash, render_template, request, jsonify
# from flask_login import login_required, current_user
#
# import pandas as pd
#
# # flasks stuff
# from forms.select_data_simple import dataForm
# from common.extensions import cache
# import utils



# # Submitted query
# @page.route('/get-data-success/',  methods=['GET'])
# @login_required
# def return_data():
#
#     # Don't allow non-approved users
#     if not current_user.approved:
#         return redirect("/")
#
#     user_query = cache.get("user_query")
#
#     # Success vs. Failure
#     if user_query:
#
#         # Start off with detail level 2
#         detail_level = 2
#
#         # Retrieve the data from  user's request
#         df = utils.select_data_from_simple(my_params=user_query, theatre_data=True)
#         cache.set("my_data", df.to_dict(orient="records"))
#
#         summary = utils.summarize_broadway_shows(df, detail_level)
#
#         # Return the response in json format
#         return render_template('analyze/display-data.html', summary=summary,
#             data=df.to_html(header="true", table_id="show-data"),
#             title="Data")
#
#     else:
#          return jsonify({
#                     "ERROR": "data not found."
#                 })
