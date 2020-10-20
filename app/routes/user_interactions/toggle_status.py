from flask import request

# import user db stuff
from flask_login import current_user
from databases.models.users import User

from . import page

@page.route('/get_view_status')
def set_view_mode():
    new_status = request.args.get('new_status')
    new_status = int(new_status)

    # change the new status
    my_user = User.find_user_by_id(current_user.id)
    my_user.update_info(update_dict={"view_mode":new_status})

    return str(new_status)
