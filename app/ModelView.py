from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask import redirect, url_for
from flask_login import current_user


class BLEXTModelView(ModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'seagullbird'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))


class BLEXTAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'seagullbird'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))


class UserModelView(BLEXTModelView):
    column_exclude_list = ['password_hash']
    column_editable_list = ['blog_title']


class BlogModelView(BLEXTModelView):
    column_exclude_list = ['body', 'html']
    column_editable_list = ['title', 'draft', 'author', 'category']


class CateModelView(BLEXTModelView):
    column_filters = ['author']
    column_editable_list = ['name']


class TagModelView(BLEXTModelView):
    column_filters = ['author']
    column_editable_list = ['name']
