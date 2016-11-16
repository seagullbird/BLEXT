#!/usr/bin/env python3
import os
from app import create_app, db
from flask_script import Shell, Manager
from app.models import User, Role, Blog, Tag
from flask_migrate import Migrate, MigrateCommand

# 创建程序实例
app = create_app(os.getenv('BLEXT_CONFIG') or 'default')
# 初始化 Manager 对象（用于命令行解析）
manager = Manager(app)
# 初始化 Migrate 对象（用于数据库迁移）
migrate = Migrate(app, db)


# shell 命令的回调函数，用于自动导入特定对象（而不用每次执行 shell 命令时去初始化）
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Blog=Blog, Tag=Tag)


# 添加命令行 shell 命令
manager.add_command('shell', Shell(make_context=make_shell_context))
# 添加命令行 db 命令
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
