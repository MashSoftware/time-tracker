import pytz
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length, ValidationError

from app.models import User


class SignupForm(FlaskForm):
    tz_tuples = []
    for tz in pytz.common_timezones:
        tz_tuples.append((tz, tz.replace("_", " ")))

    email_address = StringField(
        "Email address",
        validators=[
            InputRequired(message="Email address is required"),
            Email(granular_message=True, check_deliverability=True),
            Length(max=256, message="Email address must be less than 256 characters"),
        ],
        description="We'll never share your email with anyone else.",
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Password is required"),
            Length(min=8, max=72, message="Password must be between 8 and 72 characters"),
        ],
        description="Must be between 8 and 72 characters.",
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            InputRequired(message="Confirm your password"),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    timezone = SelectField(
        "Timezone",
        validators=[InputRequired(message="Timezone is required")],
        choices=tz_tuples,
        default="Europe/London",
    )

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user is not None:
            raise ValidationError("Email address is already in use, please log in")


class LoginForm(FlaskForm):
    email_address = StringField(
        "Email address",
        validators=[
            InputRequired(message="Email address is required"),
            Email(granular_message=True, check_deliverability=True),
            Length(max=256, message="Email address must be less than 256 characters"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Password is required"),
            Length(min=8, max=72, message="Password must be between 8 and 72 characters"),
        ],
        description="Must be between 8 and 72 characters",
    )
    remember_me = BooleanField("Remember me")


class TokenRequestForm(FlaskForm):
    email_address = StringField(
        "Email address",
        validators=[
            InputRequired(message="Email address is required"),
            Email(granular_message=True, check_deliverability=True),
            Length(max=256, message="Email address must be less than 256 characters"),
        ],
    )


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(
        "New password",
        validators=[
            InputRequired(message="New password is required"),
            Length(min=8, max=72, message="New password must be between 8 and 72 characters",),
        ],
        description="Must be between 8 and 72 characters",
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            InputRequired(message="Confirm your password"),
            EqualTo("new_password", message="Passwords must match."),
        ],
    )
