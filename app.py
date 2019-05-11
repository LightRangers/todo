import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from handlers.main import IndexHnadeler, ExploreHandler, PostHandler

define('port', default='8000', help='listenting port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHnadeler),
            (r'/explore', ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', PostHandler),
        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
        )

        super().__init__(handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port)
    print('Server start on port {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()
