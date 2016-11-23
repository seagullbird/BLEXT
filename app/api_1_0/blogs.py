from flask import jsonify, g, request, current_app, url_for
from ..models import Blog, Category, Tag
from . import api
from .errors import bad_request
from .. import db


# 当前用户的所有文章端点
@api.route('/blogs/')
def get_blogs():
    # 添加分页
    page = request.args.get('page', 1, type=int)
    # 每页显示的博客数保存在配置里
    pagination = g.current_user.blogs.filter_by(author_id=g.current_user.id).order_by(Blog.timestamp.desc()).paginate(
        page, per_page=current_app.config['API_BLOGS_PER_PAGE'], error_out=False)
    blogs = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_blogs', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_blogs', page=page + 1, _external=True)
    return jsonify({
        'blogs': [blog.to_json() for blog in blogs],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


# id为blog_id的文章端点
@api.route('/blogs/<int:blog_id>')
def get_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return jsonify(blog.to_json())


# id为blog_id的文章的类别名端点
@api.route('/category/<int:blog_id>')
def get_blog_category(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog:
        categories = blog.category
        return jsonify(categories.to_json())
    return bad_request('Blog not found')


# id为blog_id的文章的标签名列表端点
@api.route('/tags/<int:blog_id>')
def get_blog_tags(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog:
        tags = blog.tags
        return jsonify({'tags': [tag.to_json() for tag in tags]})
    return bad_request('Blog not found')


# 发布新文章端点
@api.route('/blogs/', methods=['POST'])
def new_blog():
    blog = Blog.from_json(request.json)
    blog.author = g.current_user
    # 获得分类名（str类型）
    category_name = request.json.get('category')
    # 获得 Category 对象
    category = Category.generate_category(category_name, g.current_user.id)
    # 获得标签名（保存在list里）
    tag_names = request.json.get('tags').split(',')
    # 获得标签对象列表
    tags = Tag.generate_tags(tag_names, g.current_user.id)
    blog.category = category
    blog.tags = tags
    db.session.add(blog)
    db.session.commit()
    return jsonify(blog.to_json()), 201, \
        {'Location': url_for('api.get_blog', blog_id=blog.id, _external=True)}
