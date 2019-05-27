import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from handlers.main import IndexHnadeler, ExploreHandler, PostHandler,UploadHandler
from handlers.account import RegisterHandler,LoginHandler

define('port', default='8000', help='listenting port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHnadeler),
            (r'/explore', ExploreHandler),
            (r'/signup', RegisterHandler),
            (r'/upload', UploadHandler),
            (r'/login', LoginHandler),
            (r'/post/(?P<post_id>[0-9]+)', PostHandler),
        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='statics',
            cookie_secret='asdasdsfecfvgweff',  # 加密cookie的内容
            login_url='/login',  # 设置装饰器@tornado.web.authenticated重定向的url
            # xsrf_cookies=True,  # 设置每次post提交附带xsrf信息
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    # 'password': '',
                    'db_sessions': 5,  # redis db index
                    # 'db_notifications': 11,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': 30,
                },
            }
        )
        super().__init__(handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port)
    print('Server start on port {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()
