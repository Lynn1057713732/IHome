# -*- coding:utf-8 -*-
import redis


class Config(object):
    """加载配置"""

    # 配置秘钥
    SECRET_KEY = 'kg+A4s8wm9pIZkVPaEK28hA7X/SMyICHsY0QdSSZmwvNKCBW4y56r8vHXsYKs6/B'
    # 开启调试模式
    DEBUG = True
    # 配置MySQL数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1057713732@127.0.0.1:3306/ihome_debug'
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


class DevelopmentConfig(Config):
    """创建调试环境下的配置类"""
    # 我们的爱家租房的房型，调试模式的配置和Config一致，所以pass
    pass


class ProductionConfig(Config):
    """创建线上环境下的配置类"""

    # 重写有差异性的配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.72.77:3306/ihome'


class UnittestConfig(Config):
    """单元测试的配置"""

    # 重写有差异性的配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome_test'


# 准备工厂设计模式的原材料
configs = {
    'default_config': Config,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'unittest': UnittestConfig
}