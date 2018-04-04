# -*- coding:utf-8 -*-
# 实现注册和登录


from . import api
from flask import request, jsonify, current_app,session
import re
from IHome.utils.response_code import RET
from IHome import redis_store, db
from IHome.models import User


@api.route('/sessions', methods=['POST'])
def login():
    """实现登录"""

    # 1.接受请求参数：手机号，密码明文密码
    json_dict = request.json
    mobile = json_dict.get('mobile')
    password = json_dict.get('password')
    current_app.logger.debug(mobile)
    # 2.判断参数的完整性
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="缺少参数")
    # 对手机号码进行校验
    if not re.match(r'^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg=u'手机号码格式错误')
    # 3.使用手机号查询要登录用户的模型数据
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询用户数据库失败 ")
    # 用户查询出来为None,那么不会返回错误，但是实际中需要判断
    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户名或密码错误")
    # 4.对密码进行校验
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg="用户名或密码错误")
    # 5.将用户的校验信息写入session
    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile
    # 6.响应登录结果
    return jsonify(errno=RET.OK, errmsg="登陆成功")



@api.route('/users', methods=['POST'])
def register():
    """实现注册
    1.获取请求参数：手机号，短信验证码，密码
    2.判断参数是否缺少
    3.获取服务器的短信验证码
    4.并与客户端传入的验证码比较,如果一致
    5.创建User模型类对象
    6.保存注册数据到数据库
    7.响应结果
    """

    # 1.获取请求参数：手机号，短信验证码，密码
    # json_str = request.data
    # json_dict = json.loads(json_str)
    # json_dict = request.get_json()
    json_dict = request.json

    mobile = json_dict.get('mobile')
    sms_code_client = json_dict.get('sms_code')
    password = json_dict.get('password')

    # 2.判断参数是否缺少
    if not all([mobile, sms_code_client, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 3.获取服务器的短信验证码
    try:
        sms_code_server = redis_store.get('Mobile:' + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询短信验证码失败')
    # 判断数据是否为空
    if not sms_code_server:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码不存在')

    # 4.并与客户端传入的验证码比较,如果一致
    if sms_code_server != sms_code_client:
        return jsonify(errno=RET.DATAERR, errmsg='输入验证码有误')

    # 5.创建User模型类对象
    user = User()
    # 注册时，默认手机号就是用户名，如果后面需要更换用户名，也是提供的有接口和界面
    user.name = mobile
    user.mobile = mobile
    # 密码需要加密后才能存储
    # user.password_hash = '加密后的密码'
    user.password = password

    # 6.保存注册数据到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存注册数据失败')

    # 7.响应结果
    return jsonify(errno=RET.OK, errmsg='注册成功')

