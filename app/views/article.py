from flask import Blueprint, render_template, url_for, redirect, request
from app.forms import PostsForm,ChangePostsForm
from flask_login import login_required, current_user
from app.models import Posts
from app.extensions import db
from datetime import datetime

article = Blueprint('article', __name__)


@article.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    form = PostsForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u = current_user._get_current_object()  # 获取原来的user对象
            p = Posts(title=form.title.data, describe=form.content.data[0:145] + '……', content=form.content.data,
                      user=u)
            # 添加进入数据库
            db.session.add(p)
            return redirect(url_for("main.index"))
    return render_template('article/publish.html', form=form)


@article.route('/mypublish', methods=['GET'])
@login_required
def mypublish():
    u = current_user._get_current_object()  # 获取原来的user对象
    page = request.args.get('page', 1, type=int)  # 获取请求中的分页的页码，默认是第一页并转换为int
    pagination = Posts.query.filter_by(uid=u.id).order_by(Posts.timestamp.desc()).paginate(page,
                                                                                           per_page=5)  # err_out 不打印错误信息
    posts = pagination.items
    return render_template('article/mypublish.html', posts=posts, pagination=pagination)


@article.route('/article_detail', methods=['GET'])
def article_detail():
    id = request.args.get('id')
    posts = Posts.query.filter_by(id=id).first()
    return render_template('article/article_detail.html', posts=posts)


@article.route('/article_delete', methods=['GET'])
@login_required
def article_delete():
    id = request.args.get('id')
    result = Posts.query.filter_by(id=id).delete()
    if result is not None:
        return redirect(url_for('article.mypublish'))


@article.route('/article_change', methods=['GET', 'POST'])
@login_required
def article_change():
    form = ChangePostsForm()
    if request.method == 'GET':
        id = request.args.get('id')
        posts = Posts.query.filter_by(id=id).first()
        form.id.data = posts.id
        form.title.data = posts.title
        form.content.data = posts.content
        return render_template('article/publish.html', form=form)
    else:
        if form.validate_on_submit():
            id = Posts.query.filter_by(id=form.id.data).update(
                {"title": form.title.data, "content": form.content.data, "describe": form.content.data[0:145] + '……',
                 "timestamp": datetime.utcnow()})
            return redirect(url_for("article.mypublish"))


@article.route('/article_search', methods=['GET'])
def article_search():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter(Posts.title.like('%{keyword}%'.format(keyword=keyword))).order_by(Posts.timestamp.desc()).paginate(page, per_page=5)
    posts = pagination.items
    print(posts)
    return render_template('article/search.html', posts=posts, pagination=pagination,keyword=keyword)
