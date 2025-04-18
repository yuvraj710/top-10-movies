"""
forms.py – Flask-WTF forms for the Top 10 Movies app.

Defines forms for editing movie ratings and reviews with validation.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class EditForm(FlaskForm):
    """
    Form used for editing a movie's rating and review.
    """
    rating = FloatField("Your Rating (0–10)", validators=[
        DataRequired(),
        NumberRange(min=0, max=10, message="Rating must be between 0 and 10.")
    ])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Submit")
