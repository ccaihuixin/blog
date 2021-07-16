from flask import Blueprint, render_template, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main/index.html')


# @main.route('/jiami/')
# def jiami():
#     return generate_password_hash('123456')
#
#
# @main.route('/check/<password>')
# def check(password):
#     # 密码校验函数:加密后的值 密码
#     # 正确:True, 错误:False
#     if check_password_hash('pbkdf2:sha256'
#                            ':150000$NH3mb7LR$a4845fb77bc535f6de9136520ffb1647e8be4aa08101b9685f5193766abf65d2',
#                            '123456'):
#         return '密码正确'
#     else:
#         return '密码错误'
#
#
# @main.route('/generate_token/')
# def generate_token():
#     s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
#     # 加密指定的数据，以字典的形式传入
#     return s.dumps({'id': 250})
#
# @main.route('/activate/<token>')
# def activate(token):
#     s=Serializer(current_app.config['SECRET_KEY'])
#     try:
#         data=s.loads(token)
#     except:
#         return 'token有误'
#     return str(int(data.get('id')))
