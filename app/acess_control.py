from functools import wraps
from flask import g, request, redirect, url_for

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not g.user or role not in g.user.roles:
                return redirect(url_for('login', next=request.url))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
