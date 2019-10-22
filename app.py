from flask import Flask, render_template, flash, redirect, request, url_for, session
from flask_login import LoginManager, UserMixin
from flask_login import login_required, logout_user, current_user, login_user

from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, IntegerField, TextField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional

from werkzeug.security import generate_password_hash, check_password_hash

import psycopg2

import collections
import datetime
import os

from db import UsersTable, PostsTable, CommentsTable

app = Flask(__name__)
app.config.from_object(__name__) 
app.config['SECRET_KEY'] = os.urandom(16)
app.config['SECRET_DEBUG'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=10)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
UDB = UsersTable(credentials)
PDB = PostsTable(credentials)
CDB = CommentsTable(credentials)
for table in [UDB, PDB, CDB]:
	table.create_table()

def time_now():
	return datetime.datetime.now(datetime.timezone.utc)

class User(UserMixin):
	def __init__(self, user_id):
		self.user_id = user_id
	def get_id(self):
		return self.user_id

class SignupForm(Form):
	name = StringField('Name', validators=[DataRequired()])
	email = StringField('Email', validators=[Email(), DataRequired()] )
	password = PasswordField('Password', validators=[DataRequired(), Length(min=1), EqualTo('confirm_password')], default='a')
	confirm_password = PasswordField('Confirm password', default='a')
	info = StringField('Informations', validators=[Optional()])
	submit = SubmitField('Singup')

class LoginForm(Form):
	name = StringField('Name', validators=[DataRequired()], default='a')
	password = PasswordField('Password', validators=[DataRequired()], default='a')
	submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def home_page():
	return render_template('home.html')

@login_required
@app.route('/inner_page', methods=['GET', 'POST'])
def inner_page():
	return render_template('inner_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	
	LF = LoginForm(request.form)
	error = None

	if request.method == 'POST':

		user_name = LF.name.data
		user_pass = LF.password.data

		existing_user = [u for u in UDB.get_users() if u[1] == user_name]
		if not existing_user:
			error = 'User not found.'
			flash(error)
		else:
			existing_user = existing_user[0]
			user_id = existing_user[0]
			required_pass = existing_user[4]
			print(required_pass, user_pass)
			if check_password_hash(required_pass, user_pass):
				error = 'Invalid pass. Try again.'
				flash(error)
			else:
				login_user( User(user_id))
				UDB.update_user( {'last_login': time_now()}, user_id)
				session['username'] = user_name 
				session['user_id'] = user_id
				session['_fresh'] = True
				return redirect('/')
			
	return render_template('login.html', error=error, form=LF)

@app.route('/singup', methods=['GET', 'POST'])
def singup():

	SF = SignupForm(request.form)
	error = None
	if request.method == 'POST':
		user_content = {}
		user_content['name'] = SF.name.data
		user_content['email'] = SF.email.data
		user_content['password'] = SF.password.data
		user_content['info'] = SF.info.data
		user_content['created_at'] = time_now()
		user_content['last_login'] = time_now()

		existing_user_names = [ user_data[1] for user_data in UDB.get_users()]

		if user_content['name'] in existing_user_names:
			error = 'Login already exists.'
			flash(error)

		confirm_password = SF.confirm_password.data
		if user_content['password'] != confirm_password:
			error = "Passwords don't match."
			flash(error)
		
		if user_content['name'] not in existing_user_names and user_content['password'] == confirm_password: 
			user_content['password'] = generate_password_hash(user_content['password'], method='sha256')
			UDB.create_user(user_content)
			return redirect('/login')

	return render_template('singup.html', error=error, form=SF)

@app.route('/user/<username>')
def user_profile(username):
	pass

@app.route('/user/<username>/edit')
def edit_user_profile(username):
    pass

@app.route("/logout")
@login_required
def logout():
	logout_user()
	try:
		session.clear()
	except:
		pass
	return redirect('/login')

@login_manager.user_loader
def get_user_loaded(user_id):
	if user_id is not None:
		return User(user_id)
	return None

if __name__ == "__main__":
	app.run()