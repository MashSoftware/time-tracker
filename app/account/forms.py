import pytz
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, TimeField
from wtforms.validators import (Email, EqualTo, InputRequired, Length,
                                ValidationError)

from app.models import User


class AccountForm(FlaskForm):
    tz_tuples = []
    for tz in pytz.common_timezones:
        tz_tuples.append((tz, tz.replace("_", " ")))

    email_address = StringField(
        'Email address',
        validators=[
            InputRequired(message="Email address is required"),
            Email(),
            Length(max=256, message="Email address must be less than 256 characters")],
        description="We'll never share your email with anyone else.")
    timezone = SelectField(
        'Timezone',
        validators=[
            InputRequired(message="Timezone is required")],
        choices=tz_tuples,
        default='Europe/London')

    def validate_email_address(self, email_address):
        if email_address.data != current_user.email_address:
            user = User.query.filter_by(email_address=email_address.data).first()
            if user is not None:
                raise ValidationError('Email address is already in use')


class PasswordForm(FlaskForm):
    current_password = PasswordField(
        'Current password',
        validators=[
            InputRequired(message="Current password is required"),
            Length(min=8, max=72, message="Current password must be between 8 and 72 characters")])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(message="New password is required"),
            Length(min=8, max=72, message="New password must be between 8 and 72 characters")],
        description="Must be between 8 and 72 characters")
    confirm_password = PasswordField(
        'Confirm password',
        validators=[
            InputRequired(message="Confirm your password"),
            EqualTo('new_password', message="Passwords must match.")])

    def validate_new_password(self, new_password):
        if new_password.data == self.current_password.data:
            raise ValidationError('New password must be different to current password')


class ScheduleForm(FlaskForm):
    sunday = TimeField('Sunday', validators=[InputRequired(message="Sunday is required")])
    monday = TimeField('Monday', validators=[InputRequired(message="Monday is required")])
    tuesday = TimeField('Tuesday', validators=[InputRequired(message="Tuesday is required")])
    wednesday = TimeField('Wednesday', validators=[InputRequired(message="Wednesday is required")])
    thursday = TimeField('Thursday', validators=[InputRequired(message="Thursday is required")])
    friday = TimeField('Friday', validators=[InputRequired(message="Friday is required")])
    saturday = TimeField('Saturday', validators=[InputRequired(message="Saturday is required")])
