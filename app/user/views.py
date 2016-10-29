from . import user
from flask import render_template, current_app, request, redirect, url_for
from flask_login import current_user, login_required
from ..models import Blog, User
from .. import db


# 用户主页路由
@user.route('/<username>')
def index(username):
    # 查找博客主人
    host_user = User.query.filter_by(username=username).first()
    # 添加分页
    page = request.args.get('page', 1, type=int)
    # 每页显示的博客数保存在配置里
    pagination = Blog.query.filter_by(author_id=host_user.id).order_by(Blog.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'], error_out=False)
    # 获得用户所有文章（按时间戳顺序）
    blogs = pagination.items
    return render_template('user/index.html', blogs=blogs, pagination=pagination, host_user=host_user)


# 用户文章路由
@user.route('/<username>/<blog_id>')
def blog_page(username, blog_id):
    # 利用blog_id从数据库读到blog对象并返回给模版
    # 如果不是作者本人访问：
    if not current_user.is_authenticated or current_user.username != username:
        host_user = User.query.filter_by(username=username).first()
        blog = host_user.blogs.filter_by(id=blog_id).first()
    else:
        blog = current_user.blogs.filter_by(id=blog_id).first()
    return render_template('user/blog_page.html', blog=blog)


# 删除用户文章（需要登录才能访问）
@login_required
@user.route('/delete/<blog_id>')
def delete_blog(blog_id):
    # 通过博客id查询到博客对象
    blog = Blog.query.filter_by(id=blog_id).first()
    # 判断是否博主本人操作
    if blog and current_user.id == blog.author_id:
        db.session.delete(blog)
    return redirect(url_for('user.index', username=current_user.username))


# 用户 About Me 页面
@user.route('/<username>/about_me')
def about_me(username):
    host_user = User.query.filter_by(username=username).first()
    about_me = ''
    if host_user and host_user.about_me:
        about_me = host_user.about_me
    return render_template('user/about_me.html', about_me=about_me)
