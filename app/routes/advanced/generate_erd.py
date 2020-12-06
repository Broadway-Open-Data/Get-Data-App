import os
from pathlib import Path

from flask import Response, request, jsonify, send_from_directory, url_for
from flask_login import login_required

import pandas as pd

# flasks stuff
from common.extensions import cache

# my stuff
import databases.methods as db_methods

# ------------------------------------------------------------------------------

from . import page

@page.route('/generate-erd/<engine_name>')
@login_required
def generate_erd(engine_name):
    """Create an erd and send path"""

    # Generate or return path?
    generate = bool(request.args.get('generate', False))

    # if generate:
    #     db_methods.get_db_ERD('broadway')


    # Get the path...
    save_dir = Path('app/static/images/databases-ERD')
    # make the dir if you need to
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    # list the dir
    my_paths = set()
    for x in os.listdir(save_dir):
        if x.startswith(engine_name):
            x_path = os.path.join(save_dir, x)
            if os.path.isfile(x_path):
                my_paths.add(x_path)


    newest_path = max(my_paths, key=os.path.getctime)
    newest_path = newest_path.replace('app/static/','')
    return send_from_directory('static', newest_path)









#
