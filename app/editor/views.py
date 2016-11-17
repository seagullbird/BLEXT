from . import editor
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from .. import db
from ..models import Blog, Category, Tag
import mistune


@editor.route('/', methods=['GET', 'POST'])
def index():
    # 如果是 POST 请求，说明用户提交了一篇新文章
    # 接下来是通过 POST 的表单中的数据在数据库中创建新文章
    if request.method == 'POST':
        # 初始化markdown解析器
        markdown = mistune.Markdown()
        # 获得作者
        author = current_user._get_current_object()
        # 获得标题
        title = request.form.get('title', 'Title unset')
        # 获得摘要（纯文本）
        summary_text = request.form.get('summary', 'Summary unset')
        # 获得摘要（富文本）
        summary = markdown(summary_text)
        # 获得纯文本正文
        blog_text = request.form.get('plainText', '')
        # 获得富文本正文
        # 利用markdown解析器将markdown转换为html
        blog_html = markdown(blog_text)
        # 草稿
        draft = True
        if request.form.get('draft') == 'false':
            draft = False

        # 获得分类名并通过其查询数据库
        category_name = request.form.get('category', 'Category unset')
        category = Category.query.filter_by(
            name=category_name, author_id=author.id).first()
        # 如果当前用户名下不存在这个分类则新建：
        if not category:
            category = Category(name=category_name, author=author)

        # 获得标签名（保存在list里）
        tag_names = request.form.get('tags', '').split(',')
        tags = []
        # 处理文章标签
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:
                # 在用户名下查询标签名
                tag = Tag.query.filter_by(
                    name=tag_name, author_id=author.id).first()
                # 如果不存在则新建并添加
                if not tag:
                    tag = Tag(name=tag_name, author=author)
                    # 添加进数据库
                    db.session.add(tag)
                tags.append(tag)

        # 创建新文章并添加进数据库
        new_blog = Blog(title=title, summary=summary, summary_text=summary_text, category=category, body=blog_text,
                        html=blog_html, author=author, draft=draft)
        # 建立新文章及其标签的对应关系
        for tag in tags:
            new_blog.tags.append(tag)
        db.session.add(new_blog)

        if not draft:
            flash('Your blog is successfully uploaded!')
        else:
            flash('Your blog is successfully saved as a draft.')
        # 重定向到编辑页
        return redirect(url_for('editor.index'))
    if session.get('blog_id'):
        blog = Blog.query.filter_by(id=session['blog_id']).first()
        if blog:
            del session['blog_id']
            tags = ','.join([tag.name for tag in blog.tags])
            return render_template('editor/index.html', title=blog.title, category=blog.category.name, tags=tags, summary_text=blog.summary_text, text=blog.body)
    return render_template('editor/index.html')


@editor.route('/edit/<int:blog_id>')
def edit(blog_id):
    session['blog_id'] = blog_id
    return redirect(url_for('editor.index'))
