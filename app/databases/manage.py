import os
import json
import sys
import datetime
import uuid
# Correct the path
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# db things
from databases import models
from flask_sqlalchemy import SQLAlchemy
from databases import db, models
# from flask_alchemydumps import AlchemyDumps


from utils.get_db_uri import get_db_uri


# ------------------------------------------------------------------------------


class ManagerApp():

    def __init__(self, **kwargs):

        self.db_name = kwargs.get('db_name', 'users')
        # Instantiate a blank app
        self.app = Flask(__name__)
        # self.app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri(self.db_name)
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.app.config['SQLALCHEMY_BINDS'] = {
            'users': get_db_uri("users"),
            'broadway': get_db_uri("broadway"),
        }


        # Configure the db
        db.init_app(self.app)
        # db = SQLAlchemy(self.app)
        with self.app.app_context():
            db.create_all()
            # db.create_all(bind=['users','broadway'])



        # extend_existing=True

        # ------------------------------------------------------------------------------





        # Instantiate the migration manager
        migrate = Migrate(self.app, db)

        self.manager = Manager(self.app)
        self.manager.add_command('db', MigrateCommand)




# ------------------------------------------------------------------------------

# # Create a hello world function
# @manager.command
# def hello(name=''):
#     print (f"hello {name}")
#
# # Create a create_all function
# @manager.command
# def create_all():
#     db.create_all()


# ------------------------------------------------------------------------------


if __name__ == '__main__':
    m = ManagerApp()
    m.manager.run()
