from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import Email, InputRequired, Length


class LoginForm(FlaskForm):
    email_address = StringField('Email address', validators=[
                                InputRequired(message="Email address is required"), Email()])
    password = PasswordField('Password', validators=[InputRequired(message="Password is required"), Length(min=8, max=72, message="Password must be between 8 and 72 characters")],
                             description="Must be between 8 and 72 characters")
    remember_me = BooleanField('Remember me')
