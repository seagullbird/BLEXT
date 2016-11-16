from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime


# （用户）角色模型
class Role(db.Model):
    # 表名
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    # 角色名
    name = db.Column(db.String(64), unique=True)

    # 对于一个Role类的实例，其 users 属性将返回与角色相关联的用户组成的列表
    # backref参数向User模型中添加一个role属性，从而定义反向关系。这一属性可替代role_id访问
    # Role模型，此时获取的是模型对象，而不是外键的值
    # dynamic: 不加载记录，但提供加载记录的查询
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


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
    # 外键，这列的值是roles表中行的id值
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 用户的文章
    blogs = db.relationship('Blog', backref='author', lazy='dynamic')
    # 用户密码散列值
    password_hash = db.Column(db.String(128))
    # 是否已确认邮箱
    confirmed = db.Column(db.Boolean, default=False)
    # 用户个性签名
    bio = db.Column(db.String(64))
    # 用户about_me
    about_me = db.Column(db.Text)
    # 用户头像图片地址
    avatar_url = db.Column(db.String(256))
    # 用户博客标题
    blog_title = db.Column(db.String(32))

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

    # 生成修改邮件地址令牌
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    # 修改邮件地址
    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


# 博客文章模型
class Blog(db.Model):
    # 表名
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    # 文章标题
    title = db.Column(db.String(128))
    # 文章简介
    summary = db.Column(db.Text)
    # 文章分类
    category = db.Column(db.String(20))
    # 文章标签
    tags = db.relationship('Tag', backref='blog', lazy='dynamic')
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


# 文章标签模型
class Tag(db.Model):
    # 表名
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    # 标签名
    name = db.Column(db.String(20))
    # 对应的文章
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))


# 加载用户的回调函数，用 user_id 查找用户并返回用户对象
# bug 记录：注意，如果不在 manage.py 里面 import User 模型，将无法加载这个回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
