from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress
from flask_talisman import Talisman

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message_category = 'info'
login.refresh_view = 'auth.login'
login.needs_refresh_message_category = 'info'
login.needs_refresh_message = 'To protect your account, please log in again to access this page.'
limiter = Limiter(app, key_func=get_remote_address, default_limits=["1 per second", "60 per minute"])
Compress(app)
csp = {
    'default-src': '\'self\'',
    'style-src': [
        'stackpath.bootstrapcdn.com',
        'use.fontawesome.com'
    ],
    'font-src': 'use.fontawesome.com',
    'script-src': [
        'code.jquery.com',
        'cdnjs.cloudflare.com',
        'stackpath.bootstrapcdn.com'
    ],
    'img-src': 'data:'
}
Talisman(app, content_security_policy=csp)

# Register blueprints
from app.auth import bp as auth_bp
from app.account import bp as account_bp
from app.entry import bp as entry_bp
app.register_blueprint(auth_bp)
app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(entry_bp, url_prefix='/entries')

from app import routes, models, errors
