import tornado.web
from PIL import Image
from pycket.session import SessionMixin
from utils.account import add_post


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('todo_user', None)


class IndexHnadeler(tornado.web.RequestHandler):
    '''
    首页，用户上传图片的展示
    '''

    def get(self):
        self.render('index.html')


class ExploreHandler(tornado.web.RequestHandler):
    '''
    最近上传的图片页面
    '''

    def get(self):
        self.render('explore.html')


class PostHandler(tornado.web.RequestHandler):
    '''
    单个图片详情页面
    '''

    def get(self, post_id):
        self.render('post.html', post_id=post_id)


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
            save_path = 'static/upload/{}'.format(p['filename'])
            with open(save_path, 'wb') as f:
                f.write(p['body'])
            post_id = add_post('upload/{}'.format(p['filename']), self.current_user)
            # 生成缩略图
            im = Image.open(save_path)
            im.thumbnail((200, 200))
            im.save('static/upload/thumb_{}.jpg'.format(p['filename']), 'JPEG')

        self.redirect('/post/{}'.format(post_id))
