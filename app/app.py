"""
This app functions as a REST api endpoint

Have the ability to utilize API keys -- or use VPN to limit to internal traffic
"""
import os
import sys
# import json
import datetime
# set the path to the root
sys.path.append(".")


# import subprocess
# import requests
import pandas as pd


from flask import Flask, Response, request, jsonify, render_template, flash, \
    redirect, send_file, url_for
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse

# Import forms
from forms.select_data_simple import dataForm
from forms.select_data_advanced import sqlForm

# Connect to the db
from connect_db import select_data_from_simple, select_data_advanced

# import utils
from utils.get_db_uri import get_db_uri

# Import cache
from common.extensions import cache


# ==============================================================================
# Begin
# ==============================================================================


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'any secret string'
csrf = CSRFProtect(app)

# Configure the app
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem", 'CACHE_DIR': '/tmp'})


# ==============================================================================
# Build routes
# ==============================================================================


# Home
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# ------------------------------------------------------------------------------

# Allow the user to request specific data from the app
@app.route('/get-data/',  methods=['GET', 'POST'])
def get_data_simple():

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

            return redirect('/get-data-success/')
    else:
        return render_template('get-data.html', title='Submit Data', form=form)


# ------------------------------------------------------------------------------

# Submitted query
@app.route('/get-data-success/',  methods=['GET'])
def return_data():

    data = cache.get("user_query")

    # Success vs. Failure
    if data:

        # Retrieve the data from  user's request
        df = select_data_from_simple(my_params=data, theatre_data=True)
        cache.set("my_data", df.to_dict(orient="records"))

        # Return the response in json format
        return render_template('display-data.html',
            summary=df.describe().to_html(header="true", table_id="summary-data"),
            data=df.to_html(header="true", table_id="show-data"),
            title="Data")

    else:
         return jsonify({
                    "ERROR": "data not found."
                })


# ------------------------------------------------------------------------------

@app.route('/get-data-advanced/', methods=['GET','POST'])
def get_data_advanced():
    """Landing page for advanced queries"""

    form = sqlForm()

    if request.method == 'POST':
        if form.validate():

            my_data = {k:v for k,v in form.allFields.data.items()}

            # get rid of the csrf token
            del my_data["csrf_token"]

            return redirect(url_for('get_data_advanced_sql',API_KEY=my_data.get("API_KEY"), query=my_data.get("query"), display_data=True))



    return render_template('get-data-advanced.html', form=form, title="Get Data Avanced")




# ------------------------------------------------------------------------------

@app.route('/get-data-advanced/sql/', methods=['GET','POST'])
def get_data_advanced_sql():
    """submit sql, returns data"""

    API_KEY = request.args.get('API_KEY')
    query = request.args.get('query')

    # Validate the api key
    None

    # make the request
    df = select_data_advanced(query)


    if request.args.get('display_data'):
        # Make data available for download
        cache.set("my_data", df.to_dict(orient="records"))

        # Render the page
        return render_template('display-data.html',
            data=df.to_html(header="true", table_id="show-data"), title="Data")

    else:
        # return the request
        result = {
            "data": df.to_json(orient='records'),
            "orient": "records",
            "query": query,
        }

        return jsonify(result)


# ------------------------------------------------------------------------------


@app.route('/download-data/<file_format>')
def download_data(file_format):
    """Download the data to the user..."""

    # Retrieve the data from  user's request
    data = cache.get("my_data")

    if not data:
        return jsonify({
            "ERROR": "data not found."
        })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    df = pd.DataFrame.from_records(data)

    if file_format == "csv":
        data_out = df.to_csv(index=False, encoding='utf-8')
    elif file_format == "json":
        data_out = df.to_json(orient='records')

    # Send the data out
    now = datetime.datetime.today().strftime("%Y-%m-%d")

    response = Response(
        data_out,
        mimetype=f"text/{file_format}",
        headers={"Content-Disposition": f"attachment; filename=open-broadway-data {now}.{file_format}"})

    return response


# ------------------------------------------------------------------------------


def main():
    # Threaded option to enable multiple instances for multiple user access support

    # Check if AWS...
    my_user = os.environ.get("USER")
    is_aws = True if "ec2" in my_user else False

    # Debug locally, but not on aws...
    app.run(host="0.0.0.0", debug=not is_aws)


if __name__ == '__main__':
    main()
