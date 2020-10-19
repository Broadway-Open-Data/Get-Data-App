# from databases import db
from databases.models.users import User

def get_all_nonapproved_users():
    """Returns a list of all users who aren't approved"""
    return list(User.query.filter_by(approved=False))
