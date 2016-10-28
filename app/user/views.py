from . import user
from flask import render_template, current_app, request
from flask_login import current_user
from ..models import Blog

# 用户主页路由


@user.route('/<username>')
def index(username):
    # 添加分页
    page = request.args.get('page', 1, type=int)
    # 每页显示的博客数保存在配置里
    pagination = Blog.query.order_by(Blog.timestamp.desc()).paginate(page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'], error_out=False)
    # 获得用户所有文章（按时间戳顺序）
    blogs = pagination.items
    return render_template('user/index.html', blogs=blogs, pagination=pagination)


# 用户文章路由
@user.route('/<username>/<blog_id>')
def blog_page(username, blog_id):
    # 利用blog_id从数据库读到blog对象并返回给模版
    blog = current_user.blogs.filter_by(id=blog_id).first()
    return render_template('user/blog_page.html', blog=blog)
