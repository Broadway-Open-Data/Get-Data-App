from flask import Blueprint
page = Blueprint('user-interactions', __name__, template_folder='templates')
from .download_data import *
from .toggle_status import *
