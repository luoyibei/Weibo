from libs.orm import db



class User(db.Model):
    '''添加用户表'''
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(20),nullable=False)
    gender = db.Column(db.Enum('男','女','保密'))
    city = db.Column(db.String(20))
    n_follow = db.Column(db.Integer, nullable=False, index=True, default=0)
    n_fans = db.Column(db.Integer, nullable=False, index=True, default=0)



class Follow(db.Model):
    '''添加关注表'''
    __tablename__ = 'follow'
    u_id = db.Column(db.Integer, primary_key=True)
    f_id = db.Column(db.Integer, primary_key=True)