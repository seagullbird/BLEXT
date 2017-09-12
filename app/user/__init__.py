# -*- coding: utf-8 -*-
from flask import Blueprint
# 创建蓝本
user = Blueprint('user', __name__)
from . import views
