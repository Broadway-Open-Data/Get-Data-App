from flask import Blueprint
page = Blueprint('analyze', __name__, template_folder='templates', url_prefix="/analyze")
from . import analyze, explore
