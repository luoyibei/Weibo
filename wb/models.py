from libs.orm import db



class Wb(db.Model):
    __tablename__ = 'wb'

    id = db.Column(db.Integer,primary_key=True)
    wbname = db.Column(db.String(20),nullable=False)
    u_name = db.Column(db.String(20))
    wbtime = db.Column(db.Date)
    wbcontent = db.Column(db.Text)