# coding:utf8

from . import main
from flask import redirect

@main.route('/')
def index():
    return redirect('/admin/')


