from flask import render_template, Blueprint
from . import page

@page.route("/about")
def about_us():
    """Always allow"""

    return render_template('about_us/about_us.html', title="About Us")
