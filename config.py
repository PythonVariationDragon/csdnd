# coding:utf8

import os
# 获取当前文件所在目录的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

# 配置的基类
class Config:
    '''设置密钥，确保不被跨站请求伪造攻击'''
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass
    # 虽然什么都没做，但仍然定义，好处在于衍生类当中可以继承并重写

    SQLALCHEMY_DATABASE_URI = 'mysql://root:abc123@localhost/CSDN'

