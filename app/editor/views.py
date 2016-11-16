from . import editor
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from .. import db
from ..models import Blog, Tag
import mistune


@editor.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获得标题
        title = request.form.get('title', 'Title unset')
        # 获得摘要
        summary = request.form.get('summary', 'Summary unset')
        # 获得分类
        category = request.form.get('category', 'Category unset')
        # 获得标签（保存为为list对象）
        tags = request.form.get('tags', '').split(',')
        # 获得纯文本正文
        blog_text = request.form.get('plainText', '')
        # 获得富文本正文
        # 初始化markdown解析器
        markdown = mistune.Markdown()
        # 利用markdown解析器将markdown转换为html
        blog_html = markdown(blog_text)
        # 草稿
        draft = True
        if request.form.get('draft') == 'false':
            draft = False

        # 创建新文章并添加进数据库
        new_blog = Blog(title=title, summary=summary, category=category, body=blog_text,
                        html=blog_html, author=current_user._get_current_object(), draft=draft)
        db.session.add(new_blog)
        # 必须先提交才能继续
        db.session.commit()

        # 处理文章标签
        for tag_name in tags:
            # 去掉首尾空格
            tag_name = tag_name.strip()
            # 查询标签名
            tag = Tag.query.filter_by(name=tag_name).first()
            # 如果存在
            if tag:
                tag.blog_id = new_blog.id
            # 否则新建
            else:
                tag = Tag(name=tag_name, blog_id=new_blog.id)
            # 添加进数据库
            db.session.add(tag)

        if not draft:
            flash('Your blog is successfully uploaded!')
        else:
            flash('Your blog is successfully saved as a draft.')
        # 重定向到编辑页
        return redirect(url_for('editor.index'))
    return render_template('editor/index.html')
