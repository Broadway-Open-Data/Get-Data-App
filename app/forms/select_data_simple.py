from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, IntegerField, SelectField, SubmitField
from wtforms.fields import FormField, FieldList
from wtforms.validators import  DataRequired

import datetime
import re

# Make a form
class showInfo(FlaskForm):
    title = StringField(label='Show Name (fuzzy)')
    keyword = StringField(label='Keyword (fuzzy)')
    showId = IntegerField(label='ShowId')

class showGenre(FlaskForm):
    musicals = BooleanField(label="Musicals", default=True, render_kw ={'checked': ''})
    plays = BooleanField(label="Plays", default=True, render_kw ={'checked':''})
    other_show_genre = BooleanField(label="Other", default=False, render_kw ={'unchecked':''})

class productionType(FlaskForm):
    originals = BooleanField(label="Originals", default=True, render_kw ={'checked':''})
    revivals = BooleanField(label="Revivals", default=True, render_kw ={'checked':''})
    other_production_type = BooleanField(label="Others", default=False, render_kw ={'unchecked':''})

class theatreInfo(FlaskForm):
    theatre_info = BooleanField(label="Theatre Info", default=False, render_kw ={'unchecked':''})
    # theatreName = StringField(label="Theatre Name (fuzzy)")
    # theatreId = IntegerField(label="Theatre ID")

class dateRange(FlaskForm):
    # startDate = DateField(label="Start Date", description="this is a description", format='%Y-%m-%d', default=datetime.datetime(1850,1,1), validators=[DataRequired()])
    # endDate = DateField(label="End Date",format='%Y-%m-%d', default=datetime.datetime(2020,6,1))
    startYear = IntegerField(label="Start Year", default=1990, validators=[DataRequired()])
    endYear = IntegerField(label="End Year",default=2020, validators=[DataRequired()])


class summarizedFields(FlaskForm):
    """Some description."""
    # showInfoSum = FormField(showInfo, label="Show Info", description="hey", separator="-")
    showGenreSum = FormField(showGenre, label="Show Genre", description="hey")
    productionTypeSum = FormField(productionType, label="Production Type", description="hey")
    theatreInfoSum = FormField(theatreInfo, label="Theatre Info",)
    dateRangeSum = FormField(dateRange, label="Date Range")



# The acrtual form!
class dataForm(FlaskForm):
    """All of the fields as one."""
    allFields = FormField(summarizedFields)
    submit = SubmitField('Submit')
