# -*- coding:utf-8 -*-
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from config import configs
# 创建一个可以被外界导入的数据库连接对象，不传参数SQLAlchemy，不会调用init_app(app)，
# 就没有db对象，在自己用到时自己调用init_app(app)，创建db对象
db = SQLAlchemy()
# 创建可以被外界导入的连接到redis数据库的对象
redis_store = None


def get_app(config_name):
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

    return app