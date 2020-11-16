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
    shows_title = StringField(label='Show Title (fuzzy)', validators=[Optional(strip_whitespace=True)])
    # Show genre
    musicals = BooleanField(label="Musicals", default=True, render_kw ={'checked': ''})
    plays = BooleanField(label="Plays", default=True, render_kw ={'checked':''})
    other_show_genre = BooleanField(label="Other", default=False, render_kw ={'unchecked':''})

    # Production Type
    originals = BooleanField(label="Originals", default=True, render_kw ={'checked':''})
    revivals = BooleanField(label="Revivals", default=True, render_kw ={'checked':''})
    other_production_type = BooleanField(label="Others", default=False, render_kw ={'unchecked':''})

    # Theatre Info
    theatre_info = BooleanField(label="Theatre Info", default=False, render_kw ={'unchecked':''})
    theatreName = StringField(label="Theatre Name (fuzzy)")


    # Date Range
    # If we add these as dates, we need js to properly format them as the user inputs them...
    # startDate = DateField(label="Start Date", description="this is a description", format='%Y-%m-%d', default=datetime.datetime(1850,1,1), validators=[DataRequired()])
    # endDate = DateField(label="End Date",format='%Y-%m-%d', default=datetime.datetime(2020,6,1))
    shows_year_from = IntegerField(label="Show Year From", default=1990, validators=[DataRequired()])
    shows_year_to = IntegerField(label="Show Year To",default=2020, validators=[DataRequired()])


    # People?
    person_name = StringField(label='Person Name', validators=[Optional(strip_whitespace=True)])


    shows_title = StringField(label='Show Title', validators=[Optional(strip_whitespace=True)])





# ==================================================================================================
