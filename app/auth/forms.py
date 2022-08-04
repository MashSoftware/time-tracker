import pytz
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional, ValidationError

from app.models import User


class SignupForm(FlaskForm):
    tz_tuples = []
    for tz in pytz.common_timezones:
        tz_tuples.append((tz, tz.replace("_", " ")))

    email_address = StringField(
        "Email address",
        validators=[
            InputRequired(message="Enter your email address"),
            Email(granular_message=True, check_deliverability=True),
            Length(max=256, message="Email address must be 256 characters or fewer"),
        ],
        description="We'll never share your email with anyone else.",
    )
    password = PasswordField(
        "Create a password",
        validators=[
            InputRequired(message="Enter a password"),
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
        validators=[InputRequired(message="Select a timezone")],
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
            InputRequired(message="Enter an email address"),
            Email(granular_message=True, check_deliverability=True),
            Length(max=256, message="Email address must be 256 characters or fewer"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Enter a password"),
            Length(min=8, max=72, message="Password must be between 8 and 72 characters"),
        ],
        description="Must be between 8 and 72 characters.",
    )
    remember_me = BooleanField("Remember me", validators=[Optional()])


class TokenRequestForm(FlaskForm):
    email_address = StringField(
        "Email address",
        validators=[
            InputRequired(message="Enter an email address"),
            Email(granular_message=True, check_deliverability=True),
            Length(max=256, message="Email address must be 256 characters or fewer"),
        ],
    )


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(
        "Create a new password",
        validators=[
            InputRequired(message="Enter a new password"),
            Length(
                min=8,
                max=72,
                message="New password must be between 8 and 72 characters",
            ),
        ],
        description="Must be between 8 and 72 characters.",
    )
    confirm_password = PasswordField(
        "Confirm new password",
        validators=[
            InputRequired(message="Confirm your new password"),
            EqualTo("new_password", message="Passwords must match."),
        ],
    )
