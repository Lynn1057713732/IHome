# -*- coding:utf-8 -*-
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from config import configs
import logging
from logging.handlers import RotatingFileHandler


from IHome.utils.common import RegexConverter
# 创建一个可以被外界导入的数据库连接对象，不传参数SQLAlchemy，不会调用init_app(app)，
# 就没有db对象，在自己用到时自己调用init_app(app)，创建db对象
db = SQLAlchemy()
# 创建可以被外界导入的连接到redis数据库的对象
redis_store = None


def setupLogging(level):
    """
    如果是开发模式，'development' -> 'DEBUG'
    如果是生产模式， 'production' -> 'WARN'
    :param level: 传入就生产不同模式的log
    :return:
    """
    # 设置日志的记录等级
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def get_app(config_name):
    """工厂方法：根据不同的配置信息，实例化出不同的app"""

    # 调用封装的日志
    setupLogging(configs[config_name].LOGGIONG_LEVEL)
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(configs[config_name])
    # 创建连接到MYSQL数据库的对象
    # db = SQLAlchemy(app)
    db.init_app(app)
    # 创建连接到redis数据库的对象
    global redis_store
    redis_store = redis.StrictRedis(host=configs[config_name].REDIS_IP, port=configs[config_name].REDIS_PORT,)
    # 开启csrf保护
    CSRFProtect(app)
    # 使用session在flask中的拓展
    Session(app)

    # 需要现有路由转换器，后面你的html_blue才能直接正则匹配
    app.url_map.converters['re'] = RegexConverter

    # 注册蓝图：为了解决导入api时，还没有redis_store，造成的ImportError: cannot import name redis_store
    from IHome.api_1_0 import api
    app.register_blueprint(api)
    # 注册静态html文件加载时的蓝图
    from IHome.web_html import html_bule
    app.register_blueprint(html_bule)

    return app