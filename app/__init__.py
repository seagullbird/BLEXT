from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config

# 声明各扩展对象
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()


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

    # 注册各蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    # 返回程序实例
    return app
