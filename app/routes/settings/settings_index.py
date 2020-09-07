from flask import render_template
from flask_login import login_required
import common
from . import page

@page.route("/", methods=['GET','POST'])
@login_required
def settings():
    """
    Allow a user to change their password and stuff
    """

    current_status = common.curr_dev_mode()
    if not current_status:
        current_status = False

    return render_template('settings/settings.html',title='Settings', current_status=current_status)
