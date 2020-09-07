import os
from pathlib import Path

# Flask stuff
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from databases.db import db

# Internal packages
import common
import utils
import routes

def create_app():
    # initialize
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = utils.get_db_uri("users")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # This is otherwise done through the bash profile
    if not os.environ.get("FLASK_SECRET_KEY"):
        os.environ['FLASK_SECRET_KEY'] = "some key"

    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
    app.config['DEBUG'] = not utils.is_aws()
    os.environ['FLASK_ENV'] = 'production' if utils.is_aws() else 'development'


    csrf = CSRFProtect(app)

    # Configure the cache
    common.cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': Path('/tmp')})


    # Configure the db
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app

def register_blueprint(app):
    """
    Register the blueprints for the app
    """

    my_pages = [
        routes.admin.page,
        routes.analyze.page,
        routes.api.page,
        routes.auth.page,
        routes.internal.page,
        routes.settings.page,
        routes.user_interactions.page
        ]

    for page in my_pages:
        app.register_blueprint(page)