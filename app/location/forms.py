from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField
from wtforms.validators import InputRequired, Length, ValidationError


class LocationForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            InputRequired(message="Enter a name"),
            Length(max=64, message="Name must be 64 characters or fewer"),
        ],
        description="Must be 64 characters or fewer.",
    )

    def validate_name(self, name):
        if len(name.data.strip()) == 0:
            raise ValidationError("Enter a name")

        for location in current_user.locations:
            if location.name == name.data.strip():
                raise ValidationError("You have already created a location with that name")


class DefaultForm(FlaskForm):
    location = RadioField(
        "Default location",
        validators=[InputRequired(message="Select a default location")],
        choices=[("None", "None")],
        default="None",
        description="This location will be used on all new time entries.",
    )
