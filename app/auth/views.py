# coding:utf8

from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required
from flask_login import current_user # 当前用户
from . import auth
from .forms import LoginForm,RegisterForm,ChangePasswordForm
from ..models import User
from .. import db # 实际上是 from ..__init__ import db
# from ..decorators import admin_required,permission_required

@auth.route('/login/',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 在数据库中查找该邮箱的用户
        user = User.query.filter_by(username=form.username.data).first()
        # 如果数据库中存在该用户，且表单中填写的密码验证通过
        if user is not None and user.verify_password(form.password.data):
            # 使用login_user来登录用户
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid email or password')
    return render_template('auth/login.html',form=form)

@auth.route('/logout/')
@login_required # 表示必须在已经登录的情况下才能访问这个路由
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

# 注册路由
@auth.route('/register/',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/change-password/',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # 首先看旧密码是否输入正确
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            # 这里的add是修改现有用户
            db.session.add(current_user)
            flash('your password has been updated')
            return redirect(url_for('main.index'))
        else:
            # 如果旧密码输错，则提示信息
            flash('invalid password')
    return render_template('auth/change_password.html',form=form)
