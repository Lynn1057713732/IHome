# -*- coding:utf-8 -*-
# 用户中心


from . import api
from flask import request, session, current_app, jsonify
from IHome.models import User
from IHome.utils.response_code import RET


@api.route('/users')
def get_user():
    """提供用户个人信息"""
    # 0.判断用户是否登录
    # 1.获取用户id (user_id),通过session
    user_id = session.get('user_id')


    # 2.查询该登录用户的user信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 3.构造响应数据
    response_data = user.to_dict()
    #current_app.logger.debug(response_data['name'])

    # 4.响应数据
    return jsonify(errno=RET.OK, errmsg='OK', data=response_data)