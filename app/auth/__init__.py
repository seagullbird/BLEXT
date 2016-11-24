from flask import Blueprint
# 创建蓝本
auth = Blueprint('auth', __name__)
from . import views
