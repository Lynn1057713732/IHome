# -*- coding:utf-8 -*-

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
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


app = Flask(__name__)

# 加载配置
app.config.from_object(Config)
# 创建连接到MYSQL数据库的对象
db = SQLAlchemy(app)
# 创建连接到redis数据库的对象
redis_store = redis.StrictRedis(host=Config.REDIS_IP, port=Config.REDIS_PORT,)
# 开启csrf保护
CSRFProtect(app)

# 创建脚本管理器对象
manager = Manager(app)
# app和db在迁移时建立关联
Migrate(app, db)
# 将数据库迁移脚本添加到脚本管理器
manager.add_command('db', MigrateCommand)


@app.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis数据库
    redis_store.set('name', 'sz07')
    return 'index'


if __name__ == '__main__':
    manager.run()