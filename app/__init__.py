import logging

from config import Config
from flask import Flask
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message_category = "info"
login.refresh_view = "auth.login"
login.needs_refresh_message_category = "info"
login.needs_refresh_message = "To protect your account, please log in again to access this page."
limiter = Limiter(key_func=get_remote_address, default_limits=["2 per second", "60 per minute"])
compress = Compress()
talisman = Talisman()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    limiter.init_app(app)
    compress.init_app(app)
    csp = {
        "default-src": "'self'",
        "style-src": ["https://cdn.jsdelivr.net", "https://use.fontawesome.com"],
        "font-src": "https://use.fontawesome.com",
        "script-src": "https://cdn.jsdelivr.net",
        "img-src": ["data:", "'self'"],
    }
    talisman.init_app(app, content_security_policy=csp, content_security_policy_nonce_in=["style-src"])

    # Register blueprints
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.account import bp as account_bp

    app.register_blueprint(account_bp, url_prefix="/account")

    from app.entry import bp as entry_bp

    app.register_blueprint(entry_bp, url_prefix="/entries")

    from app.tag import bp as tag_bp

    app.register_blueprint(tag_bp, url_prefix="/tags")

    from app.search import bp as search_bp

    app.register_blueprint(search_bp, url_prefix="/search")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Startup")

    return app


from app import models
