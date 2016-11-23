from flask import jsonify, g
from . import api

# 已登录用户只能获得自己的个人账户信息


# 用户个人信息端点
@api.route('/user/')
def get_user():
    return jsonify(g.current_user.to_json())


# 用户所有分类端点
@api.route('/categories')
def get_user_categories():
    categories = g.current_user.categories
    return jsonify({'categories': [category.to_json() for category in categories]})


# 用户所有标签端点
@api.route('/tags')
def get_user_tags():
    tags = g.current_user.tags
    return jsonify({'tags': [tag.to_json() for tag in tags]})
