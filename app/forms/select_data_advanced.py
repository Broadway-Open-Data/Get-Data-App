from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, IntegerField, SubmitField
from wtforms.fields import FormField, FieldList
from wtforms.validators import DataRequired

import datetime

# Make a form
class Params(FlaskForm):
    query = StringField(label='sql Query', default="select * from shows;", validators=[DataRequired()])
    API_KEY = StringField(label='API_KEY', validators=[DataRequired()])

class sqlForm(FlaskForm):
    """All of the fields as one."""
    allFields = FormField(Params)
    submit = SubmitField('Submit')
