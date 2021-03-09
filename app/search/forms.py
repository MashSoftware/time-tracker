from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    query = StringField("Search", validators=[InputRequired(message="Enter a search query")])
