from flask import jsonify
from ..models import Blog
from . import api


@api.route('/blogs/')
def get_blogs():
    blogs = Blog.query.all()
    return jsonify({'blogs': [blog.to_json() for blog in blogs]})


@api.route('/blogs/<int:blog_id>')
def get_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return jsonify(blog.to_json())
