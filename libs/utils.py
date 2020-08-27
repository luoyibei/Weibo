from flask import session
from flask import redirect
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def check_session(*args,**kwargs):
        name = session.get('name')
        if not name :
            return redirect('/user/login')
        else:
            return view_func(*args,**kwargs)
    return check_session
