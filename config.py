# -*- coding:utf-8 -*-
import redis


class Config(object):
    """加载配置"""

    # 配置秘钥
    SECRET_KEY = 'kg+A4s8wm9pIZkVPaEK28hA7X/SMyICHsY0QdSSZmwvNKCBW4y56r8vHXsYKs6/B'
    # 开启调试模式
    DEBUG = True
    # 配置MySQL数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1057713732@127.0.0.1:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置Redis数据库
    REDIS_IP = '127.0.0.1'
    REDIS_PORT = 6379
    # 配置session数据存储在Redis数据库中
    SESSION_TYPE = 'redis'
    # 指定存储在session数据在Redis中的位置
    SESSION_REDIS = redis.StrictRedis(host=REDIS_IP, port=REDIS_PORT,)
    # 开启session数据的签名，让session数据不以明文形式存储
    SESSION_USE_SIGNER = True
    # 设置session的会话的超时时长
    PERMANENT_SESSION_LIFETIME = 3600 * 24
