from flask import Blueprint
page = Blueprint('auth', __name__, template_folder='templates')

from . import forgot_password, login, signup
