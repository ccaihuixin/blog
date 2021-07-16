from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostsForm(FlaskForm):
    # 设置字段的其他属性使用render_kw完成
    content = TextAreaField('这一刻的想法', render_kw={'placeholder': '这一刻的想法'},
                            validators=[DataRequired(), Length(1, 128, message="长度要介于1，128之间")])
    submit = SubmitField('发表')
