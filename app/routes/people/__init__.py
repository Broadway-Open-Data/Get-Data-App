from flask import Blueprint
page = Blueprint('people', __name__, template_folder='templates', url_prefix="/people")
from . import people_index
from . import people
