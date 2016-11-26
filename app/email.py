# -*- coding: utf-8 -*-
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    # 创建邮件内容
    msg = Message(app.config['BLEXT_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['BLEXT_MAIL_SENDER'], recipients=[to])
    # 创建纯文本正文
    msg.body = render_template(template + '.txt', **kwargs)
    # 创建富文本正文
    msg.html = render_template(template + '.html', **kwargs)
    # 异步发送邮件
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
