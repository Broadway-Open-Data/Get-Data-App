from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, FormField
# from wtforms.fields import FormField, FieldList
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length, Optional

import sys
sys.path.append(".")
# Import as if you're one directory up
from forms.custom_validator import NotEqualTo


class AuthenticateUsersForm(FlaskForm):
    """All of the fields as one."""

    class allFields_(FlaskForm):
        userEmail = StringField('Email', validators=[Length(min=6), Email(message='Enter a valid email.'),DataRequired()])
        approve = BooleanField('Approve', validators=[NotEqualTo('un_approve')])
        un_approve = BooleanField('Unapprove', validators=[NotEqualTo('approve')])

    allFields = FormField(allFields_)
    submit = SubmitField('Submit')
