import uuid
from datetime import datetime
from time import time

import bcrypt
import jwt
import pytz
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID

from app import db, login
from app.utils import seconds_to_decimal, seconds_to_string


class User(UserMixin, db.Model):
    __tablename__ = "user_account"

    # Fields
    id = db.Column(UUID, primary_key=True)
    password = db.Column(db.LargeBinary, nullable=False)
    email_address = db.Column(db.String(256), nullable=False, unique=True, index=True)
    timezone = db.Column(db.String, nullable=False, server_default="UTC")
    entry_history = db.Column(db.Integer, nullable=False, server_default="12")
    tag_limit = db.Column(db.Integer, nullable=False, server_default="8")
    location_limit = db.Column(db.Integer, nullable=False, server_default="3")
    activated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    login_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    sunday = db.Column(db.Integer, nullable=False, server_default="0")
    monday = db.Column(db.Integer, nullable=False, server_default="0")
    tuesday = db.Column(db.Integer, nullable=False, server_default="0")
    wednesday = db.Column(db.Integer, nullable=False, server_default="0")
    thursday = db.Column(db.Integer, nullable=False, server_default="0")
    friday = db.Column(db.Integer, nullable=False, server_default="0")
    saturday = db.Column(db.Integer, nullable=False, server_default="0")
    default_tag_id = db.Column(UUID, nullable=True)
    default_location_id = db.Column(UUID, nullable=True)

    # Relationships
    events = db.relationship("Event", backref="user", lazy=True, passive_deletes=True)
    tags = db.relationship("Tag", backref="user", lazy=True, passive_deletes=True, order_by="asc(Tag.name)")
    locations = db.relationship(
        "Location",
        backref="user",
        lazy=True,
        passive_deletes=True,
        order_by="asc(Location.name)",
    )

    # Methods
    def __init__(self, password, email_address, timezone):
        self.id = str(uuid.uuid4())
        self.email_address = email_address.lower()
        self.timezone = timezone
        self.created_at = pytz.utc.localize(datetime.utcnow())
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
        current_app.logger.info(f"User {self.id} set password")

    def check_password(self, password):
        current_app.logger.info(f"User {self.id} password check")
        return bcrypt.checkpw(password.encode("UTF-8"), self.password)

    def generate_token(self, expires_in=600):
        current_app.logger.info(f"User {self.id} generated token")
        return jwt.encode(
            {"id": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])["id"]
        except jwt.PyJWTError:
            return
        return User.query.get(id)

    def schedule(self):
        """Returns the user schedule total in seconds"""
        return self.monday + self.tuesday + self.wednesday + self.thursday + self.friday + self.saturday + self.sunday

    def schedule_string(self):
        return seconds_to_string(self.schedule())

    def schedule_decimal(self):
        return seconds_to_decimal(self.schedule())


@login.user_loader
def load_user(id):
    return User.query.get(id)


class Event(db.Model):
    # Fields
    id = db.Column(UUID, primary_key=True)
    user_id = db.Column(
        UUID,
        db.ForeignKey("user_account.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tag_id = db.Column(UUID, db.ForeignKey("tag.id", ondelete="SET NULL"), nullable=True, index=True)
    location_id = db.Column(
        UUID,
        db.ForeignKey("location.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    started_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    ended_at = db.Column(db.DateTime(timezone=True), nullable=True)
    comment = db.Column(db.String(64), nullable=True)

    # Methods
    def __init__(self, user_id, started_at):
        self.id = str(uuid.uuid4())
        self.user_id = str(uuid.UUID(str(user_id), version=4))
        self.started_at = started_at

    def duration(self, end=None):
        """Returns the duration of an event in seconds"""
        if self.ended_at:
            return int((self.ended_at - self.started_at).total_seconds())
        elif end:
            return int((end - self.started_at).total_seconds())
        else:
            return 0

    def duration_string(self, end=None):
        return seconds_to_string(self.duration(end))

    def duration_decimal(self, end=None):
        return seconds_to_decimal(self.duration(end))


class Tag(db.Model):
    # Fields
    id = db.Column(UUID, primary_key=True)
    user_id = db.Column(
        UUID,
        db.ForeignKey("user_account.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Relationships
    events = db.relationship(
        "Event",
        backref="tag",
        lazy=True,
        passive_deletes=True,
        order_by="desc(Event.started_at)",
    )

    # Methods
    def __init__(self, user_id, name):
        self.id = str(uuid.uuid4())
        self.user_id = str(uuid.UUID(str(user_id), version=4))
        self.name = name
        self.created_at = pytz.utc.localize(datetime.utcnow())


class Location(db.Model):
    # Fields
    id = db.Column(UUID, primary_key=True)
    user_id = db.Column(
        UUID,
        db.ForeignKey("user_account.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Relationships
    events = db.relationship(
        "Event",
        backref="location",
        lazy=True,
        passive_deletes=True,
        order_by="desc(Event.started_at)",
    )

    # Methods
    def __init__(self, user_id, name):
        self.id = str(uuid.uuid4())
        self.user_id = str(uuid.UUID(str(user_id), version=4))
        self.name = name.strip()
        self.created_at = pytz.utc.localize(datetime.utcnow())
