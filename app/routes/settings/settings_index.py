from flask import Blueprint, render_template, request
from flask_login import login_required


page = Blueprint('settings', __name__, template_folder='templates')

@page.route("/settings", methods=['GET','POST'])
@login_required
def settings():
    """
    Allow a user to change their password and stuff
    """

    return render_template('settings/settings.html',title='Settings')


@page.route('/get_toggled_status')
def toggled_status():
    current_status = request.args.get('status')
    print(current_status)
    if current_status == 'ON':
        return 'OFF'
    else:
        return 'ON'
