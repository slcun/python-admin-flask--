from flask_limiter import Limiter
from flask_login import current_user
from flask import request, Flask


# 定义 key 函数：优先使用 current_user.id，否则用 IP
def get_user_identifier():
    # 注意：current_user 可能是 AnonymousUserMixin（未登录）
    if hasattr(current_user, 'id') and current_user.is_authenticated:
        return str(current_user.id)  # 用户 ID 作为 key
    return request.remote_addr  # 未登录用户则按 IP 限流

limiter = Limiter(
    key_func=get_user_identifier,
    # default_limits=["100 per hour"],  # 可选全局默认
    storage_uri="memory://"  # 生产建议: "redis://localhost:6379"
)

def init_limit(app: Flask) -> None:
    limiter.init_app(app)