from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from application.models import SocialUser


class LoginForm(FlaskForm):
    username = StringField(label="User name ", validators=[DataRequired()])
    password = PasswordField(label="Password ", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")

