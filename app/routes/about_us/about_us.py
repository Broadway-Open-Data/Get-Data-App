from flask import render_template, Blueprint
from . import page

@page.route("/about")
def contributors():
    """Always allow"""

    return render_template('about_us/contributors.html', title="Contributors")
