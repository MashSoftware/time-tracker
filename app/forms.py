from datetime import datetime

import pytz
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, PasswordField, SelectField,
                     StringField)
from wtforms.validators import (Email, EqualTo, InputRequired, Length,
                                Optional, ValidationError)

from app.models import User


class SignupForm(FlaskForm):
    tz_tuples = []
    for tz in pytz.common_timezones:
        tz_tuples.append((tz, tz))

    email_address = StringField('Email address', validators=[InputRequired(message="Email address is required"), Email()],
                                description="We'll never share your email with anyone else.")
    password = PasswordField('Password', validators=[InputRequired(message="Password is required"), Length(min=8, max=72, message="Password must be between 8 and 72 characters")],
                             description="Must be between 8 and 72 characters.")
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(
        message="Confirm your password"), EqualTo('password', message="Passwords must match.")])
    timezone = SelectField('Timezone', validators=[InputRequired(message="Timezone is required")],
                           choices=tz_tuples,
                           default='Europe/London')

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user is not None:
            raise ValidationError('Email address is already in use, please log in')


class LoginForm(FlaskForm):
    email_address = StringField('Email address', validators=[
                                InputRequired(message="Email address is required"), Email()])
    password = PasswordField('Password', validators=[InputRequired(message="Password is required"), Length(min=8, max=72, message="Password must be between 8 and 72 characters")],
                             description="Must be between 8 and 72 characters")
    remember_me = BooleanField('Remember me')


class PasswordForm(FlaskForm):
    current_password = PasswordField('Current password', validators=[
                                     InputRequired(message="Current password is required"), Length(min=8, max=72, message="Current password must be between 8 and 72 characters")])
    new_password = PasswordField('New password', validators=[InputRequired(message="New password is required"), Length(min=8, max=72, message="New password must be between 8 and 72 characters")],
                                 description="Must be between 8 and 72 characters")
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(
        message="Confirm your password"), EqualTo('new_password', message="Passwords must match.")])

    def validate_new_password(self, new_password):
        if new_password.data == self.current_password.data:
            raise ValidationError('New password must be different to current password')


class AccountForm(FlaskForm):
    tz_tuples = []
    for tz in pytz.common_timezones:
        tz_tuples.append((tz, tz))

    email_address = StringField('Email address', validators=[InputRequired(message="Email address is required"), Email()],
                                description="We'll never share your email with anyone else.")
    timezone = SelectField('Timezone', validators=[InputRequired(message="Timezone is required")],
                           choices=tz_tuples,
                           default='Europe/London')

    def validate_email_address(self, email_address):
        if email_address.data != current_user.email_address:
            user = User.query.filter_by(email_address=email_address.data).first()
            if user is not None:
                raise ValidationError('Email address is already in use')


class EventForm(FlaskForm):
    started_at = DateTimeField(
        'Start',
        format='%d/%m/%Y %H:%M:%S',
        validators=[InputRequired(message="Started is required")],
        description="Must be in the format dd/mm/yyyy hh:mm:ss")
    ended_at = DateTimeField(
        'Stop',
        format='%d/%m/%Y %H:%M:%S',
        validators=[Optional()],
        description="Must be in the format dd/mm/yyyy hh:mm:ss")

    def validate_started_at(self, started_at):
        if pytz.timezone(current_user.timezone).localize(started_at.data) > pytz.utc.localize(datetime.utcnow()):
            raise ValidationError('Start must be in the past')

    def validate_ended_at(self, ended_at):
        if ended_at.data <= self.started_at.data:
            raise ValidationError('Stop must be after start')

        if pytz.timezone(current_user.timezone).localize(ended_at.data) > pytz.utc.localize(datetime.utcnow()):
            raise ValidationError('Stop must be in the past')
