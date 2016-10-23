from flask import Blueprint
from . import views, errors
# 创建蓝本
main = Blueprint('main', __name__)
