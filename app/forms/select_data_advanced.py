from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, IntegerField, SubmitField, SelectField
from wtforms.fields import FormField, FieldList
from wtforms.validators import DataRequired, Length

import datetime

# Make a form
class Params(FlaskForm):
    query = StringField(label='sql Query', default="select * from shows;", validators=[DataRequired()])
    API_KEY = StringField(label='API_KEY', validators=[DataRequired()])
    detail_level = IntegerField(label='Data Summary Detail Level', default=1, validators=[DataRequired()])
    
class sqlForm(FlaskForm):
    """All of the fields as one."""
    allFields = FormField(Params)
    submit = SubmitField('Submit')
