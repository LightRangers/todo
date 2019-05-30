import uuid

from pycket.session import SessionMixin

import tornado.websocket
import tornado.web
import tornado.escape

from .main import BaseHandler


class RoomHandler(BaseHandler):
    """
    聊天室页面
    """

    @tornado.web.authenticated
    def get(self):
        m = {
            'id': 41342,
            'username': self.current_user,
            'body': 'hello 36 class'
        }

        msgs = [
            {
                'html': self.render_string('message.html', chat=m)
            }
        ]
        self.render('room.html', messages=msgs)


class ChatWSHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    """
    处理和响应  连接
    """
    waiters = set()  # 等待接受信息的用户

    def get_current_user(self):
        return self.session.get('todo_user', None)

    def open(self, *args, **kwargs):
        """ 新的连接打开，自动调用"""
        print("new ws connecttion: {}".format(self))
        ChatWSHandler.waiters.add(self)

    def on_close(self):
        """ 连接断开，自动调用 """
        print("close ws connection: {}".format(self))
        ChatWSHandler.waiters.remove(self)

    def on_message(self, message):
        """ 服务端接收到消息自动调用 """
        print("got message: {}".format(message))
        parsed = tornado.escape.json_decode(message)
        msg = parsed['body']
        chat = {
            'id': str(uuid.uuid4()),
            'body': msg,
            'username': self.current_user
        }

        chat['html'] = tornado.escape.to_basestring(self.render_string('message.html', chat=chat))

        for w in ChatWSHandler.waiters:
            w.write_message(chat)


class EchoWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
