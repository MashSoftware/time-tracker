from datetime import datetime

import pytz
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import DateTimeField, RadioField
from wtforms.validators import InputRequired, Optional, ValidationError


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
