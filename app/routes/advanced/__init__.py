from flask import Blueprint
page = Blueprint('advanced', __name__, template_folder='templates', url_prefix="/advanced")
from .get_data import *
