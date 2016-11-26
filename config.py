import os
# 获取项目根路径
basedir = os.path.abspath(os.path.dirname(__file__))


# 通用配置类
class Config:
    # 配置密钥（从环境变量中读取或为默认值）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 邮件主题的前缀
    BLEXT_MAIL_SUBJECT_PREFIX = '[Blext]'
    # 发件人的地址
    BLEXT_MAIL_SENDER = 'Blext admin <380554381@qq.com>'
    # 电子邮件收件人
    BLEXT_ADMIN = os.environ.get('BLEXT_ADMIN')
    # 用户博客主页每页显示文章数
    BLEXT_BLOGS_PER_PAGE = 5
    # API每次get_blogs请求返回的每页文章数
    API_BLOGS_PER_PAGE = 5
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 数据库缓慢查询阈值
    BLEXT_SLOW_DB_QUERY_TIME = 0.5
    # 告诉Flask-SQLAlchemy启用记录查询统计数字的功能
    SQLALCHEMY_RECORD_QUERIES = True
    # 邮件服务器的主机名
    MAIL_SERVER = 'smtp.qq.com'
    # 邮件服务器端口
    MAIL_PORT = 587
    # 启用传输层安全（TLS）协议
    MAIL_USE_TLS = True
    # 邮件帐户用户名
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # 邮件账户密码
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # 默认情况下不使用SSL
    SSL_DISABLE = True

    @staticmethod
    def init_app(app):
        pass


# 开发环境配置类
class DevelopmentConfig(Config):
    # debug 模式
    DEBUG = True
    # 数据库URL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


# 测试配置类
class TestingConfig(Config):
    # 测试模式
    TESTING = True
    # 禁用 CSRF 保护功能
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


# 生产环境类
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.BLEXT_MAIL_SENDER,
            toaddrs=[cls.BLEXT_ADMIN],
            subject=cls.BLEXT_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # 输出到stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


# 注册不同配置环境，并设默认配置为开发配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig
}
