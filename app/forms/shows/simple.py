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
    # Show Info
    show_title_ADVANCED = StringField(label='Show Title (fuzzy)', validators=[Optional(strip_whitespace=True)])
    # Show genre
    show_genre_musical = BooleanField(label="Musicals", default=True, render_kw = dict(unchecked=''))
    show_genre_play = BooleanField(label="Plays", default=True, render_kw = dict(unchecked=''))
    show_genre_other = BooleanField(label="Other", default=False, render_kw = dict(unchecked=''))

    # Production Type
    show_type_original = BooleanField(label="Originals", default=True, render_kw = dict(checked=''))
    show_type_revival = BooleanField(label="Revivals", default=True, render_kw = dict(checked=''))
    show_type_other = BooleanField(label="Others", default=False, render_kw = dict(unchecked=''))

    # Theatre Info
    theatre_info = BooleanField(label="Theatre Info", description="include theatre info?", default=False, render_kw = dict(unchecked=''))
    theatre_name_ADVANCED = StringField(label="Theatre Name (fuzzy)")


    # Date Range
    # If we add these as dates, we need js to properly format them as the user inputs them...
    # startDate = DateField(label="Start Date", description="this is a description", format='%Y-%m-%d', default=datetime.datetime(1850,1,1), validators=[DataRequired()])
    # endDate = DateField(label="End Date",format='%Y-%m-%d', default=datetime.datetime(2020,6,1))
    show_year_from = IntegerField(label="Show Year From", default=1990, validators=[DataRequired()])
    show_year_to = IntegerField(label="Show Year To",default=2020, validators=[DataRequired()])


    # People
    person_name_ADVANCED = StringField(label='Person Name', validators=[Optional(strip_whitespace=True)])




# ==================================================================================================
