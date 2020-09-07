from flask import Blueprint
page = Blueprint('api', __name__, template_folder='templates', url_prefix="/api")

from . import docs
