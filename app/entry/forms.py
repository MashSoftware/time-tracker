from datetime import datetime

import pytz
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import DateField, RadioField, TimeField
from wtforms.validators import InputRequired, Optional, ValidationError


class EventForm(FlaskForm):
    started_at_date = DateField(
        'Start date',
        validators=[InputRequired(message="Start date is required")])
    started_at_time = TimeField(
        'Start time',
        validators=[InputRequired(message="Start time is required")])
    ended_at_date = DateField(
        'Stop date',
        validators=[Optional()])
    ended_at_time = TimeField(
        'Stop time',
        validators=[Optional()])
    tag = RadioField(
        'Tag',
        validators=[InputRequired(message="Tag is required")])

    def validate_started_at_date(self, started_at_date):
        started_at = datetime(
            started_at_date.data.year,
            started_at_date.data.month,
            started_at_date.data.day,
            self.started_at_time.data.hour,
            self.started_at_time.data.minute,
            self.started_at_time.data.second
        )
        if pytz.timezone(current_user.timezone).localize(started_at) > pytz.utc.localize(datetime.utcnow()):
            raise ValidationError('Start must be in the past')

    def validate_started_at_time(self, started_at_time):
        started_at = datetime(
            self.started_at_date.data.year,
            self.started_at_date.data.month,
            self.started_at_date.data.day,
            started_at_time.data.hour,
            started_at_time.data.minute,
            started_at_time.data.second
        )
        if pytz.timezone(current_user.timezone).localize(started_at) > pytz.utc.localize(datetime.utcnow()):
            raise ValidationError('Start must be in the past')

    def validate_ended_at_date(self, ended_at_date):
        if ended_at_date.data <= self.started_at_date.data:
            raise ValidationError('Stop must be after start')

        if pytz.timezone(current_user.timezone).localize(ended_at_date.data) > pytz.utc.localize(datetime.utcnow()):
            raise ValidationError('Stop must be in the past')
