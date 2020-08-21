from flask import Blueprint, render_template
from flask_login import login_required


page = Blueprint('settings', __name__, template_folder='templates')

@page.route("/settings")
@login_required
def settings():
    """
    Allow a user to change their password and stuff
    """

    return render_template('settings/settings.html',title='Settings')
