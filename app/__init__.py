# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_admin import Admin


# 声明各扩展对象
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()

# 设置安全等级为 strong ,
# Flask-Login会记录客户端IP地址和浏览器的用户代理信息，如果发现异动就登出用户
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.sign_in'


# 定义程序工厂函数
def create_app(config_name):
    # 初始化程序实例
    app = Flask(__name__)
    # 导入配置
    app.config.from_object(config[config_name])

    # 初始化各扩展对象
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 添加 Model View
    from .models import User, Blog, Category, Tag
    from .ModelView import BLEXTAdminIndexView, UserModelView, BlogModelView, CateModelView, TagModelView
    admin = Admin(app=app, name='BLEXT Backstage', index_view=BLEXTAdminIndexView())
    admin.add_view(UserModelView(User, db.session, endpoint='user-admin'))
    admin.add_view(BlogModelView(Blog, db.session, endpoint='blog-admin'))
    admin.add_view(CateModelView(Category, db.session, endpoint='cate-admin'))
    admin.add_view(TagModelView(Tag, db.session, endpoint='tag-admin'))

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    # 注册各蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    from .editor import editor as editor_blueprint
    app.register_blueprint(editor_blueprint, url_prefix='/editor')
    from .settings import settings as settings_blueprint
    app.register_blueprint(settings_blueprint, url_prefix='/settings')
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    # 返回程序实例
    return app
