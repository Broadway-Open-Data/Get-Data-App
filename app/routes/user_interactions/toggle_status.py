from flask import request
import common

from . import page

@page.route('/get_toggled_status')
def toggled_status():
    current_status = request.args.get('status')

    if current_status == 'Developer Mode':
        common.toggle_dev_mode(False)
        return 'Analyst Mode'
    else:
        common.toggle_dev_mode(True)
        return 'Developer Mode'
