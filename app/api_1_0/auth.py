# 使用 flask 扩展 flask_httpauth 实现的 REST web 服务用户验证
from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
from . import api
from ..models import User
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


# 验证用户密码的回调函数
@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token:
        if password:
            user = User.query.filter_by(email=email_or_token).first()
            if user:
                g.current_user = user
                return user.verify_password(password)
        # 如果 password 为空，则假定 email_or_token 是令牌
        else:
            g.current_user = User.verify_auth_token(email_or_token)
            # 为了让视图函数能区分两种认证方法
            g.token_used = True
            return g.current_user is not None
    return False


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


# 向客户端返回令牌的视图函数
@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})
