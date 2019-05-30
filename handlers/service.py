import requests
from .main import BaseHandler
from utils.photo import UploadImage


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
