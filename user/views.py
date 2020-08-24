from flask import Blueprint

user_bp = Blueprint('user',__name__,url_prefix='/user')
user_bp.template_folder = './templates'


@user_bp.route('/login')
def login():
    return 'hello'