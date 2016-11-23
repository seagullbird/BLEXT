# 使用 flask 扩展 flask_httpauth 实现的 REST web 服务用户验证
from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
from . import api
from ..models import User
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()

# 用户第一次验证时，必须提供邮箱和密码，如果第一次验证访问的是'/token'路由，验证通过后会得到
# 一个token值，该token的过期时间是一个小时。之后的一个小时内用户可以直接使用token进行访问，
# 避免了多次发送敏感信息。token过期后，再通过token访问会得到
# 'Invalid credentials'的回复，此时应该重新用邮箱和密码访问'/token'路由以获得新的token值。

# 另外，此api仅提供给配套编辑器使用，用于返回已登录用户的个人账号信息及发布文章，
# 匿名用户（未登录）不能获取任何信息，所以该api不提供对匿名用户的支持。


# 验证用户密码的回调函数
@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token:
        if password:
            user = User.query.filter_by(email=email_or_token).first()
            if user:
                g.current_user = user
                g.token_used = False
                return user.verify_password(password)
        # 如果 password 为空，则假定 email_or_token 是令牌
        else:
            g.current_user = User.verify_auth_token(email_or_token)
            # 为了让视图函数能区分两种认证方法
            # 存储在flask全局变量中的 token_used 变量表明了是否已经使用了token验证
            g.token_used = True
            return g.current_user is not None
    return False


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


# 请求钩子，确保了每一次对api路由的访问都需要用户验证，
# 并且作为附加验证，未确认账户的用户也不能访问api
# （所以其余对于资源端点的定义都不用考虑用户验证问题，因为先在这里就已经全部处理了
@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


# 向客户端返回令牌的视图函数
@api.route('/token')
def get_token():
    # 如果已经使用了token验证，则不能重新获取token（直到上一个token过期）
    if g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})
