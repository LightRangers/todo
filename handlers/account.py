from .main import BaseHandler
from utils.account import authenticate, register


class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')

        if username and password1 and (password1 == password2):
            register(username, password1)
            self.write('注册成功')
        else:
            self.write('两次密码不一致')


class LoginHandler(BaseHandler):
    def get(self):
        msg = self.get_argument('msg', '')
        next_url = self.get_argument('next', '')
        self.render('login.html', next_url=next_url, msg=msg)

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        next_url = self.get_argument('next', '')
        if not username.strip() or not password.strip():
            self.redirect('/login?msg=用户或密码为空')
        else:
            if authenticate(username, password):
                self.session.set('todo_user', username)
                if next_url:
                    self.redirect(next_url)
                else:
                    self.redirect('/')
            else:
                self.redirect('/login?msg=密码错误')


class LogoutHandler(BaseHandler):
    def get(self):
        self.session.delete('todo_user')
        self.render('logout.html')
