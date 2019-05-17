from models.auth import User


# 用户登录验证
def authenticate(username, password):
    # return User.is_exists(username, password)
    return User.get_password(username) == password
