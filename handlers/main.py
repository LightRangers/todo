import tornado.web
from pycket.session import SessionMixin
from utils.account import HandlerORM
from utils.photo import UploadImage
from models.db import DBSession


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('todo_user', None)

    def prepare(self):
        self.db_session = DBSession()
        self.orm = HandlerORM(db_session=self.db_session)

    def on_finish(self):
        self.db_session.close()


class IndexHnadeler(BaseHandler):
    '''
    首页，用户上传图片的展示
    '''

    @tornado.web.authenticated
    def get(self):
        posts = self.orm.get_posts_for(self.current_user)
        self.render('index.html', posts=posts)


class ExploreHandler(BaseHandler):
    '''
    最近上传的图片页面
    '''

    def get(self):
        posts = self.orm.get_all_posts()
        self.render('explore.html', posts=posts)


class PostHandler(BaseHandler):
    '''
    单个图片详情页面
    '''

    def get(self, post_id):
        post = self.orm.get_post(post_id)
        user = post.user
        if not post:
            self.write("id错误")
        else:
            self.render('post.html', post=post, user=user)


class ProfileHandler(BaseHandler):
    '''
    用户档案页面
    '''

    @tornado.web.authenticated
    def get(self):
        user = self.orm.get_user(self.current_user)
        self.render('profile.html', user=user,like_posts=[])


class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self):
        pics = self.request.files.get('picture', [])  # 没有的话给一个空列表
        # 设置id，默认为1
        post_id = 1
        for p in pics:
            up_img = UploadImage(p['filename'], self.settings['static_path'])
            up_img.save_upload(p['body'])
            up_img.make_thumb()
            post_id = self.orm.add_post(up_img.image_url, up_img.thumb_url, self.current_user)
        self.redirect('/post/{}'.format(post_id))
