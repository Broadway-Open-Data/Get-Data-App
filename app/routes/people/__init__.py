# only allow these roles to view these pages...
accepted_roles = [
    'admin-master'
    'admin-master-2'
    'data.admin'
    'data.editor'
    'data.viewer'
    'user-approval.admin'
    'user-approval.editor'
]


from flask import Blueprint
page = Blueprint('people', __name__, template_folder='templates', url_prefix="/people")
from . import people_index
from . import view_people
