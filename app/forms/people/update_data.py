from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, IntegerField, SubmitField, SelectField
# from wtforms.fields import FormField, FieldList
from wtforms.validators import DataRequired, Length, Optional
#
# # import databases
# from databases.models.broadway import Person, Show, ShowsRolesLink
#
# import datetime

# Make a form
class UpdateDataForm(FlaskForm):
    person_id = IntegerField(label='Person id ("id")', validators=[DataRequired()])
    gender_identity = StringField(label='Gender Identity', validators=[Optional(strip_whitespace=True)])
    racial_identities = StringField(label='Racial Identities (comma seperated)', validators=[Optional(strip_whitespace=True)])
