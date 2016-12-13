# -*- coding: utf-8 -*-
from flask import jsonify, g, request, current_app, url_for
from ..models import Blog
from . import api
from .errors import bad_request, forbidden
from .. import db
from app.exceptions import ParsingError


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
    if not request.json:
        return bad_request("No JSON found")
    body = request.json.get('body')
    draft = request.json.get('draft')
    if body is None or body == '':
        return bad_request('blog does not have a body')
    if draft is None or draft == '':
        return bad_request('blog does not have a draft value')
    if draft == 'true':
        draft = True
    draft = False
    try:
        blog = Blog(body=body, draft=draft, author_id=g.current_user.id)
        db.session.add(blog)
        db.session.commit()
        return jsonify(blog.to_json()), 201, \
            {'Location': url_for(
                'api.get_blog', blog_id=blog.id, _external=True, _scheme='https')}
    except Exception:
        return bad_request('There is something wrong in your format. Committing abolished.')


# 更新文章端点
@api.route('/blogs/<int:blog_id>', methods=['PUT'])
def edit_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog:
        if blog.author_id == g.current_user.id:
            try:
                blog.body = request.json.get('body')
                blog.draft = False
                if request.json.get('draft') == 'true':
                    blog.draft = True
                db.session.add(blog)
                db.session.commit()
                return jsonify(blog.to_json())
            except Exception:
                return bad_request('There is something wrong in your format. Committing abolished.')
        return forbidden('Insufficient permissions')
    return bad_request('Blog not found')
