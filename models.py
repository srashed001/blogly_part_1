"""Models for Blogly."""

from enum import unique
from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy.orm import backref

db = SQLAlchemy()

def connect_db(app):
    db.app = app 
    db.init_app(app)

class User(db.Model):
    """creates user model class"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    img_url = db.Column(db.String, nullable=False)

    posts = db.relationship('Post', backref= 'users', cascade='all, delete-orphan')

    def __repr__(self):
        u = self 
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} img_url={u.img_url}>"

class Post(db.Model):
    """creates post model class"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id') )

    @property
    def friendly_date(self):

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
        p = self 
        return f"<Post id={p.id} title={p.title} content={p.content} created_at{p.created_at}>"

class PostTag(db.Model):
    """create post_tag model class"""

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, )
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, )

    def __repr__(self):
        pt = self 
        return f"<PostTag post_id={pt.post_id} tag_id={pt.tag_id}>"

class Tag(db.Model):
    """creates tag model class"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.Text, unique=True)

    posts = db.relationship('Post', secondary= 'post_tags', backref='tags')

    def __repre__(self):
        t = self 
        return f"<Tag id={t.id} name={t.name}>"
    


