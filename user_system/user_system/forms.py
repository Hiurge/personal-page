from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, IntegerField, TextField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional

class SignupForm(Form):
	name = StringField('User name', validators=[DataRequired()])
	email = StringField('Email', validators=[Email(), DataRequired()] )
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')]) #validators: Length(min=6)
	confirm_password = PasswordField('Confirm password')
	info = StringField('Additional informations', validators=[Optional()])
	submit = SubmitField('Singup')

class LoginForm(Form):
	name = StringField('User name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')