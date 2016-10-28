from . import editor
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from .. import db
from ..models import Blog
from .blog_parser import BlogParser


@editor.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 允许的文件格式
        ALLOWED_EXTENSIONS = ['md']

        # 判断文件类型方法
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

        # 从 request 中读取文件
        file = request.files['file']
        # 如果文件满足需要的类型：
        if file and allowed_file(file.filename):
            # 取得文件内容（以str形式）
            blog = file.stream.read().decode('utf-8')
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
