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
from databases.models.broadway import Person, DataEdits, RacialIdentity
from databases.methods.broadway import update_person_identities
from utils.get_db_uri import get_db_uri


# Flask Stuff
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Data stuff
import pandas as pd



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

    def test_single_change(self):

        # Alt:
        my_person = Person.get_by_id(18174)

        # print(my_person.__dict__)
        curr_g_id = my_person.gender_identity_id

        new_g_id = 1 if curr_g_id==2 else 2

        # Update value
        my_person.update_info_and_track(update_dict={'gender_identity_id':new_g_id}, debug=True, test=False)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def test_multi_change(self):
        """Try changing multiple things"""

        # Alt:
        my_person = Person.get_by_id(18174)
        print("pre:", my_person.racial_identity)

        # ----------------------------------------------------------------------
        # Just track the change, don't update...

        curr_racial_ids = getattr(my_person, 'racial_identity') # maybe it's in here....

        if len(curr_racial_ids)==2:
            new_racial_identity = ['white']
        else:
            new_racial_identity = ['white','british']


        update_person_identities(18174, 'racial_identity', new_racial_identity, track_changes=True)

        print("post:", my_person.racial_identity)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def update_gender(self):
        """Try changing multiple things"""

        # Alt:
        my_person = Person.get_by_id(18174)
        print("gender identity:", my_person.gender_identity_id, my_person.gender_identity)
        


    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Done with this function...






if __name__ =='__main__':

    args = parser.parse_args()

    db_app = ConnectApp()

    if 'query_all_users' in args.function_name:
        all_user_ids = db_app.query_all_users()
        print(all_user_ids)

    # Test the functionality of the update stuff
    if 'test_single_change' in args.function_name:
        db_app.test_single_change()

    # Test the functionality of the update stuff
    if 'test_multi_change' in args.function_name:
        db_app.test_multi_change()







#
