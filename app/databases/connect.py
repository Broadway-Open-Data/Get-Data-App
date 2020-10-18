import os
import json
import sys
import datetime
import uuid
# Correct the path
sys.path.append(".")

# Internal stuff
from databases import db
from databases.models import User
from utils.get_db_uri import get_db_uri


# Flask Stuff
from flask import Flask
from flask_sqlalchemy import SQLAlchemy








# ------------------------------------------------------------------------------


class ConnectApp():

    def __init__(self, **kwargs):

        # Instantiate a blank app
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri("users")
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # instantiate the db
        db.init_app(app=self.app)
        self.app.app_context().push()

        db.create_all()

    # ------------------------------------------------------------------------------

    # Create some methods

    def query_all_users(self):
        """Get all existing show ids"""
        query_all = db.session.query(User.id).all()
        all_ids = [int(x[0]) for x in query_all]
        return all_ids



    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def foo(self):
        print("foo")


    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -






if __name__ =='__main__':
    # do_all()
    db_app = ConnectApp()
    print(db_app.query_all_users())
    print("*****\nDONE! All data is living in the database.\n*****")
