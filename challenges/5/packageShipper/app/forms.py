from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class ShippingForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(max=100)])
    package_type = SelectField('Package Type', choices=[
        ('envelope', 'Envelope - FREE'),
        ('small_box', 'Small Box - FREE'),
        ('medium_box', 'Medium Box - FREE'),
        ('large_box', 'Large Box - FREE')
    ], validators=[DataRequired()])
    destination = StringField('Destination Address', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Purchase Label')