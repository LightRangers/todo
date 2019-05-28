from models.auth import User, Post
import hashlib


# md5加密


def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()


# 用户登录验证
def authenticate(username, password):
    return User.get_password(username) == hashed(password)


class HandlerORM:
    '''
    辅助操作数据库的工具类，结合RequestHandler使用
    '''

    def __init__(self, db_session):
        '''
        :param db_session: 由handler进行实例化和close
        '''
        self.db = db_session

    def get_user(self, username):
        user = self.db.query(User).filter_by(name=username).first()
        return user

    # 注册
    def register(self, username, password):
        self.db.add(User(name=username, password=hashed(password)))
        self.db.commit()

    # 上传图片
    def add_post(self, img_url, thumb_url, username):
        user = self.get_user(username)
        post = Post(image_url=img_url, thumb_url=thumb_url, user=user)
        self.db.add(post)
        self.db.commit()
        post_id = post.id
        return post_id

    def get_all_posts(self, ):
        posts = self.db.query(Post).all()
        return posts

    def get_posts_for(self, username):
        user = self.get_user(username)
        posts = self.db.query(Post).filter_by(user=user).all()
        return posts

    def get_post(self, post_id):
        '''
        返回特定id的post实例
        :param post_id:
        :return:
        '''

        post = self.db.query(Post).filter_by(id=post_id).first()
        return post
