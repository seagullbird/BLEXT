from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User


# 用户登录表单类
class SigninForm(FlaskForm):
    # 电子邮件字段
    email = StringField('Email', validators=[
                        Required(), Length(1, 64), Email()])
    # 密码字段
    password = PasswordField('Password', validators=[Required()])
    # 记住我字段
    remember_me = BooleanField('Keep me logged in')
    # 提交按钮
    submit = SubmitField('Log In', render_kw={"class_": "btn btn-info"})


# 用户注册表单类
class SignupForm(FlaskForm):
    # 电子邮件字段
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    # 用户名字段
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    # 密码字段
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    # 确认密码字段
    password2 = PasswordField('Confirm password', validators=[Required()])
    # 提交按钮
    submit = SubmitField('Register')

    # 手动添加的 email 验证方法，通过数据库查询判断邮箱是否已经注册
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    # 手动添加的 username 验证方法，通过数据库查询判断用户名是否已经注册
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


# 用户修改密码表单
class ChangePasswordForm(FlaskForm):
    # 旧密码字段
    old_password = PasswordField('Old password', validators=[Required()])
    # 新密码字段
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    # 确认新密码字段
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')


# 提交重设密码请求表单
class PasswordResetRequestForm(FlaskForm):
    # 邮箱字段
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


# 重设密码页面表单
class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    # 验证邮箱是否存在
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


# 修改邮件地址表单
class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    # 验证邮箱是否存在
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
