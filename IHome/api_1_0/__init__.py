# -*- coding:utf-8 -*-
from flask import Blueprint
# url_prefix代表url默认前缀，可进入源代码看，使注册的api蓝图都以/api/1.0开始
api = Blueprint('api_1_0', __name__, url_prefix='/api/1.0')

# 为了让api导入到蓝图时，蓝图注册路由的代码可以跟着被导入，那么我们的路由和视图对应的关系就会有路由
from . import  verify