import functools
from flask import abort
from flask_jwt_extended import current_user

def is_admin(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        print(current_user.roles)
        if "Admin" not in [role.name for role in current_user.roles]:
            abort(403)
        return f(*args, **kwargs)
    return wrapped