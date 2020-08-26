from flask import Blueprint
from flask import Flask,request,redirect,render_template,session
from libs.orm import db
from user.models import  User
from libs.utils import login_required


user_bp = Blueprint('user',__name__,url_prefix='/user')
user_bp.template_folder = './templates'




@user_bp.route('/login',methods=('POST','GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user = User.query.filter_by(username=username).one()
        except Exception as e:
            db.session.rollback()
            return render_template('login.html',err='您输入的帐号有误')

        if user.password != password:
            return render_template('login.html',err='您输入的密码有误')
        session['name'] = user.username
        return redirect('/wb/home')
    else:
        return render_template('login.html')



@user_bp.route('/register',methods=('POST','GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password1 = request.form.get('password1').strip()
        password2 = request.form.get('password2').strip()
        gender = request.form.get('gender').strip()
        city = request.form.get('city').strip()
        if not password1 or password1 != password2:
            return render_template('register.html',err='密码不符合要求')
        user = User(username=username,password=password2,gender=gender,city=city)
        db.session.add(user)
        try:
            db.session.commit()
            return redirect('/user/login')
        except Exception as e:
            db.session.rollback()
            return render_template('register.html',err='您的帐号已被占用')

    else:
        return render_template('register.html')


@user_bp.route('/info')
@login_required
def info():
    username = session['name']
    user = User.query.filter_by(username=username).one()
    return render_template('info.html',user=user)


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
