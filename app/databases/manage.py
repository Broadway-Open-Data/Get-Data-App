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
from databases import db
from utils.get_db_uri import get_db_uri


# ------------------------------------------------------------------------------


class ManagerApp():

    def __init__(self, **kwargs):

        self.db_name = kwargs.get('db_name', 'users')
        # Instantiate a blank app
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri(self.db_name)
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


        # Only import necessary models...
        if self.db_name =='users':
            import databases.models.users as _
        else:
            import databases.models.broadway as _ 

        # instantiate the db
        db.init_app(app=self.app)
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
