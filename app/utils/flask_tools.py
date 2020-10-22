from flask import redirect
from flask_login import current_user
from functools import wraps


def require_role(*role):
    """make sure user has this role"""
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):


            # If one role
            if isinstance(*role, str) and not current_user.has_role(*role):
                return redirect("/")

            # If a list of roles
            if isinstance(*role, list) and not any([current_user.has_role(x) for x in role]):
                return redirect("/")
            # Otherwise
            return func(*args, **kwargs)

        return wrapped_function
    return decorator
