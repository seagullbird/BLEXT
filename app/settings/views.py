# -*- coding: utf-8 -*-
from . import settings
from flask import render_template, flash, redirect, url_for
from .forms import ChangePasswordForm, ProfileSettingForm
from flask_login import login_required, current_user, logout_user
from .. import db
import mistune


# 设置个人资料
@settings.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_setting():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # 如果旧密码输入正确
        if current_user.verify_password(form.old_password.data):
            # 更改旧密码为新密码并提交
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated. Please sign in again.')
            logout_user()
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
            return redirect(url_for('settings.admin_setting'))
    return render_template('user/settings.html', title='Personal Account', form=form, host_user=current_user)


# 设置账户资料
@settings.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_setting():
    form = ProfileSettingForm()
    if form.validate_on_submit():
        if form.bio.data:
            current_user.bio = form.bio.data
        if form.avatar_url.data:
            current_user.avatar_url = form.avatar_url.data
        if form.blog_title.data:
            current_user.blog_title = form.blog_title.data
        if form.about_me.data:
            current_user.about_me_text = form.about_me.data
            markdown = mistune.Markdown()
            # 利用markdown解析器将markdown转换为html
            current_user.about_me = markdown(form.about_me.data)
        db.session.add(current_user)
        return redirect(url_for('user.index', username=current_user.username))
    form.bio.data = current_user.bio
    form.avatar_url.data = current_user.avatar_url
    form.blog_title.data = current_user.blog_title
    form.about_me.data = current_user.about_me_text
    return render_template('user/settings.html', title='Public Profile', form=form, host_user=current_user)
