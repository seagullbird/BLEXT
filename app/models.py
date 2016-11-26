from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from datetime import datetime
import mistune
import bleach
from .blog_parser import Blog_Parser
from .exceptions import ParsingError


# 用户模型
# 继承 UserMixin ，包含要使用 Flask-login 的一些默认方法
class User(db.Model, UserMixin):
    # 表名
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # 用户名，唯一
    username = db.Column(db.String(64), unique=True, index=True)
    # 用户邮箱
    email = db.Column(db.String(64), unique=True, index=True)
    # 用户的文章
    blogs = db.relationship('Blog', backref='author', lazy='dynamic')
    # 用户密码散列值
    password_hash = db.Column(db.String(128))
    # 是否已确认邮箱
    confirmed = db.Column(db.Boolean, default=False)
    # 用户个性签名
    bio = db.Column(db.String(64))
    # 用户about_me纯文本
    about_me_text = db.Column(db.Text)
    # 用户about_me富文本
    about_me = db.Column(db.Text)
    # 用户头像图片地址
    avatar_url = db.Column(db.String(256))
    # 用户博客主页标题
    blog_title = db.Column(db.String(32))
    # 用户文章的所有分类
    categories = db.relationship('Category', backref='author', lazy='dynamic')
    # 用户文章的所有标签
    tags = db.relationship('Tag', backref='author', lazy='dynamic')

    # 将 password 属性设置为只写属性，即不能直接通过 .password 访问密码值
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 设置用户密码，保存密码散列值
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码验证
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成确认令牌
    def generate_confirmation_token(self, expiration=3600):
        # 使用通用密钥生成签名，过期时间默认为一小时（3600秒）
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # dumps()方法为指定的数据生成一个加密签名，
        # 然后再对数据和签名进行序列化，生成令牌字符串
        return s.dumps({'confirm': self.id})

    # 检验令牌
    def confirm(self, token):
        # 检验令牌方法检验令牌中包含的 id 是否和当前已登录的用户相匹配
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # 生成重设密码令牌
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    # 重设密码
    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    # 生成 api 确认令牌
    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    # 验证 api 确认令牌（如果验证通过则返回用户对象）
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    # 将用户资源转化为JSON格式的序列化字典（用于api）
    def to_json(self):
        return {
            'url': url_for('api.get_user', _external=True),
            'username': self.username,
            'blogs': url_for('api.get_blogs', _external=True),
            'categories': url_for('api.get_user_categories', _external=True),
            'tags': url_for('api.get_user_tags', _external=True),
            'avatar_url': self.avatar_url,
            'blog_count': self.blogs.count()
        }

    def __repr__(self):
        return '<User %r>' % self.username


# 文章与标签关系表
blog_tag = db.Table('blog_tag',
                    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                    db.Column('page_id', db.Integer, db.ForeignKey('blogs.id'))
                    )


