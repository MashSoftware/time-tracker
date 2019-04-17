import bcrypt
from sqlalchemy.dialects.postgresql import UUID

from app import db


class User(db.Model):
    __tablename__ = 'user_account'

    # Fields
    user_id = db.Column(UUID, primary_key=True)
    password = db.Column(db.Binary, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    email_address = db.Column(db.String, nullable=False, unique=True, index=True)
    login_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Methods
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('UTF-8'), self.password)
