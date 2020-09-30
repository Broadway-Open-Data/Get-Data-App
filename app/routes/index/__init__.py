from flask import Blueprint
page = Blueprint('index', __name__, template_folder='templates')

from . import index
