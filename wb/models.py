from libs.orm import db



class Wb(db.Model):
    '''添加微博表'''
    __tablename__ = 'wb'

    id = db.Column(db.Integer,primary_key=True)
    u_name = db.Column(db.String(20),nullable=False)
    wbtime = db.Column(db.DateTime,nullable=False)
    wbcontent = db.Column(db.Text,nullable=False)




class Comment(db.Model):
    '''添加评论表'''
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    u_name = db.Column(db.String(20),nullable=False)
    w_id = db.Column(db.Integer,nullable=False)
    cmcontent = db.Column(db.Text, nullable=False)
    cmtime = db.Column(db.DateTime, nullable=False)
