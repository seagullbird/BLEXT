# -*- coding: utf-8 -*-
from flask import Blueprint
# 创建蓝本
editor = Blueprint('editor', __name__)

from . import views
