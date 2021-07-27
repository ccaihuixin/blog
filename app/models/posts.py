from app.extensions import db
from datetime import datetime

from app.models import User


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    describe = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    rid = db.Column(db.Integer, index=True, default=0)  # 回复id 默认为0 表示发表
    # 指定外键(表名.字段)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship("Comment", lazy="dynamic")
    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "describe": self.describe,
            "create_time": self.timestamp,
            "content": self.content,
            "comments_count": self.comments.count(),
            "author": self.user.to_dict() if self.user else None
        }
        return resp_dict

class Comment(db.Model):
    """评论"""
    __tablename__ = "comment"
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间
    id = db.Column(db.Integer, primary_key=True)  # 评论编号
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # 用户id
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)  # 文章id
    content = db.Column(db.Text, nullable=False)  # 评论内容
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))  # 父评论id
    parent = db.relationship("Comment", remote_side=[id])  # 自关联
    like_count = db.Column(db.Integer, default=0)  # 点赞条数

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "parent": self.parent.to_dict() if self.parent else None,
            "user": User.query.get(self.user_id).to_dict(),
            "post_id": self.post_id,
            "like_count": self.like_count
        }
        return resp_dict

class CommentLike(db.Model):
    """评论点赞"""
    __tablename__ = "comment_like"
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间
    comment_id = db.Column("comment_id", db.Integer, db.ForeignKey("comment.id"), primary_key=True)  # 评论编号
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True)  # 用户编号