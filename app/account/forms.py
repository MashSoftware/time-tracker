import pytz
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, TimeField
from wtforms.validators import Email, EqualTo, InputRequired, Length, ValidationError

from app.models import User


class AccountForm(FlaskForm):
    tz_tuples = []
    for tz in pytz.common_timezones:
        tz_tuples.append((tz, tz.replace("_", " ")))

    email_address = StringField(
        "Email address",
        validators=[
            InputRequired(message="Enter an email address"),
            Email(granular_message=True, check_deliverability=True),
            Length(max=256, message="Email address must be 256 characters or fewer"),
        ],
        description="We'll never share your email with anyone else.",
    )
    timezone = SelectField(
        "Timezone",
        validators=[InputRequired(message="Select a timezone")],
        choices=tz_tuples,
        default="Europe/London",
    )

    def validate_email_address(self, email_address):
        if email_address.data != current_user.email_address:
            user = User.query.filter_by(email_address=email_address.data).first()
            if user is not None:
                raise ValidationError("Email address is already in use")


class PasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current password",
        validators=[
            InputRequired(message="Enter your current password"),
            Length(
                min=8,
                max=72,
                message="Current password must be between 8 and 72 characters",
            ),
        ],
    )
    new_password = PasswordField(
        "New password",
        validators=[
            InputRequired(message="Enter a new password"),
            Length(
                min=8,
                max=72,
                message="New password must be between 8 and 72 characters",
            ),
        ],
        description="Must be between 8 and 72 characters",
    )
    confirm_password = PasswordField(
        "Confirm new password",
        validators=[
            InputRequired(message="Confirm your new password"),
            EqualTo("new_password", message="Passwords must match."),
        ],
    )

    def validate_new_password(self, new_password):
        if new_password.data == self.current_password.data:
            raise ValidationError("New password must be different to current password")


class ScheduleForm(FlaskForm):
    monday = TimeField("Monday", validators=[InputRequired(message="Enter Monday's time")])
    tuesday = TimeField("Tuesday", validators=[InputRequired(message="Enter Tuesday's time")])
    wednesday = TimeField("Wednesday", validators=[InputRequired(message="Enter Wednesday's time")])
    thursday = TimeField("Thursday", validators=[InputRequired(message="Enter Thursday's time")])
    friday = TimeField("Friday", validators=[InputRequired(message="Enter Friday's time")])
    saturday = TimeField("Saturday", validators=[InputRequired(message="Enter Saturday's time")])
    sunday = TimeField("Sunday", validators=[InputRequired(message="Enter Sunday's time")])
