from flask import Blueprint
page = Blueprint('internal', __name__, template_folder='templates')

from . import format, verify
