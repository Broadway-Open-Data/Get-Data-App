import sys
import os
import json
import sys
import datetime
import uuid


# Correct the path
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Internal stuff
from create_db import db


# Flask Stuff
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from utils.get_db_uri import get_db_uri


# Define args
import argparse

parser = argparse.ArgumentParser(description='describe the name of the operation you want to do -- using the function name / class method.')
parser.add_argument('function_name', nargs='*', help='name of the class method you want to run')



# ------------------------------------------------------------------------------


class ConnectApp():

    def __init__(self, **kwargs):

        # Instantiate a blank app
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_BINDS'] = {
            'users': get_db_uri("users"),
            'broadway': get_db_uri("broadway"),
        }

        # instantiate the db
        self.app.app_context().push()
        db.init_app(app=self.app)
        db.create_all()

    # ------------------------------------------------------------------------------

    # Create some methods

    def query_all_users(self):
        """Get all existing show ids"""

        query = """
        SELECT
            id
        FROM
            users.user
        ;
        """
        result = db.get_engine(bind='users').execute(query)
        all_ids = [int(x[0]) for x in result]
        return all_ids



    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def test_on_change(self):
        print("foo")

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -






if __name__ =='__main__':

    args = parser.parse_args()

    db_app = ConnectApp()

    if 'query_all_users' in args.function_name:
        all_user_ids = db_app.query_all_users()
        print(all_user_ids)

    # Test the functionality of the update stuff
    if 'test_on_change' in args.function_name:
        db_app.test_on_change()







#
