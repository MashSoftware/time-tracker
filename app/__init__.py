import logging

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

csrf = CSRFProtect()
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address, default_limits=["2 per second", "60 per minute"])
login = LoginManager()
login.login_message_category = "info"
login.login_view = "auth.login"
login.needs_refresh_message = "To protect your account, please log in again to access this page."
login.needs_refresh_message_category = "info"
login.refresh_view = "auth.login"
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # Initialise app extensions
    csrf.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.account import bp as account_bp
    from app.auth import bp as auth_bp
    from app.entry import bp as entry_bp
    from app.location import bp as location_bp
    from app.main import bp as main_bp
    from app.search import bp as search_bp
    from app.tag import bp as tag_bp

    app.register_blueprint(account_bp, url_prefix="/account")
    app.register_blueprint(auth_bp)
    app.register_blueprint(entry_bp, url_prefix="/entries")
    app.register_blueprint(location_bp, url_prefix="/locations")
    app.register_blueprint(main_bp)
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(tag_bp, url_prefix="/tags")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Startup")

    return app


from app import models  # noqa: E402,F401
