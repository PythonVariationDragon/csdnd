# coding:utf8

from . import db
from . import admin
from . import login_manager
from .main.forms import SearchByUsername,SearchByPassword,SearchByEmail

from flask import render_template,session
from flask_admin import BaseView,expose # BaseView自定义视图：搜索用户名
from flask_admin.contrib.sqla import ModelView # ModelView是对数据库可视化：Account
from flask_login import UserMixin,current_user

from werkzeug.security import generate_password_hash,check_password_hash

# 新建一个数据表
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    email = db.Column(db.String(64), unique=True)
    # 设置密码列，用于保存密码的散列值
    password_hash = db.Column(db.String(128))

    # 使用property装饰器，把密码变成私有财产，不允许访问
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 使用password.setter装饰器，允许写入密码
    @password.setter
    def password(self, pw):
        self.password_hash = generate_password_hash(pw)  # 输入是原密码，输出是加密后的密码散列值

    # 验证用户填写的密码是否正确
    def verify_password(self, pw):
        return check_password_hash(self.password_hash, pw)  # 输入是用户填写的密码已经本地存储的密码散列值，输出是验证结果

# Flask-login要求实现一个回调函数，通过user_id 加载用户
@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

# 使用现有数据表
# 两个一一对应：数据库表名和列名
class Account(db.Model):
    __tablename__ = 'CSDN'
    USERNAME = db.Column('USERNAME',db.String(64),primary_key = True)
    PASSWORD = db.Column('PASSWORD',db.String(64))
    EMAIL = db.Column('EMAIL',db.String(64))

    def __repr__(self):
        return '<User: %r>' %self.USERNAME

# admin.add_view(ModelView(Account,db.session))

# 数据库视图
class AccountView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        return False
    # can_create = False
    column_list = ['USERNAME','PASSWORD','EMAIL'] # 默认不显示主键，手动添加主键
    column_labels = {
        'USERNAME':u'用户名',
        'PASSWORD':u'密码',
        'EMAIL':u'邮箱'
    }
admin.add_view(AccountView(Account,db.session))


# 自定义视图
class SearchUsername(BaseView):
    edit_template='search2.html'
    @expose('/', methods=['GET', 'POST']) #相当于route('/')
    def index(self):
        form = SearchByUsername()
        if form.validate_on_submit():
            account = Account.query.filter_by(USERNAME=form.USERNAME.data).first()
            session['username'] = account.USERNAME
            session['password'] = account.PASSWORD
            session['email'] = account.EMAIL
        return render_template('search.html',
                               form=form,
                               username=session.get('username'),
                               password=session.get('password'),
                               email = session.get('email'))

admin.add_view(SearchUsername(name=u'搜索用户名'))