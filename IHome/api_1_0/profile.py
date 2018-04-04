# -*- coding:utf-8 -*-
# 用户中心


from . import api
from flask import request, session, current_app, jsonify
from IHome.models import User
from IHome.utils.response_code import RET
from IHome.utils.image_storage import upload_image
from IHome import db, constants


@api.route('/users/avatar', methods=['POST'])
def upload_avatar():
    """提供用户头像上传
    0.先判断用户是否登录 @login_required
    1.接受请求参数:avatar对应的图片数据，并校验
    2.调用上传图片的工具方法
    3.存储图片的key到user.avatar_url属性中
    4.响应上传结果，在结果中传入avatar_url，方便用户上传完成后立即刷新头像
    """

    # 1.接受请求参数:avatar对应的图片数据，并校验
    try:
        image_data = request.files.get('avatar')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='头像参数错误')

    # 2.调用上传图片的工具方法
    try:
        key = upload_image(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传头像失败')

    # 3.存储图片的key到user.avatar_url属性中
    # 获取登录用户的user_id
    user_id = session.get('user_id')


    # 查询登录用户对象
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')
    # 给登录用户模型属性赋新值
    user.avatar_url = key
    # 将新值保存的数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='存储用户头像地址失败')

    # 4.响应上传结果，在结果中传入avatar_url，方便用户上传完成后立即刷新头像
    # 拼接访问头像的全路径
    # http://oyucyko3w.bkt.clouddn.com/FtEAyyPRhUT8SU3f5DNPeejBjMV5
    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg='上传头像成功', data=avatar_url)


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