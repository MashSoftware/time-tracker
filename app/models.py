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
    email_address = db.Column(db.String, nullable=False, unique=True, index=True)
    timezone = db.Column(db.String, nullable=False, server_default='UTC')
    login_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Relationships
    events = db.relationship('Event', backref='user', lazy=True, passive_deletes=True)

    # Methods
    def __init__(self, password, email_address, timezone):
        self.id = str(uuid.uuid4())
        self.email_address = email_address.lower()
        self.timezone = timezone
        self.created_at = datetime.utcnow()
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('UTF-8'), self.password)


@login.user_loader
def load_user(id):
    return User.query.get(id)


class Event(db.Model):
    # Fields
    id = db.Column(UUID, primary_key=True)
    user_id = db.Column(UUID, db.ForeignKey('user_account.id', ondelete="CASCADE"), nullable=False, index=True)
    started_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    ended_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Methods
    def __init__(self, user_id, started_at):
        self.id = str(uuid.uuid4())
        self.user_id = str(uuid.UUID(user_id, version=4))
        self.started_at = started_at
