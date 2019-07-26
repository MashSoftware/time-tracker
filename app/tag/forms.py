from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length, ValidationError


class TagForm(FlaskForm):
    description = StringField(
        'Description',
        validators=[
            InputRequired(message="Description is required"),
            Length(max=64, message="Description must be less than 64 characters")
        ])

    def validate_description(self, description):
        for tag in current_user.tags:
            if tag.description == description.data:
                raise ValidationError('You have already created a tag with that description')
