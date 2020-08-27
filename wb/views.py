from flask import Blueprint
from flask import Flask, request, redirect, render_template, session
from libs.orm import db
from user.models import User
from wb.models import Wb,Comment,Thumb,Follow
from libs.utils import login_required
import datetime
import math

wb_bp = Blueprint('wb', __name__, url_prefix='/wb')
wb_bp.template_folder = './templates'


# 钩子函数
# 信息验证，查看是否已登录
# check_path = ['/user/info','/wb/mywb']
#
# @wb_bp.before_app_request
# def process_request():
#     if request.path in check_path:
#         username = session['name']
#         if not username:
#             return render_template('login.html',err='用户未登录!')


@wb_bp.route('/home')
def home():
    '''微博主页'''
    # u_name = session.get('name')
    # wbs = Wb.query.all()
    # 获取页码数以及设置默认页码数
    page = int(request.args.get('page', 1))
    page_prev = page - 1
    page_next = page + 1
    per_page = 2

    offset = per_page * (page - 1)
    wbs = Wb.query.order_by(Wb.wbtime.desc()).limit(per_page).offset(offset)

    max_page = math.ceil(Wb.query.count() / per_page)

    if page <= 3 :
        start,end = 1,min(7,max_page)
    elif page > (max_page - 3):
        start,end = (max_page-6),max_page
    else:
        start,end = (page - 3),(page + 3)
    pages = range(start, end + 1)

    # paginate = Wb.query.paginate(page=int(page), per_page=2)
    # wbs = paginate.items
    return render_template('home.html',page_prev=page_prev,page_next=page_next,page=page,pages=pages,wbs=wbs)


@wb_bp.route('/read')
def read():
    '''阅读微博'''
    id = request.args.get('id')
    wb = Wb.query.get(id)
    session['w_id'] = id
    '''展示所有的评论'''
    comments = Comment.query.filter_by(w_id=id).order_by(Comment.cmtime.desc()).all()
    thumb = Thumb.qyery.filter_by(u_id=session['u_id']).filter_by(w_id=id)
    follow = Follow.qyery.filter_by(u_id=session['u_id']).filter_by(w_id=id)
    return render_template('read.html', wb=wb,comments=comments,thumb=thumb,follow=follow)


@wb_bp.route('/thumb')
def thumb():
    '''点赞'''

    w_id = request.args.get('id')
    u_id = session.get('u_id')
    wb = Wb.query.filter_by(id=w_id).one()
    wb.n_thumb = wb.n_thumb + 1
    '''提交wb'''
    db.session.commit()

    thumb = Thumb(u_id=u_id,w_id=w_id,flag=True)
    db.session.add(thumb)
    '''提交Thumb'''
    db.session.commit()

    redirect('/wb/read?id=%s' % w_id)



@wb_bp.route('/de_thumb')
def de_thumb():
    '''取消点赞'''
    w_id = request.args.get('id')
    u_id = session.get('u_id')
    wb = Wb.query.filter_by(id=w_id).one()
    wb.n_thumb = wb.n_thumb - 1
    '''提交wb'''
    db.session.commit()

    Thumb.query.filter_by(w_id=w_id,u_id=u_id).delete()
    '''提交Thumb'''
    db.session.commit()

    redirect('/wb/read?id=%s' % w_id)


@wb_bp.route('/follow')
def follow():
    '''关注博主'''

    w_id = request.args.get('id')
    u_id = session.get('u_id')
    wb = Wb.query.filter_by(id=w_id).one()
    wb.n_follow = wb.n_follow+ 1
    '''提交wb'''
    db.session.commit()

    follow = Follow(u_id=u_id,w_id=w_id,flag=True)
    db.session.add(follow)
    '''提交follow'''
    db.session.commit()

    redirect('/wb/read?id=%s' % w_id)


@wb_bp.route('/de_follow')
def de_follow():
    '''取消关注'''
    w_id = request.args.get('id')
    u_id = session.get('u_id')
    wb = Wb.query.filter_by(id=w_id).one()
    wb.n_follow = wb.n_follow - 1
    '''提交wb'''
    db.session.commit()

    Follow.query.filter_by(w_id=w_id,u_id=u_id).delete()
    '''提交follow'''
    db.session.commit()

    redirect('/wb/read?id=%s' % w_id)


@wb_bp.route('/comment',methods=('POST',))
@login_required
def comment():
    '''添加评论'''
    cmcontent =  request.form.get('cmcontent')
    u_name = session.get('name')
    # # user = User.query.filter_by(username=u_name).one()
    w_id = session.get('w_id')
    # wb = Wb.query.filter_by(id=w_id).one()
    cmtime = datetime.datetime.now()
    comment = Comment(u_name=u_name,w_id=w_id,cmtime=cmtime,cmcontent=cmcontent)
    db.session.add(comment)
    db.session.commit()
    return redirect('/wb/read?id=%s' % w_id)


@wb_bp.route('/reply',methods=('POST',))
@login_required
def reply():
    '''添加回复'''
    u_name = session.get('name')
    w_id = request.form.get('w_id')
    c_id = request.form.get('c_id')
    cmcontent = request.form.get('cmcontent')
    cmtime = datetime.datetime.now()

    comment = Comment(u_name=u_name, w_id=w_id, cmtime=cmtime,c_id=c_id, cmcontent=cmcontent)
    db.session.add(comment)
    db.session.commit()

    return redirect('/wb/read?id=%s' % w_id)


@wb_bp.route('/de_comment')
def de_comment():
    '''删除回复'''
    w_id = session.get('w_id')
    c_id = request.args.get('c_id')
    comment = Comment.query.get(c_id)


    if comment.u_name != session.get('name'):
        err = '不允许删除别人的评论哦~'
        return render_template('read.html',err=err)
    comment.cmcontent = '当前评论已被删除'
    db.session.commit()
    return redirect('/wb/read?id=%s' % w_id)


@wb_bp.route('/mywb')
@login_required
def mywb():
    '''我的微博'''
    u_name = session['name']
    wbs = Wb.query.filter_by(u_name=u_name).all()

    return render_template('mywb.html', wbs=wbs)


@wb_bp.route('/addwb', methods=('POST', 'GET'))
def addwb():
    '''添加微博'''
    if request.method == 'POST':
        u_name = session['name']
        wbtime = datetime.datetime.now()
        wbcontent = request.form.get('wbcontent', '').strip()
        if not wbcontent:
            return render_template('addwb.html', err='微博内容不能为空')
        wb = Wb(u_name=u_name, wbtime=wbtime, wbcontent=wbcontent)
        db.session.add(wb)
        db.session.commit()
        return redirect('/wb/read?id=%s' % wb.id)
    else:
        return render_template('addwb.html')


@wb_bp.route('/updatewb', methods=('POST', 'GET'))
def updatewb():
    '''更改微博'''

    if request.method == 'POST':
        id = request.form.get('id')
        wbtime = datetime.datetime.now()
        wbcontent = request.form.get('wbcontent')
        if not wbcontent:
            return render_template('addwb.html', err='微博内容不能为空')
        wb = Wb.query.get(id)
        wb.wbtime = wbtime
        wb.wbcontent = wbcontent
        db.session.commit()
        return redirect('/wb/read?id=%s' % wb.id)
    else:
        id = request.args.get('id')
        wb = Wb.query.get(id)
        return render_template('updatewb.html', wb=wb)


@wb_bp.route('/delete')
def delete():
    '''删除微博'''
    id = request.args.get('id')
    Wb.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/wb/mywb')
