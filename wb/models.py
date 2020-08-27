from libs.orm import db



class Wb(db.Model):
    '''添加微博表'''
    __tablename__ = 'wb'

    id = db.Column(db.Integer,primary_key=True)
    u_name = db.Column(db.String(20),nullable=False)
    n_thumb = db.Column(db.Integer, nullable=False, index=True, default=0)
    n_follow = db.Column(db.Integer, nullable=False, index=True, default=0)
    wbtime = db.Column(db.DateTime,nullable=False)
    wbcontent = db.Column(db.Text,nullable=False)




class Comment(db.Model):
    '''添加评论表'''
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    u_name = db.Column(db.String(20),nullable=False,index=True)
    w_id = db.Column(db.Integer,nullable=False,index=True)
    c_id = db.Column(db.Integer, nullable=False,index=True,default=0)
    cmcontent = db.Column(db.Text, nullable=False)
    cmtime = db.Column(db.DateTime, nullable=False)


    @property
    def upper(self):
        if self.c_id == 0:
            return None
        else:
            return Comment.query.get(self.c_id)


class Thumb(db.Model):
    '''添加点赞表'''
    __tablename__ = 'thumb'
    u_id = db.Column(db.Integer, primary_key=True)
    w_id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.Boolean,nullable=False,default=False)


class Follow(db.Model):
    '''添加点赞表'''
    __tablename__ = 'follow'
    u_id = db.Column(db.Integer, primary_key=True)
    w_id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.Boolean,nullable=False,default=False)