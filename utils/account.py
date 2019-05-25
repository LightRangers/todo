from models.auth import User, Post
from models.db import DBSession
import hashlib

# md5加密

db_session = DBSession()


def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()


# 用户登录验证
def authenticate(username, password):
    return User.get_password(username) == hashed(password)


# 注册
def register(username, password):
    s = DBSession()
    s.add(User(name=username, password=hashed(password)))
    s.commit()
    s.close()


# 上传图片
def add_post(img_url, thumb_url, username):
    session = DBSession()
    user = session.query(User).filter_by(name=username).first()
    post = Post(image_url=img_url, thumb_url=thumb_url, user=user)
    session.add(post)
    session.commit()
    post_id = post.id
    session.close()
    return post_id


def get_all_posts():
    session = DBSession()
    posts = session.query(Post).all()
    return posts


def get_post(post_id):
    post = db_session.query(Post).filter_by(id=post_id).first()
    return post
