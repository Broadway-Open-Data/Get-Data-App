from .models import User

def get_all_nonapproved_users(self):
    """Gets all users who aren't approved"""
    return User.query.filter_by(approved=False)
