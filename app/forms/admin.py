from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, FormField, SelectField
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

class CreateRoles(FlaskForm):
        """Allows creation of roles."""

        class allFields_(FlaskForm):
            roleName = StringField('Role Name', validators=[Length(min=4, message="Role name must be at;east 4 characters"), DataRequired()])
            permissions = SelectField('Permissions', choices=[(x,x) for x in ["admin", "data-admin", "data-editor", "user", "user-beta"]], validators=[DataRequired()])
            create_role = SelectField('Create Role', choices=[(x,x) for x in ["Create", "Delete"]], validators=[DataRequired()])


        allFields = FormField(allFields_)
        submit = SubmitField('Submit')

class AssignRoles(FlaskForm):
        """Allows assignment of roles etc."""
        class allFields_(FlaskForm):
            # Ideally, can query the currenr role names...
            roleName = StringField('Role Name', validators=[Length(min=4, message="Role name must be at;east 4 characters"), DataRequired()])
            userEmail = StringField('Email', validators=[Length(min=6), Email(message='Enter a valid email.'),DataRequired()])
            assign = SelectField('Assign', choices=[(x,x) for x in ["Assign", "Unassign"]], validators=[DataRequired()])

        allFields = FormField(allFields_)
        submit = SubmitField('Submit')
