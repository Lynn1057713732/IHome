# -*- coding:utf-8 -*-
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from config import Config

app = Flask(__name__)

# 加载配置
app.config.from_object(Config)
# 创建连接到MYSQL数据库的对象
db = SQLAlchemy(app)
# 创建连接到redis数据库的对象
redis_store = redis.StrictRedis(host=Config.REDIS_IP, port=Config.REDIS_PORT,)
# 开启csrf保护
CSRFProtect(app)
# 使用session在flask中的拓展
Session(app)