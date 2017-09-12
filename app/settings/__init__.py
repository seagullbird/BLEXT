# -*- coding: utf-8 -*-
from flask import Blueprint
# 创建蓝本
settings = Blueprint('settings', __name__)
from . import views
