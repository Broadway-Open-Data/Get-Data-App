from flask import render_template, Blueprint
from . import page

@page.route("/about/contributors")
def contributors():
    """Always allow"""

    return render_template('about/contributors.html', title="Contributors")
