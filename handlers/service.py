import requests
from .main import BaseHandler
from utils.photo import UploadImage

from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from .chat import ChatWSHandler, make_data


class SyncSaveHandler(BaseHandler):
    def get(self):
        save_url = self.get_argument('save_url', '')
        print(save_url)
        resp = requests.get(save_url)
        up_img = UploadImage('x.jpg', self.settings['static_path'])
        up_img.save_upload(resp.content)
        up_img.make_thumb()
        post_id = self.orm.add_post(up_img.image_url, up_img.thumb_url, self.current_user)
        self.redirect('/post/{}'.format(post_id))


class AsyncSaveHandler(BaseHandler):
    @coroutine
    def get(self):
        save_url = self.get_argument('save_url', '')
        username = self.get_argument('name', '')
        print(save_url)
        client = AsyncHTTPClient()
        resp = yield client.fetch(save_url)

        up_img = UploadImage('x.jpg', self.settings['static_path'])
        up_img.save_upload(resp.body)
        up_img.make_thumb()
        post_id = self.orm.add_post(up_img.image_url, up_img.thumb_url, username)
        # self.redirect('/post/{}'.format(post_id))
        msg = 'user {} post: http://127.0.0.1:8000/post/{}'.format(username, post_id)
        chat = make_data(self, msg, img_url=up_img.thumb_url, post_id=post_id)
        ChatWSHandler.send_updates(chat)
