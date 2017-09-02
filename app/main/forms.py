from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length


class SearchByUsername(FlaskForm):
    USERNAME = StringField('Username:',validators=[DataRequired()])
    submit = SubmitField('Search')

class SearchByPassword(FlaskForm):
    PASSWORD = StringField('Password:',validators=[DataRequired()])
    submit = SubmitField('Search')

class SearchByEmail(FlaskForm):
    EMAIL = StringField('Email:',validators=[DataRequired()])
    submit = SubmitField('Search')