from . import user
from flask import render_template
from flask_login import current_user
from ..models import Blog


# 用户主页路由
@user.route('/<username>')
def index(username):
    # 获得用户所有文章（按时间戳顺序）
    blogs = current_user.blogs.order_by(Blog.timestamp.desc()).all()
    return render_template('user/index.html', blogs=blogs)


# 用户文章路由
@user.route('/<username>/<blog_id>')
def blog_page(username, blog_id):
    blog = current_user.blogs.filter_by(id=blog_id).first()
    return render_template('user/blog_page.html', blog=blog)
