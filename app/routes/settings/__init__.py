from flask import Blueprint
page = Blueprint('settings', __name__, template_folder='templates', url_prefix="/settings")

from . import api_key, change_password, settings_index, update_profile