# 博客文章模型
class Blog(db.Model):
    # 表名
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    # 文章标题
    title = db.Column(db.String(128))
    # 文章简介纯文本
    summary_text = db.Column(db.Text)
    # 文章简介
    summary = db.Column(db.Text)
    # 文章分类
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    # 文章标签
    tags = db.relationship('Tag', secondary=blog_tag,
                           backref=db.backref('blogs', lazy='dynamic'))
    # 文章正文（纯文本）
    body = db.Column(db.Text)
    # 文章正文（html）
    html = db.Column(db.Text)
    # 时间戳
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 作者
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 是否草稿
    draft = db.Column(db.Boolean, default=False)

    # 当body属性更新时，自动从body中解析出其余各项属性并更新（或新建）
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        markdown = mistune.Markdown()
        blog_parser = Blog_Parser(value)
        # html中允许的html标签
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']
        # 利用parse函数从value（也就是被改变的body）值中解析出各项属性并赋值
        try:
            title, category_name, tag_names, summary_text, content = blog_parser.parse()
            target.title = title
            target.summary_text = summary_text
            target.summary = markdown(summary_text)
            target.html = bleach.linkify(bleach.clean(
                markdown(content),
                tags=allowed_tags, strip=True))
            target.change_category(Category.generate_category(
                category_name, target.author_id))
            target.change_tags(Tag.generate_tags([t.strip() for t in tag_names.strip(
                '[').strip(']').split(',')], target.author_id))

        except ParsingError as e:
            raise ParsingError(e)

    # 更新标签处理
    def change_tags(self, new_tags):
        old_tags = self.tags
        # 求差集，new_tags 中没有而 old_tags 中有的为已删除标签
        deleted_tags = list(set(old_tags).difference(set(new_tags)))
        # 删除原有的所有标签
        self.tags.clear()
        # 更新新的标签
        self.tags = new_tags
        # 对于已删除的标签，如果其下没有任何文章则删除该标签
        for tag in deleted_tags:
            if not tag.blogs.all():
                db.session.delete(tag)

    # 更新分类处理
    def change_category(self, new_category):
        old_category = self.category
        if old_category:
            # 如果新分类与原分类不同才处理
            if new_category != old_category:
                # 更新分类
                self.category = new_category
                # 如果原分类下再没有任何文章则删除原分类
                if not old_category.blogs.all():
                    db.session.delete(old_category)
        else:
            self.category = new_category

    # 删除标签处理（删除文章时）
    def delete_tags(self):
        cur_tags = self.tags[:]
        for tag in cur_tags:
            tag.blogs.remove(self)
            # 如果该标签下删除这篇博文后没有其他博文了则删除该标签
            if not tag.blogs.all():
                db.session.delete(tag)

    # 删除分类处理（删除文章时）
    def delete_category(self):
        cur_category = self.category
        # 如果该分类下删除这篇博文后没有其他博文了则删除该分类
        cur_category.blogs.remove(self)
        if not cur_category.blogs.all():
            db.session.delete(cur_category)

    # 将博客文章资源转化为JSON格式的序列化字典（用于api）
    def to_json(self):
        # _external=True 指定生成完整 URL （而不是相对 URL ）
        return {
            'url': url_for('api.get_blog', blog_id=self.id, _external=True),
            'id': self.id,
            'title': self.title,
            'summary_text': self.summary_text,
            'body': self.body,
            'timestamp': self.timestamp,
            'draft': self.draft,
            'author': url_for('api.get_user', _external=True),
            'category': url_for('api.get_blog_category', blog_id=self.id, _external=True),
            'tags': url_for('api.get_blog_tags', blog_id=self.id, _external=True)
        }

    def __repr__(self):
        return '<Blog %r>' % self.title


# 将 on_change_body 函数注册到 body 字段上
# 只要 body 字段设定了新值，on_change_body 函数就会自动调用
db.event.listen(Blog.body, 'set', Blog.on_changed_body)


# 文章分类模型（一篇文章对应一个分类，一个分类对应多篇文章）
class Category(db.Model):
    # 表名
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    # 分类名
    name = db.Column(db.String(20))
    # 对应的文章
    blogs = db.relationship('Blog', backref='category', lazy='dynamic')
    # 对应的用户
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # 从分类名 category_name 和用户 id 生成新分类（如果不存在）
    @staticmethod
    def generate_category(category_name, author_id):
        category = Category.query.filter_by(
            name=category_name, author_id=author_id).first()
        # 如果当前用户名下不存在这个分类则新建：
        if not category:
            category = Category(name=category_name, author_id=author_id)
        return category

    def to_json(self):
        return {
            'name': self.name
        }

    def __repr__(self):
        return '<Category %r>' % self.name


# 文章标签模型
class Tag(db.Model):
    # 表名
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    # 标签名
    name = db.Column(db.String(20))
    # 对应的用户
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # 从标签名 list 和 用户 id 生成 Tag 类型列表
    @staticmethod
    def generate_tags(tag_names, author_id):
        tags = []
        # 处理文章标签
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:
                # 在用户名下查询标签名
                tag = Tag.query.filter_by(
                    name=tag_name, author_id=author_id).first()
                # 如果不存在则新建并添加
                if not tag:
                    tag = Tag(name=tag_name, author_id=author_id)
                    # 添加进数据库
                    db.session.add(tag)
                tags.append(tag)
        return tags

    def to_json(self):
        return {
            'name': self.name
        }

    def __repr__(self):
        return '<Tag %r>' % self.name


# 加载用户的回调函数，用 user_id 查找用户并返回用户对象
# bug 记录：注意，如果不在 manage.py 里面 import User 模型，将无法加载这个回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
