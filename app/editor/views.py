from . import editor
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from .. import db
from ..models import Blog
from ..exceptions import ParsingError

# 对于“用户重新编辑已存在文章后发布不会覆盖原文章而是产生新的一篇文章”问题的解决办法：
# 在编辑器页面中添加隐藏（hidden）标签 #blog_id，编辑器主页（下面的 index 函数）收到任何
# GET 请求后首先检查 session，如果 session中有 blog_id
# 值说明是从博文页面中的编辑按钮链接过来的；将 session 中的 blog_id 值保存在页面上的
# #blog_id 标签中并立即删除 session 中的值。用户点击发布按钮时，浏览器会将 #blog_id
# 的值随一并提交，通过表单中 blog_id 值判断该文是新建文章还是已有文章重编辑。


@editor.route('/', methods=['GET', 'POST'])
def index():
    # 如果是 POST 请求，说明用户提交了一篇新文章
    # 接下来是通过 POST 的表单中的数据在数据库中创建新文章
    if request.method == 'POST':
        success = False
        # 获得作者
        author = current_user._get_current_object()
        # 获得纯文本正文
        blog_text = request.form.get('plainText')
        # 草稿
        draft = True
        if request.form.get('draft') == 'false':
            draft = False
        # 如果是编辑已存在文章，form 中应该有已存在文章的id
        blog_id = request.form.get('blog_id')
        # 如果表单中的 blog_id 有值说明该文章是重新编辑文章，不需创建新的
        if blog_id:
            try:
                old_blog = Blog.query.filter_by(id=int(blog_id)).first()
                old_blog.draft = draft
                old_blog.body = blog_text
                db.session.add(old_blog)
                success = True
            except ParsingError as e:
                print(e)
        else:
            # 创建新文章并添加进数据库
            try:
                new_blog = Blog(
                    body=blog_text, author_id=author.id, draft=draft)
                db.session.add(new_blog)
                success = True
            except ParsingError as e:
                print(e)

        if success:
            if not draft:
                flash('Your blog is successfully uploaded!')
            else:
                flash('Your blog is successfully saved as a draft.')
            # 重定向到编辑页
            return redirect(url_for('editor.index'))
        else:
            flash('There is something wrong in your format. Committing abolished.')
            return render_template('editor/index.html', text=blog_text)

    # 如果 session 中有 blog_id 值说明是从 edit 路由重定向过来的
    if session.get('blog_id'):
        # 从 session 中获得 blog_id 并立即删除 session 中的值
        blog_id = session['blog_id']
        del session['blog_id']
        blog = Blog.query.filter_by(id=blog_id).first()
        # 查找该博文如果存在：
        if blog:
            # 将已有内容渲染到页面上，并附上 blog_id 作为隐藏标签的值
            return render_template('editor/index.html', text=blog.body, blog_id=blog_id)

    placeholder = '---\ntitle: <title>\ncategory: <category>\ntags: []\n---\n<summary>\n<!-- more -->\n<Content>'
    return render_template('editor/index.html', text=placeholder)


# 用户文章重新编辑路由（博文页面上的 edit 按钮）
@editor.route('/edit/<int:blog_id>')
def edit(blog_id):
    session['blog_id'] = blog_id
    return redirect(url_for('editor.index'))
