from flask import send_from_directory, Blueprint
from flask_login import current_user, login_required
from flask import render_template


page = Blueprint('admin', __name__, template_folder='templates')
@page.route("/admin")
@login_required
def admin():
    """Only allow admin users"""
    if not current_user.is_admin():
        return redirect("/")
    # Otherwise, proceed
    return render_template('admin/admin.html',title='Admin')
