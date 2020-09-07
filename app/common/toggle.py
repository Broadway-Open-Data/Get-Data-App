from flask_login import current_user

from databases.db import User

def toggle_dev_mode(val):
    my_user = User.find_user_by_id(current_user.id)
    my_user.toggle_developer_mode(val)

def curr_dev_mode():
    my_user = User.find_user_by_id(current_user.id)
    return my_user.developer_mode
