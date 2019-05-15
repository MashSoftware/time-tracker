from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'
login.refresh_view = 'login'
login.needs_refresh_message_category = 'info'
login.needs_refresh_message = 'To protect your account, please log in again to access this page.'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

from app import routes, models, errors
