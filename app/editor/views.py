from . import editor
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from .. import db
from ..models import Blog
from .blog_parser import BlogParser


@editor.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 取得文件内容（以str形式）
        blog = request.form.get('plainText', '')
        # 如果文件不为空：
        if blog:
            # 初始化BlogParser对象
            blog_parser = BlogParser(blog)
            # 获得标题
            title = blog_parser.get_title()
            # 获得摘要
            summary = blog_parser.get_summary()
            # 获得纯文本正文
            blog_text = blog_parser.get_blog_text()
            # 获得富文本正文
            blog_html = blog_parser.get_blog_html()

            # 创建新文章并添加进数据库
            new_blog = Blog(title=title, summary=summary, body=blog_text,
                            html=blog_html, author=current_user._get_current_object())
            db.session.add(new_blog)
            flash('Your blog is successfully uploaded!')
        # 重定向到编辑页
        return redirect(url_for('editor.index'))
    return render_template('editor/index.html')


@editor.route('/publish')
def publish():

    return redirect(url_for('main.index'))
