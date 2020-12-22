from flask import render_template
from flask_login import current_user
from . import page

from databases.methods.broadway import person_add_show_credit


@page.route('/')
def index():
    # if current_user.developer_mode
    # z = current_user.view_mode
    # print(z)
    my_params = dict(
        # show_id = 330662,
        show_name='Tuck Everlasting',
        show_year=2016,
        person_name='Mary Michell Campbell',
        role_name='Music Director'
    )
    person_add_show_credit(**my_params)

    return render_template('index.html', title='Home')
