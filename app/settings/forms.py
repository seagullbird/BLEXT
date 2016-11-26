from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Required, EqualTo, Length


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


class ProfileSettingForm(FlaskForm):
    # 用户签名字段
    bio = StringField('Bio', validators=[Length(0, 64)])
    # 用户头像
    avatar_url = StringField('Avatar URL', validators=[Length(0, 256)])
    # 用户博客标题
    blog_title = StringField('Blog Title', validators=[Length(0, 32)])
    # 用户 about me 字段
    about_me = TextAreaField('About me (In markdown)')

    submit = SubmitField('Update Profile')
