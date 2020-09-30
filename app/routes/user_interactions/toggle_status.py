from flask import request
import common

from . import page

@page.route('/get_view_status')
def set_view_mode():
    new_status = request.args.get('new_status')
    new_status = int(new_status)

    # change the new status
    common.set_view_mode(new_status)

    return str(new_status)
