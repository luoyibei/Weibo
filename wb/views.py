from flask import Blueprint
from flask import Flask,request,redirect,render_template,session
from libs.orm import db
from user.models import  User
from wb.models import Wb
import datetime


wb_bp = Blueprint('wb',__name__,url_prefix='/wb')
wb_bp.template_folder = './templates'


@wb_bp.route('/home')
def home():
    # u_name = session.get('name')
    wbs = Wb.query.all()
    return render_template('home.html',wbs=wbs)


@wb_bp.route('/mywb')
def mywb():
    u_name = session['name']
    wbs = Wb.query.filter_by(u_name=u_name).all()

    return render_template('mywb.html',wbs=wbs)


@wb_bp.route('/addwb',methods=('POST','GET'))
def addwb():
    if request.method == 'POST':
        wbname = request.form.get('wbname')
        u_name = request.form.get('u_name')
        wbtime = request.form.get('wbtime')
        wbcontent = request.form.get('wbcontent')
        wb = Wb(wbname=wbname,u_name=u_name,wbtime=wbtime,wbcontent=wbcontent)
        db.session.add(wb)
        db.session.commit()
        return redirect('/wb/mywb')
    else:
        u_name = session['name']
        wbtime = datetime.datetime.now().strftime('%Y-%m-%d')
        return render_template('addwb.html',u_name=u_name,wbtime=wbtime)


@wb_bp.route('/updatewb',methods=('POST','GET'))
def updatewb():
    if request.method == 'POST':
        id = session['wbid']
        wbname = request.form.get('wbname')
        u_name = request.form.get('u_name')
        wbtime = request.form.get('wbtime')
        wbcontent = request.form.get('wbcontent')
        Wb.query.filter_by(id=id).update({'wbname':wbname,'wbcontent':wbcontent})
        db.session.commit()
        return redirect('/wb/mywb')
    else:
        id = request.args.get('id')
        wb = Wb.query.get(id)
        session['wbid'] = id
        return render_template('updatewb.html',wb=wb)


@wb_bp.route('/delete')
def delete():
    id = request.args.get('id')
    Wb.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/wb/mywb')
