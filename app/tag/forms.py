from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length, ValidationError


class TagForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            InputRequired(message="Name is required"),
            Length(max=64, message="Name must be less than 64 characters"),
        ],
        description="Must be less than 64 characters.",
    )

    def validate_name(self, name):
        if len(name.data.strip()) == 0:
            name.data = name.data.strip()
            raise ValidationError("Name is required")

        for tag in current_user.tags:
            if tag.name == name.data.strip():
                name.data = name.data.strip()
                raise ValidationError("You have already created a tag with that name")
