import uuid
from datetime import datetime

import bcrypt
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'user_account'

    # Fields
    id = db.Column(UUID, primary_key=True)
    password = db.Column(db.Binary, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    email_address = db.Column(db.String, nullable=False, unique=True, index=True)
    login_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Methods
    def __init__(self, password, first_name, last_name, email_address):
        self.id = str(uuid.uuid4())
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email_address = email_address.lower()
        self.created_at = datetime.utcnow()
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('UTF-8'), self.password)


@login.user_loader
def load_user(id):
    return User.query.get(id)
