from flask import Blueprint
page = Blueprint('about_us', __name__, template_folder='templates')

from . import about_us, contributors
