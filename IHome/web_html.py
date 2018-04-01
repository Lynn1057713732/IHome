# -*- coding:utf-8 -*-

from flask import Blueprint, current_app


html_bule = Blueprint('html/blue', __name__)


@html_bule.route('/<re(".*"):file_name>')
def get_static_html(file_name):
    """获取静态文件"""
    # 需求1：http://127.0.0.1:5000/login.html
    # 需求2：http://127.0.0.1:5000/ 默认加载index.html
    # 需求3：http://127.0.0.1:5000/favicon.ico  加载title图标

    if not file_name:
        file_name = 'index.html'
    if file_name != 'favicon.ico':
        # 2.拼接file_name静态文件的路径
        file_name = 'html/' + file_name

    return current_app.send_static_file(file_name)