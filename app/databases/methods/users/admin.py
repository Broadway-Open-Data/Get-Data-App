# from databases import db
from databases import models

def get_all_nonapproved_users():
    """Gets all users who aren't approved"""
    return list(models.User.query.filter_by(approved=False))
