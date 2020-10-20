from flask import Blueprint
page = Blueprint('people', __name__, template_folder='templates', url_prefix="/people")
from . import index
from . import people
