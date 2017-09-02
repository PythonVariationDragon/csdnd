# coding:utf8

from flask import Flask,session
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_admin import Admin

from config import Config

'''
    第1步：实例化所有的扩展
'''
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong' # 设置安全等级为强，监视IP代理和用户代理，一旦发现异动就退出登录
login_manager.login_view = 'auth.login' # 指定登录页面的端点，也就是auth蓝本里的视图函数login()
moment = Moment()
admin = Admin(name='CSDN',template_mode='bootstrap3')

'''
    第2步：创建工厂函数create_app
'''
# 唯一的参数config_name：开发、测试或生产环境。例如'development'
def create_app():
    app = Flask(__name__)

    # from_object就是从一个config类里面导入所有的配置项
    # 这个config类就是config[config_name]
    app.config.from_object(Config)
    Config.init_app(app) # 其实什么都没做

    # 初始化所有的扩展对象
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    admin.init_app(app)

    # 注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth
    app.register_blueprint(auth,url_prefix='/auth')

    return app