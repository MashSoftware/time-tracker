from datetime import datetime

import pytz
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import DateField, RadioField, TextAreaField, TimeField
from wtforms.validators import InputRequired, Length, Optional, ValidationError


class EventForm(FlaskForm):
    started_at_date = DateField("Start date", validators=[InputRequired(message="Start date is required")])
    started_at_time = TimeField("Start time", validators=[InputRequired(message="Start time is required")])
    ended_at_date = DateField("Stop date", validators=[Optional()])
    ended_at_time = TimeField("Stop time", validators=[Optional()])
    tag = RadioField("Tag", validators=[InputRequired(message="Tag is required")])
    comment = TextAreaField(
        "Comment",
        validators=[Optional(), Length(max=64, message="Comment must be less than 64 characters")],
        description="Must be less than 64 characters.",
    )

    def validate_started_at_date(self, started_at_date):
        current_localised_date = (
            pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone(current_user.timezone)).date()
        )
        if started_at_date.data > current_localised_date:
            raise ValidationError("Start date must be today or in the past")

    def validate_started_at_time(self, started_at_time):
        current_localised_datetime = pytz.utc.localize(datetime.utcnow()).astimezone(
            pytz.timezone(current_user.timezone)
        )

        try:
            started_at = datetime(
                self.started_at_date.data.year,
                self.started_at_date.data.month,
                self.started_at_date.data.day,
                started_at_time.data.hour,
                started_at_time.data.minute,
                started_at_time.data.second,
            )
        except AttributeError:
            raise ValidationError("Start date is required")

        if pytz.timezone(current_user.timezone).localize(started_at) > current_localised_datetime:
            raise ValidationError("Start time must be now or in the past")

    def validate_ended_at_date(self, ended_at_date):
        if self.started_at_date.data is None:
            raise ValidationError("Start date and time are also required")

        if ended_at_date.data < self.started_at_date.data:
            raise ValidationError("Stop date must be the same as or after start date")

        current_localised_date = (
            pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone(current_user.timezone)).date()
        )

        if ended_at_date.data > current_localised_date:
            raise ValidationError("Stop date must be today or in the past")

    def validate_ended_at_time(self, ended_at_time):
        try:
            started_at = datetime(
                self.started_at_date.data.year,
                self.started_at_date.data.month,
                self.started_at_date.data.day,
                self.started_at_time.data.hour,
                self.started_at_time.data.minute,
                self.started_at_time.data.second,
            )
        except AttributeError:
            raise ValidationError("Start date and time are also required")

        try:
            ended_at = datetime(
                self.ended_at_date.data.year,
                self.ended_at_date.data.month,
                self.ended_at_date.data.day,
                ended_at_time.data.hour,
                ended_at_time.data.minute,
                ended_at_time.data.second,
            )
        except AttributeError:
            raise ValidationError("Stop date is required")

        if ended_at < started_at:
            raise ValidationError("Stop time must be after start time")

        current_localised_datetime = pytz.utc.localize(datetime.utcnow()).astimezone(
            pytz.timezone(current_user.timezone)
        )

        if pytz.timezone(current_user.timezone).localize(ended_at) > current_localised_datetime:
            raise ValidationError("Stop time must be now or in the past")
