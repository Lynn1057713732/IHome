# -*- coding:utf-8 -*-
# 用户房屋模块接口

from . import api
from flask import current_app, jsonify, request, g, session
from IHome.utils.response_code import RET
from IHome.models import Area, House, Facility
from IHome import db, constants, redis_store
from IHome.utils.common import login_required


@api.route('/houses', methods=['POST'])
@login_required
def pub_house():
    """发布新房源
    0.校验用户是否登录
    1.接受参数
    2.校验参数
    3.实例化房屋模型对象，给对象赋值属性
    4.保存到数据库
    5，返回响应信息
    """
    # 1.接受所有参数
    json_dict = request.json

    title = json_dict.get('title')
    price = json_dict.get('price')
    address = json_dict.get('address')
    area_id = json_dict.get('area_id')
    room_count = json_dict.get('room_count')
    acreage = json_dict.get('acreage')
    unit = json_dict.get('unit')
    capacity = json_dict.get('capacity')
    beds = json_dict.get('beds')
    deposit = json_dict.get('deposit')
    min_days = json_dict.get('min_days')
    max_days = json_dict.get('max_days')

    # 2.校验参数：注意price / deposit， 需要用户传入数字
    # 判断参数是否缺失
    if not all([title, price, address, area_id, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数缺失")
    # 提示：在开发中，对于像价格这样的浮点数，不要直接保存浮点数，因为有精度的问题，一般以分为单
    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数格式错误")

    # 3.实例化房屋模型对象，并给房屋属性赋值
    house = House()
    house.user_id = g.user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    # 处理房屋的设施，保存设置的表示数字
    facilities = json_dict.get('facility')
    # 查询出被选中的设置模型对象，赋值给房子的模型属性
    house.facilities = Facility.query.filter(Facility.id.in_(facilities)).all()
    # 4.保存到数据库
    # try:
    #     db.session.add(house)
    #     db.session.commit()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     db.session.rollback()
    #     return jsonify(errno=RET.DBERR, errmsg="发布新房源失败")
    # 5.响应结果
    return jsonify(errno=RET.OK, errmsg="发布新房源成功", data={'house_id':house.id})


@api.route('/areas')
def get_areas():
    """提供城区信息,在需要显示城区信息时调用该接口
    1.查询所有城区信息
    2.构造响应信息
    3.响应结果
    """
    # 1.查询所有城区信息,如果为空，就不显示任何信息。
    # areas返回的数据时模型对象列表[area1,area2,area3...]
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询城区数据失败")
    # 2.构造响应信息
    # 将每一个area模型对象转成字典信息存在一个列表中
    area_dict_list = []
    for area in areas:
        area_dict_list.append(area.to_dict())
    # 3.响应结果
    return jsonify(errno=RET.OK, errmsg="NOT OK", data=area_dict_list)


