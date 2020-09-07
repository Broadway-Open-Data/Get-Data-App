from flask import redirect, url_for, \
    flash, render_template, request, jsonify
from flask_login import login_required
# flasks stuff
from common.extensions import cache

# ------------------------------------------------------------------------------

from . import page

# Allow the user to request specific data from the app
@page.route('/explore/')
@login_required
def explore_index():
    return render_template('analyze/explore/index.html', title='Explore')
