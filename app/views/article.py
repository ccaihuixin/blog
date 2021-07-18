from flask import Blueprint, render_template
from app.forms import PostsForm
from flask_login import login_required
article = Blueprint('article', __name__)


@article.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    form = PostsForm()
    return render_template('article/publish.html', form=form)
