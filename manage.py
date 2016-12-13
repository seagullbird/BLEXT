#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
COV = None
# 如果环境变量中有FLASK_COVERAGE，启动代码覆盖检测
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    # 启动覆盖检测引擎
    # branch=True 开启分支覆盖分析，
    # 除了跟踪哪行代码已经执行外，还要检查每个条件语句的True分支和False分支是否都执行了
    # include选项用来限制程序包中文件的分析范围，只对这些文件中的代码进行覆盖检测
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from flask_script import Shell, Manager
from app.models import User, Blog, Tag, Category
from flask_migrate import Migrate, MigrateCommand

# 创建程序实例
app = create_app(os.getenv('BLEXT_CONFIG') or 'default')
# 初始化 Manager 对象（用于命令行解析）
manager = Manager(app)
# 初始化 Migrate 对象（用于数据库迁移）
migrate = Migrate(app, db)


# shell 命令的回调函数，用于自动导入特定对象（而不用每次执行 shell 命令时去初始化）
def make_shell_context():
    return dict(app=app, db=db, User=User, Blog=Blog, Category=Category, Tag=Tag)


# 添加命令行 shell 命令
manager.add_command('shell', Shell(make_context=make_shell_context))
# 添加命令行 db 命令
manager.add_command('db', MigrateCommand)


# 为 test 命令添加可选项 --coverage （flask-script会自动根据传入参数名确定选项名），
# 并据此向函数中传入True或False
@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        # 重启脚本（因为收到coverage参数时全局作用域中的代码已经执行了，为了检测的准确性）
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)


# 在请求分析器的监视下运行程序
@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


# 程序部署命令
@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()


if __name__ == '__main__':
    manager.run()
