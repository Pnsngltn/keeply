from flask import redirect, render_template, session
from functools import wraps

def login_required(f):
    """
        Decorate routes to require login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def conflict(s1, e1, s2, e2):
    return not (e1 <= s2 or s1 >= e2)


