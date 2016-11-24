from flask import Blueprint
# 创建蓝本
main = Blueprint('main', __name__)
from . import views
