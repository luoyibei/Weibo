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
        return redirect('/wb/home')
    else:
        return render_template('login.html')



@user_bp.route('/register',methods=('POST','GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        city = request.form.get('city')
        user = User(username=username,password=password,gender=gender,city=city)
        db.session.add(user)
        db.session.commit()
        return redirect('/user/login')
    else:
        return render_template('register.html')