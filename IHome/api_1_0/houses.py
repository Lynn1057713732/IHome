# -*- coding:utf-8 -*-
# 用户房屋模块接口

from . import api
from flask import current_app, jsonify
from IHome.utils.response_code import RET
from IHome.models import Area


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


