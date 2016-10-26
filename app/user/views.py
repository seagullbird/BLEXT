from . import user
from flask import render_template
from flask_login import current_user
from ..models import Blog


@user.route('/<username>')
def index(username):
    # 获得用户所有文章（按时间戳顺序）
    blogs = current_user.blogs.order_by(Blog.timestamp.desc()).all()
    return render_template('user/index.html', blogs=blogs)
