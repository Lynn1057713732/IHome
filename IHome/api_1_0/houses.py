# -*- coding:utf-8 -*-
# 用户房屋模块接口

from . import api
from flask import current_app, jsonify, request, g, session
from IHome.utils.response_code import RET
from IHome.models import Area, House, Facility, HouseImage
from IHome import db, constants, redis_store
from IHome.utils.common import login_required
from IHome.utils.image_storage import upload_image


@api.route('/houses/index')
def get_house_index():
    """首页房屋推荐信息
    1.查询最新发布的五个房源信息
    2.构造响应数据
    3.响应结果
    """
    # 1.查询最新发布的五个房屋信息 houses == [House, House, House, ...],查询出来的是模型对象
    try:
        houses = House.query.order_by(House.create_time.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询房源数据失败")
    # 2.构造响应数据
    house_dict_list = []
    for house in houses:
        house_dict_list.append(house.to_basic_dict())

        # 3.响应结果
    return jsonify(errno=RET.OK, errmsg='OK', data=house_dict_list)


@api.route('/houses/detail/<int:house_id>')
def get_house_detail(house_id):
    """房源详细信息
    0.获取house_id,通过正则。如果house_id不满足条件不会进入到使用当中
    1.查询房屋全部信息
    2.构造响应数据
    3.响应结果
    """
    # 1.查询房屋全部信息
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询房屋数据失败')
    if not house:
        return jsonify(errno=RET.NODATA, errmsg='房屋不存在')

    # 2.构造响应数据
    response_data = house.to_full_dict()

    # 获取user_id : 当用户登录后访问detail.html，就会有user_id，反之，没有user_id
    login_user_id = session.get('user_id', -1)

    # 3.响应结果
    return jsonify(errno=RET.OK, errmsg='OK', data={'house': response_data, 'login_user_id': login_user_id})


@api.route('/houses/image', methods=['POST'])
@login_required
def upload_house_image():
    """发布房屋图片
    0.判断用户是否登录
    1.接受参数：house_id,image_data
    2.校验参数
    3.查询house模型对象数据，没有数据就不用上传
    4.调用上传图片的方法，上传图片到七牛云
    5.将图片上的七牛云key，保存到数据库
    6.响应结果：上传的房屋图片，需要立即刷新出来
    """
    # 1.接受参数：house_id,image_data，校验参数
    try:
        image_data = request.files.get('house_image')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="无法收到房屋图片")
    try:
        house_id = request.form.get('house_id')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="缺少必要参数")
    # 3.查询house模型对象数据，没有数据就不用上传
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询房屋数据失败")
    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")
    # 4.调用上传图片的方法，上传图片到七牛云
    try:
        key = upload_image(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传房屋图片失败')

    # 5.将图片上的七牛云key，保存到数据库
    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = key

    # 选择一个图片，作为房屋的默认图片
    if not house.index_image_url:
        house.index_image_url = key
    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='存储房屋图片失败')

    # 6.响应结果：上传的房屋图片，需要立即刷新出来
    image_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg='发布房屋图片成功', data={'image_url': image_url})


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
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="发布新房源失败")
    # 5.响应结果
    return jsonify(errno=RET.OK, errmsg="发布新房源成功", data={'house_id':house.id})


@api.route('/areas')
def get_areas():
    """提供城区信息,在需要显示城区信息时调用该接口
    1.查询所有城区信息
    2.构造响应信息
    3.响应结果
    """
    # 查询缓存数据，如果有缓存数据，就使用缓存数据，反之，就查询，并缓存新查询的数据
    try:
        area_dict_list = redis_store.get('Areas')
        if area_dict_list:
            return jsonify(errno=RET.OK, errmsg='OK', data=eval(area_dict_list))
    except Exception as e:
        current_app.logger.error(e)

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

    # 缓存城区信息到redis : 没有缓存成功也没有影响，因为前面会判断和查询
    try:
        redis_store.set('Areas', area_dict_list, constants.AREA_INFO_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)


    # 3.响应结果
    return jsonify(errno=RET.OK, errmsg="NOT OK", data=area_dict_list)


