from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.forms import PostsForm
from app.models import Posts
from app.extensions import db

main = Blueprint('main', __name__)
from flask_login import current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            # 根据表单提交的数据常见对象
            u = current_user._get_current_object()  # 获取原生的user对象
            p = Posts(content=form.content.data, user=u)
            # 然后写入数据库
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('登陆后才能发表')
            return redirect(url_for('user.login'))
        # 读取博客，并分配到模板中，然后再模板中渲染
        # 按照发表时间，降序排列
        # 只获取发表的帖子，过滤回复的贴子
    # posts=Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).all()
    # 分页处理
    page = request.args.get('page', 1,type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=3,
                                                                                        error_out=False)
    posts=pagination.items
    return render_template('main/index.html', form=form, posts=posts,pagination=pagination)

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
