from flask import session
from flask import redirect

def login_required(view_func):
    def check_session(*args,**kwargs):
        name = session.get('name')
        if not name :
            return redirect('/user/login')
        else:
            return view_func(*args,**kwargs)
    return check_session
