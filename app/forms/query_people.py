from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, IntegerField, SubmitField, SelectField
from wtforms.fields import FormField, FieldList
from wtforms.validators import DataRequired, Length, Optional

# import databases
from sqlalchemy.orm import load_only
from databases.models.broadway import Person, Show, ShowsRolesLink

import datetime

# Make a form
class Query(FlaskForm):
    person_f_name = StringField(label='First Name', validators=[Optional(strip_whitespace=True)])
    person_m_name = StringField(label='Middle Name', validators=[Optional(strip_whitespace=True)])
    person_l_name = StringField(label='Last Name', validators=[Optional(strip_whitespace=True)])
    shows_title = StringField(label='Show Title', validators=[Optional(strip_whitespace=True)])
    shows_year = StringField(label='Show Year', validators=[Optional(strip_whitespace=True)])
    role_name = StringField(label='Role Name', validators=[Optional(strip_whitespace=True)])
