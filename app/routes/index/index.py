from flask import render_template
from flask_login import current_user
from . import page

@page.route('/')
def index():
    # if current_user.developer_mode
    # z = current_user.view_mode
    # print(z)
    return render_template('index.html', title='Home')
