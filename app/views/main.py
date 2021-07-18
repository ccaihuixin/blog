from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from app.forms import PostsForm
from app.models import Posts
from app.extensions import db

main = Blueprint('main', __name__)
from flask_login import current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    # form = PostsForm()
    # if form.validate_on_submit():
    #     if current_user.is_authenticated:
    #         # 根据表单提交的数据常见对象
    #         u = current_user._get_current_object()  # 获取原生的user对象
    #         p = Posts(content=form.content.data, user=u)
    #         # 然后写入数据库
    #         db.session.add(p)
    #         return redirect(url_for('main.index'))
    #     else:
    #         flash('登陆后才能发表')
    #         return redirect(url_for('user.login'))
    # 读取博客，并分配到模板中，然后再模板中渲染
    # 按照发表时间，降序排列
    # 只获取发表的帖子，过滤回复的贴子
    # posts=Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).all()
    # 分页处理
    # 默认是第一页
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=5,
                                                                                        error_out=False)
    posts = pagination.items
    return render_template('main/index.html', posts=posts, pagination=pagination)
