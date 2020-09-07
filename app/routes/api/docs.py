from flask import send_from_directory, redirect, url_for, \
    flash, render_template, request
from flask_login import login_required


from . import page
@page.route("/docs")
@login_required
def api_docs():
    """Documentation"""
    return render_template('api/docs.html',title='API Docs')
