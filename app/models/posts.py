from app.extensions import db
from datetime import datetime


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    rid = db.Column(db.Integer, index=True, default=0)  # 回复id 默认为0 表示发表
    # 指定外键(表名.字段)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
