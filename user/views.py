from flask import Blueprint
from flask import Flask,request,redirect,render_template,session
from libs.orm import db
from user.models import  User


user_bp = Blueprint('user',__name__,url_prefix='/user')
user_bp.template_folder = './templates'


@user_bp.route('/login',methods=('POST','GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user = User.query.filter_by(username=username).one()
        except:
            db.session.rollback()
            return '用户昵称错误'

        if user.password != password:
            return '密码错误！'
        session['name'] = username
        return redirect('/weibo/home?id=%s' % user.id)
    else:
        return render_template('login.html')

@user_bp.route('/register',methods=('POST','GET'))
def register():
    if request.method == 'POST':
        pass
    else:
        return render_template('register.html')