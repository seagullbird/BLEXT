from . import auth
from flask import render_template, flash, url_for, redirect, request
from .forms import SigninForm, SignupForm, ChangePasswordForm, PasswordResetForm, PasswordResetRequestForm, ChangeEmailForm
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .. import db
from ..email import send_email


# 请求钩子：过滤未确认用户
# 使用 before_app_request 装饰器来使用针对全局请求的钩子
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


# 确认相关信息页面
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


# 登录页面
@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    # 登录表单模型
    signinForm = SigninForm()
    # 如果表单验证通过：
    if signinForm.validate_on_submit():
        # 按照表单所提交的信息从数据库中查询
        user = User.query.filter_by(email=signinForm.email.data).first()
        # 如果能够查找到该用户并且密码正确：
        if user is not None and user.verify_password(signinForm.password.data):
            # 登入用户
            login_user(user, signinForm.remember_me.data)
            # 用户访问未授权的URL时会显示登录表单，Flask-Login会把原地址保存在查询字符串的
            # next参数中，这个参数可从request.args字典中读取。如果读取不到则重定向到主页
            return redirect(request.args.get('next') or url_for('user.index', username=user.username))
        # 否则提醒错误的信息
        flash('Invalid username or password.')
    return render_template('auth/sign_in.html', form=signinForm)


# 注册页面
@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    # 注册表单模型
    signupForm = SignupForm()
    # 如果表单验证通过：
    if signupForm.validate_on_submit():
        # 创建新用户对象
        user = User(email=signupForm.email.data,
                    username=signupForm.username.data,
                    password=signupForm.password.data)
        # 添加到数据库（会自动提交）
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        # 将用户作为未确认用户登录
        login_user(user, False)
        # 重定向到确认相关信息页面
        return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/sign_up.html', form=signupForm)


# 确认账户页面
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    # 如果当前用户已被确认：
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    # 检验令牌：
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    # 重定向到主页
    return redirect(url_for('main.index'))


# 登出页面
@auth.route('sign_out')
@login_required
def sign_out():
    # 登出用户
    logout_user()
    # 提示用户
    flash('You have been signed out.')
    # 重定向到主页
    return redirect(url_for('main.index'))


# 重新发送确认邮件路由，重做一遍注册路由中的工作
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


# 修改密码页面
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # 如果旧密码输入正确
        if current_user.verify_password(form.old_password.data):
            # 更改旧密码为新密码并提交
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


# 重设密码请求页面
@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            # 向用户邮箱发送令牌邮件确认用户身份
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.sign_in'))
    return render_template('auth/reset_password.html', form=form)


# 重设密码页面
@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.sign_in'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


# 重设邮件地址请求页面
@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            # 需要向新邮件地址发送确认邮件
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


# 重设邮件地址页面
@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
