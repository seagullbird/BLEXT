# -*- coding: utf-8 -*-
from flask import Blueprint
# 创建蓝本
api = Blueprint('api', __name__)
from . import auth, blogs, users, errors
