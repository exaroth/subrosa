from flask import request, url_for, session, redirect
from main import app
from functools import wraps



def login_required(f):

    """
    Simple authorization decorator 
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated

def dynamic_content(f):
    """
    Redirects to index if DYNAMIC_SITE
    variable is set to False
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if not app.config.get("DYNAMIC_SITE", False):
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated
