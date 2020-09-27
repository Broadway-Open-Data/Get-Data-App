from flask import Blueprint
page = Blueprint('about', __name__, template_folder='templates')

from . import about_us, contributors
