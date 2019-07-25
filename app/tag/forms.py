from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length


class TagForm(FlaskForm):
    description = StringField(
        'Description',
        validators=[
            InputRequired(message="Description is required"),
            Length(max=64, message="Description must be less than 64 characters")
        ])
