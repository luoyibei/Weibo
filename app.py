from flask import Flask,request,redirect,render_template,session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
import pymysql


from libs.orm import db
from user.views import user_bp
from wb.views import wb_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:19971231@localhost/Weibo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
manger = Manager(app)
migrate = Migrate(app,db)
manger.add_command('db',MigrateCommand)
app.secret_key = r'wdcyqgdeiuwyt38r79108-0i!#!$#^%$gvwui][-'
db.init_app(app)


@app.route('/')
def hello_world():
    return redirect('/wb/home')


app.register_blueprint(user_bp)
app.register_blueprint(wb_bp)

if __name__ == '__main__':
    manger.run()
