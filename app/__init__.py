import os
from pathlib import Path

# Flask stuff
from flask import Flask
from flask_wtf.csrf import CSRFProtect

# Internal packages
import utils
import databases
import common
# Order is important here
import forms
import routes



# import a second time, why not...
from databases import db

def create_app():
    # initialize
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = utils.get_db_uri("users")
    app.config['SQLALCHEMY_BINDS'] = {
        'users': utils.get_db_uri("users"),
        'broadway': utils.get_db_uri("broadway"),
    }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECURITY_TRACKABLE']=True
    # This is otherwise done through the bash profile
    if not os.environ.get("FLASK_SECRET_KEY"):
        os.environ['FLASK_SECRET_KEY'] = "some key"

    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
    app.config['DEBUG'] = not utils.is_aws()
    os.environ['FLASK_ENV'] = 'production' if utils.is_aws() else 'development'


    csrf = CSRFProtect(app)

    # Configure the cache
    common.cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': Path('/tmp')})

    SQLALCHEMY_DATABASE_URI = 'postgres://db_user:db_pw@localhost:5432/db_name'

    # Configure the db
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # Set the max length, just once...
        db.get_engine(bind='broadway').execute("SET session group_concat_max_len=30000;")

    return app

def register_blueprint(app):
    """
    Register the blueprints for the app
    """

    # I wish there was a better way to do this...
    my_pages = [
        routes.about.page,
        routes.admin.page,
        routes.advanced.page,
        routes.analyze.page,
        routes.api.page,
        routes.auth.page,
        routes.index.page,
        routes.internal.page,
        routes.people.page,
        routes.settings.page,
        routes.user_interactions.page
        ]

    for page in my_pages:
        app.register_blueprint(page)
