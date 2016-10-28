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
    SQLALCHEMY_TRACK_MODIFICATIONS = True


# 开发环境配置类
class DevelopmentConfig(Config):
    # debug 模式
    DEBUG = True
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
    # 数据库URL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


# 测试配置类
class TestingConfig(Config):
    # 测试模式
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


# 生产环境类
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


# 注册不同配置环境，并设默认配置为开发配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
