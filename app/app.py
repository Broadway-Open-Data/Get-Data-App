"""
This app functions as a REST api endpoint

Have the ability to utilize API keys -- or use VPN to limit to internal traffic
"""
import os
import sys
# set the path to the root
sys.path.append(".")


import subprocess
import requests
import pandas as pd
from flask import Flask, request, jsonify, render_template, flash, redirect
from flask_wtf.csrf import CSRFProtect

# Import forms
from forms.select_data import dataForm

# import utils
from utils.get_db_uri import get_db_uri

# ==============================================================================
# Begin
# ==============================================================================


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'any secret string'
csrf = CSRFProtect(app)

# db.init_app(app)
# with app.app_context():
#     db.create_all()



# ==============================================================================
# Build routes
# ==============================================================================



# Home
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# ------------------------------------------------------------------------------


@app.route('/submit-data/',  methods=['GET', 'POST'])
def submit_data():

    form = dataForm(request.form)

    if request.method == 'POST':
        if True: #form.validate():
            my_data = {}
            for key, value in form.allFields.data.items():
                if type(value)==dict:
                    my_data.update(value)
            # get rid of the csrf token
            del my_data["csrf_token"]
            return render_template('submit-data-success.html', title="Success", data=my_data)
    else:
        return render_template('submit-data.html', title='Submit Data', form=form)


# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------

@app.route('/return-data/', methods=['GET','POST'])
def respond():
    """submit a specific json, returns data"""

    # Retrieve the api_key
    # api_key = request.form.get("api_key", None)
    # if not api_key:
    #     return jsonify({
    #         "ERROR": "api_key not found."
    #     })

    # Retrieve the data from  parameter
    data = request.form.get("data", None)
    # data = request.get_json(force=True)

    if not data:
        return jsonify({
            "ERROR": "data not found."
        })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # Proceed
    response = {}

    # Return the response in json format
    return jsonify(response)



# ------------------------------------------------------------------------------


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", debug=True)
