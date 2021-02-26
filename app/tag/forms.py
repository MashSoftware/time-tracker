from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length, ValidationError


class TagForm(FlaskForm):
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

        for tag in current_user.tags:
            if tag.name == name.data.strip():
                raise ValidationError("You have already created a tag with that name")
