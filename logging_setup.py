import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, request
from flask_login import current_user

def setup_logging(app: Flask):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)

    @app.before_request
    def log_request_info():
        user = current_user.get_id() if current_user.is_authenticated else 'Anonymous'
        app.logger.info(f"User: {user} - {request.method} {request.path}")

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled Exception: {e}", exc_info=True)
        return "Internal Server Error", 500
