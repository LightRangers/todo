from models.auth import User
from models.db import DBSession
import hashlib


# md5加密
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
