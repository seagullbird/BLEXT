from flask import Blueprint
from . import views, errors
# 创建蓝本
user = Blueprint('user', __name__)
