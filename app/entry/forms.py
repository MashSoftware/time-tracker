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

    def validate_started_at(self, started_at):
        if pytz.timezone(current_user.timezone).localize(started_at.data) > pytz.utc.localize(datetime.utcnow()):
            raise ValidationError('Start must be in the past')

    def validate_ended_at(self, ended_at):
        if ended_at.data <= self.started_at.data:
            raise ValidationError('Stop must be after start')

        if pytz.timezone(current_user.timezone).localize(ended_at.data) > pytz.utc.localize(datetime.utcnow()):
            raise ValidationError('Stop must be in the past')
