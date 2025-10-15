import re
import inspect
from flask.cli import AppGroup
from flask import current_app

check_cli = AppGroup('check', help='Commands for checking application aspects.')

@check_cli.command('auth')
def check_auth():
    """检查路由视图函数的 @login_required 和 @authorize(...) 装饰器使用情况。"""
    app = current_app
    if not app:
        print("错误：未在应用上下文中运行。请使用 'flask check auth' 命令。")
        return

    print("\n" + "="*120)
    print("Flask 路由鉴权装饰器检查报告".center(120))
    print("="*120)
    # 调整列宽以适应更长的权限字符串
    header_format = "{:<35} {:<35} {:<30} {:<20} {:<30}"
    row_format = "{:<35} {:<35} {:<30} {:<20} {:<30}"
    print(header_format.format("Endpoint", "URL Rule", "View Function", "@login_required", "@authorize(...)"))
    print("-" * 120)

    has_missing_auth = False # 标记是否有缺失鉴权的路由

    with app.app_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'static':
                continue

            view_func = app.view_functions.get(rule.endpoint)
            if not view_func:
                continue

            # --- 获取源代码 ---
            try:
                # 使用 getsourcelines 可能更稳定，获取整个函数定义
                source_lines = inspect.getsourcelines(view_func)[0]
                source_code = "".join(source_lines)
            except (OSError, TypeError):
                # 如果无法获取源代码（如 C 扩展），则跳过
                source_code = ""

            # --- 检查 @login_required 装饰器 ---
            # 匹配常见的形式，包括可能的模块前缀
            has_login_required = bool(re.search(r"@.*login_required", source_code))

            # --- 检查 @authorize 装饰器并提取权限 ---
            authorize_permissions_list = []
            # 改进的正则表达式：
            # @ : 匹配 @ 符号
            # (?:.*?\.)? : 非捕获组，匹配可能的模块名和点 (例如 auth.)
            # authorize : 匹配 authorize 函数名
            # \( : 匹配左圆括号
            # ([^)]*) : 捕获组，匹配括号内的所有内容 (非右括号字符)
            # \) : 匹配右圆括号
            # 这个模式会找到 @authorize(...) 的整个调用
            authorize_calls = re.findall(r"@.*?authorize\s*\(([^)]*)\)", source_code, re.DOTALL)

            for call_args in authorize_calls:
                # 在找到的参数字符串中，再次使用正则提取被引号包围的权限字符串
                # 匹配单引号或双引号内的内容
                permissions_found = re.findall(r"['\"]([^'\"]+)['\"]", call_args)
                authorize_permissions_list.extend(permissions_found)

            # 将找到的所有权限字符串用逗号连接
            authorize_permissions = ", ".join(authorize_permissions_list) if authorize_permissions_list else "N/A"

            # --- 判断是否可能缺失鉴权 ---
            # 简单判断：如果既没有 login_required 也没有 authorize 权限，则标记
            if not has_login_required and not authorize_permissions_list:
                 has_missing_auth = True

            # --- 格式化输出 ---
            login_status = "✅ Yes" if has_login_required else "❌ No"
            auth_status = authorize_permissions if authorize_permissions != "N/A" else "❌ N/A"

            # 格式化字符串长度
            def truncate(s, length):
                return s if len(s) <= length else s[:length-2] + ".."

            endpoint_str = truncate(rule.endpoint, 34)
            rule_str = truncate(str(rule), 34)
            func_name_str = truncate(view_func.__name__, 29)

            print(row_format.format(endpoint_str, rule_str, func_name_str, login_status, auth_status))

    print("-" * 120)
    if has_missing_auth:
        print("\n⚠️  注意：以上标记为 '❌ No' 和 '❌ N/A' 的路由可能缺少鉴权，请仔细检查！")
    else:
        print("\n✅ 所有路由似乎都应用了至少一种鉴权机制。")
    print("="*120 + "\n")

