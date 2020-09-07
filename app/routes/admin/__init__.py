from flask import Blueprint
page = Blueprint('admin', __name__, template_folder='templates', url_prefix="/admin")

from . import admin_index, manage_roles, manage_users
