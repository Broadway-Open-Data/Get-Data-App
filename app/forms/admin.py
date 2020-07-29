from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, FormField
# from wtforms.fields import FormField, FieldList
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length, Optional



class AuthenticateUsersForm(FlaskForm):
    """All of the fields as one."""

    class allFields_(FlaskForm):
        userEmail = StringField('Email', validators=[Length(min=6), Email(message='Enter a valid email.'),DataRequired()])
        approve = BooleanField('Authenticate')

    allFields = FormField(allFields_)
    submit = SubmitField('Submit')
