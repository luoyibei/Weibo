from flask import Blueprint
from flask import Flask, request, redirect, render_template, session
from libs.orm import db
from user.models import User, Follow
from libs.utils import login_required

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_bp.template_folder = './templates'


@user_bp.route('/login', methods=('POST', 'GET'))
def login():
    '''登录'''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user = User.query.filter_by(username=username).one()
        except Exception as e:
            db.session.rollback()
            return render_template('login.html', err='您输入的帐号有误')

        if user.password != password:
            return render_template('login.html', err='您输入的密码有误')
        session['name'] = user.username
        session['u_id'] = user.id
        return redirect('/wb/home')
    else:
        return render_template('login.html')


@user_bp.route('/register', methods=('POST', 'GET'))
def register():
    '''注册'''
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password1 = request.form.get('password1').strip()
        password2 = request.form.get('password2').strip()
        gender = request.form.get('gender').strip()
        city = request.form.get('city').strip()
        if not password1 or password1 != password2:
            return render_template('register.html', err='密码不符合要求')
        user = User(username=username, password=password2, gender=gender, city=city)
        db.session.add(user)
        try:
            db.session.commit()
            return redirect('/user/login')
        except Exception as e:
            db.session.rollback()
            return render_template('register.html', err='您的帐号已被占用')

    else:
        return render_template('register.html')


@user_bp.route('/info')
@login_required
def info():
    '''查看个人信息'''
    username = session['name']
    user = User.query.filter_by(username=username).one()
    return render_template('info.html', user=user)


@user_bp.route('/other')
@login_required
def other():
    '''查看别的用户的信息'''
    other_id = int(request.args.get('uid')) # 其他人的 uid
    if other_id == session.get('u_id'):
        return redirect('/user/info')
    user = User.query.get(other_id)  # 其他人

    self_uid = session.get('u_id')
    if self_uid:
        if Follow.query.filter_by(u_id=self_uid, f_id=other_id).count():
            is_follow = True
        else:
            is_follow = False
    else:
        is_follow = False

    return render_template('other.html', user=user, is_follow=is_follow)


@user_bp.route('/follow')
@login_required
def follow():
    '''关注博主'''
    f_id = int(request.args.get('f_id'))

    u_id = session.get('u_id')

    if u_id == f_id:
        err = '不允许自己关注自己哦~'
        return render_template('other.html', err=err)

    fw = Follow(u_id=u_id, f_id=f_id)
    try:
        '''关注'''
        User.query.filter_by(id=u_id).update({'n_follow': User.n_follow + 1})
        User.query.filter_by(id=f_id).update({'n_fans': User.n_fans + 1})
        db.session.add(fw)
        db.session.commit()
    except Exception:
        '''取消关注'''
        db.session.rollback()
        User.query.filter_by(id=u_id).update({'n_follow': User.n_follow - 1})
        User.query.filter_by(id=f_id).update({'n_fans': User.n_fans - 1})
        Follow.query.filter_by(f_id=f_id, u_id=u_id).delete()

        db.session.commit()
    return redirect('/user/other?uid=%s' % f_id)



@user_bp.route('/fans')
@login_required
def show_fans():
    '''粉丝列表'''
    u_id = session['u_id']
    fans = Follow.query.filter_by(f_id=u_id).values('u_id')
    fans_uids = [u_id for (u_id,) in fans]

    users = User.query.filter(User.id.in_(fans_uids))
    return render_template('fans.html', users=users)



@user_bp.route('/author')
def author():
    return render_template('author.html')

@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
