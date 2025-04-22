from flask import Flask
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from extensions import db, login_manager

from logging_setup import setup_logging

def create_app():
    import os

    print("Current working directory:", os.getcwd())

    app = Flask(__name__)
    app.config.from_object(Config)

    setup_logging(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_debugger=True, use_reloader=True)
