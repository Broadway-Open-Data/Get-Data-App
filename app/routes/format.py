import os
from flask import send_from_directory, Blueprint

page = Blueprint('page_format', __name__, template_folder='templates')
@page.route('/favicon.ico')
def favicon():
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_from_directory(
        os.path.join(parent_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
        )
