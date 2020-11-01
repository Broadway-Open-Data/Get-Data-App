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

    def test_update_functionality(self):
        print("foo")

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -






if __name__ =='__main__':
    db_app = ConnectApp()
    all_user_ids = db_app.query_all_users()
    print(all_user_ids)

    # Test the functionality of the update stuff
    db_app.test_update_functionality()
    # print("*****\nDONE! All data is living in the database.\n*****")
