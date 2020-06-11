import os
from flask import render_template, send_from_directory
from .utils import log_exception


def init_standard_views(app):
    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    @app.errorhandler(404)
    def missing_page(exception):
        """Catch internal 404 errors, display
            a nice error page and log the error.
        """
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def forbidden_page(exception):
        """Catch internal 404 errors, display
            a nice error page and log the error.
        """
        return render_template("404.html"), 403

    @app.errorhandler(500)
    @app.errorhandler(Exception)
    def internal_error(exception):
        """Catch internal exceptions and 500 errors, display
            a nice error page and log the error.
        """
        log_exception(exception)
        return render_template("500.html"), 500
