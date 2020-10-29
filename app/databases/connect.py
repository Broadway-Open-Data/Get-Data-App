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
        self.app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri('users')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['JSON_AS_ASCII'] = False
        
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
            user
        ;
        """
        result = db.engine.execute(query)
        all_ids = [int(x[0]) for x in result]
        return all_ids



    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def foo(self):
        print("foo")

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -






if __name__ =='__main__':
    db_app = ConnectApp()
    all_user_ids = db_app.query_all_users()
    print(all_user_ids)
    # print("*****\nDONE! All data is living in the database.\n*****")
