from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, IntegerField, SubmitField
from wtforms.fields import FormField, FieldList
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """All of the fields as one."""
    email = StringField(label='user name', default="user_1", validators=[DataRequired()])
    password = StringField(label='password', default="foo", validators=[DataRequired()])
    submit = SubmitField('Submit')
