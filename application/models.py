from application import db
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy import desc , Index
from datetime import datetime

class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR


likes = db.Table('likes',
    db.Column('post_id', db.Integer, db.ForeignKey('post.post_id')),
    db.Column('user_id', db.Integer, db.ForeignKey('social_user.id'))
)

dislikes = db.Table('dislikes',
    db.Column('post_id', db.Integer, db.ForeignKey('post.post_id')),
    db.Column('user_id', db.Integer, db.ForeignKey('social_user.id'))
)


class SocialUser(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=50), unique=True ,nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer())
    gender = db.Column(db.String(length=10))
    profile_pic = db.Column(db.LargeBinary())
    posts = db.relationship('Post', backref='social_user')
    liked = db.relationship("Post",secondary=likes,  backref='liked_by')
    disliked = db.relationship("Post", secondary=dislikes , backref='disliked_by')
    comments = db.relationship("Comment", backref='user')

    def __repr__(self):
        return f"id : {self.id}, username : {self.username} , email : {self.email}"


class Post(db.Model):
    post_id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.Text())
    social_user_id = db.Column(db.Integer(), db.ForeignKey('social_user.id'))
    comments = db.relationship('Comment', backref='post')

    __ts_vector__ = db.Column(TSVector(), db.Computed(
        "to_tsvector('english', title || ' ' || content)", persisted=True
    ))

    __table_args__ = (Index('ix_post___ts_vector',
                            __ts_vector__, postgresql_using='gin'), )

    def __str__(self):
        return f"id : {self.post_id}, title : {self.title}, content : {self.content}, user : {self.social_user_id}"


class Auth(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('social_user.id'))
    auth_token = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"  id : {self.id} userid : {self.user_id} token : {self.auth_token}"


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    content = db.Column(db.String(), nullable=False)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.post_id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('social_user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now() )

    def __repr__(self):
        return f"cid: {self.id}, comment: {self.content} Post_id: {self.post_id} User_id: {self.user_id} Date:{self.date_posted}"