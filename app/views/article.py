from flask import Blueprint, render_template, url_for, redirect, request
from app.forms import PostsForm
from flask_login import login_required, current_user
from app.models import Posts
from app.extensions import db

article = Blueprint('article', __name__)


@article.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    form = PostsForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u = current_user._get_current_object()  # 获取原来的user对象
            p = Posts(title=form.title.data, content=form.content.data, user=u)
            # 添加进入数据库
            db.session.add(p)
            return redirect(url_for("main.index"))
    return render_template('article/publish.html', form=form)


@article.route('/mupublish', methods=['GET'])
@login_required
def mypublish():
    u = current_user._get_current_object()  # 获取原来的user对象
    page = request.args.get('page', 1, type=int)  # 获取请求中的分页的页码，默认是第一页并转换为int
    pagination = Posts.query.filter_by(uid=u.id).order_by(Posts.timestamp.desc()).paginate(page, per_page=5) # err_out 不打印错误信息
    posts = pagination.items
    return render_template('article/mypublish.html', posts=posts, pagination=pagination)
