from . import editor
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from .. import db
from ..models import Blog
from werkzeug import secure_filename
import mistune


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
            # 取得文件标题
            filename = secure_filename(file.filename)
            # 取得文件内容（以str形式）
            markdown_body = file.stream.read().decode('utf-8')

            # 利用 mistune 将文章转换为 html 形式并存储
            markdown = mistune.Markdown()
            html_body = markdown(markdown_body)

            # 取得文章摘要
            summary = ''
            # 按行遍历文章内容：
            for line in markdown_body.split('\n'):
                # 如果找到摘要结束标志则退出
                if line.strip() == '<!-- more -->':
                    break
                # 否则将summary加上这一行
                summary += line + '\n'
            # 如果全文没有摘要标志则取全文前50个字
            else:
                summary = summary[:50] + '...'
            summary = summary.strip('\n').replace('\n', '<br>')
            # 创建新文章并添加进数据库
            new_blog = Blog(title=filename.split('.')[
                            0], summary=summary, body=markdown_body, html=html_body, author=current_user._get_current_object())
            db.session.add(new_blog)
            flash('Your blog is successfully uploaded!')
        # 重定向到编辑页
        return redirect(url_for('editor.index'))

    return render_template('editor/index.html')
