from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[list['Post']] = relationship(back_populates='user')
    comments: Mapped[list['Comment']] = relationship(back_populates='author_comment')
    follower: Mapped[list['Follower']] = relationship(back_populates='follower_user')
    following: Mapped[list['Follower']] = relationship(back_populates='following_user')

class Post(db.Model):
    __tablename__ = 'post'
    post_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped['User'] = relationship(back_populates='posts')
    media: Mapped[list['Media']] = relationship(back_populates='post')
    comments: Mapped[list['Comment']] = relationship(back_populates='post')

class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(100))
    author_id: Mapped[str] = mapped_column(ForeignKey('user.user_id'))
    author_comment: Mapped['User'] = relationship(back_populates='comments')
    post_id: Mapped[int] = mapped_column(ForeignKey('post.post_id'))
    post: Mapped['Post'] = relationship(back_populates='comments')

class MediaType(enum.Enum):
    VIDEO = 'video'
    IMAGEN = 'imagen'

class Media(db.Model):
    __tablename__ = 'media'
    media_id: Mapped[int] = mapped_column(primary_key=True)
    media_type:Mapped[MediaType] = mapped_column(Enum(MediaType))
    url: Mapped[str] = mapped_column(String(100))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.post_id'))
    post: Mapped['Post'] = relationship(back_populates='media')

class Follower(db.Model):
    __tablename__ = 'follower'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    follower_user: Mapped['User'] = relationship(back_populates='follower')
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    following_user: Mapped['User'] = relationship(back_populates='following')
