from flask_login import current_user

from databases.models.users import User

def set_view_mode(val):
    """must be an int"""
    assert(isinstance(val, int))
    my_user = User.find_user_by_id(current_user.id)
    my_user.update_info({"view_mode":val})
    my_user.save_to_db()

# def get_view_mode():
#     my_user = User.find_user_by_id(current_user.id)
#     return my_user.view_mode
