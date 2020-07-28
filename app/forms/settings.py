from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, FormField
# from wtforms.fields import FormField, FieldList
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length, Optional



class ChangePasswordForm(FlaskForm):
    """All of the fields as one."""

    class allFields_(FlaskForm):
        new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
        confirm = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])

    allFields = FormField(allFields_)
    submit = SubmitField('Submit')



class UpdateProfileForm(FlaskForm):
    """All of the fields as one."""

    class allFields_(FlaskForm):
        email = StringField('Email Address', validators=[Length(min=6), Email(message='Enter a valid email.'),DataRequired()])
        website = StringField('Website',validators=[Optional()])
        instagram = StringField('Instagram Handle', validators=[Optional()])

    allFields = FormField(allFields_)
    submit = SubmitField('Submit')

# class ResetPasswordForm(FlaskForm):
#     """Allow a user to reset their password"""
