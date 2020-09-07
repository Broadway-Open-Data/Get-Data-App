from flask import Blueprint, render_template, request
from flask_login import login_required
import user_interactions

page = Blueprint('settings', __name__, template_folder='templates')

@page.route("/settings", methods=['GET','POST'])
@login_required
def settings():
    """
    Allow a user to change their password and stuff
    """

    current_status = user_interactions.curr_dev_mode()
    if not current_status:
        current_status = False

    return render_template('settings/settings.html',title='Settings', current_status=current_status)


@page.route('/get_toggled_status')
def toggled_status():
    current_status = request.args.get('status')

    if current_status == 'Developer Mode':
        user_interactions.toggle_dev_mode(False)
        return 'Analyst Mode'
    else:
        user_interactions.toggle_dev_mode(True)
        return 'Developer Mode'
