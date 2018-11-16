from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User

VALID_SUFFIX = ["columbia.edu", "barnard.edu"]


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64), Email()])
    submit = SubmitField("Submit")


class ChangePasswordForm(FlaskForm):
    message = "Passwords must match"
    password = PasswordField('New Password',
                             validators=[DataRequired(),
                                         EqualTo('password2',
                                                 message=message)])

    password2 = PasswordField('Retype your password',
                              validators=[DataRequired()])
    submit = SubmitField("Change Password")


class RegistrationForm(FlaskForm):
    email = StringField(
        'Email', validators=[
            DataRequired(), Length(
                1, 64), Email()])
    uni = StringField(
        'UNI', validators=[
            DataRequired(), Length(1, 15)])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo(
                'password2',
                message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        email = field.data
        print(email)
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
        elif email[-12:] != VALID_SUFFIX[0] and email[-11:] != VALID_SUFFIX[1]:
            email_err = "Email address need to be columbia.edu or barndard.edu"
            raise ValidationError(email_err)
