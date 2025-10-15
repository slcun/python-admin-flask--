from flask import render_template, jsonify


def init_error_views(app):
    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(405)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(429)
    def ratelimit_exceeded(e):
        return jsonify(
            success=False, msg="请求频率超限，请稍后再试。"
        )
