# -*- coding:utf-8 -*-

from IHome.api_1_0 import api


@api.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis数据库
    # 只有在get_app之后才会对redis_store进行对象的初始化，在之前redis_store都是none，最好在哪里使用哪里导入
    from IHome import redis_store
    redis_store.set('name', '12345')
    # 测试session：flask自带的session模块,用于存储session
    # from flask import session
    # session['name'] = 'hey python'
    # 测试redis数据库
    # redis_store.set('name', 'sz07')
    return 'index'