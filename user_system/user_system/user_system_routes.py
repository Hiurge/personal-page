from flask import Flask, render_template, flash, redirect, request, url_for, session
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

import psycopg2

import collections
import os

from flask import Blueprint
from flask import current_app as app

from user_system.user_system.user_system_helpers import User, time_now
from user_system.user_system.forms import SignupForm, LoginForm

from db import UsersTable

user_system_bp = Blueprint('user_system_bp', __name__, template_folder='templates', static_folder='static') 

login_manager = LoginManager()
login_manager.init_app(app)  # REFACTOR IT

access = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}  # REFACTOR IT
UT = UsersTable(access)  # REFACTOR IT


@user_system_bp.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	LF = LoginForm(request.form)
	if request.method == 'POST':

		typed_user_name = LF.name.data
		typed_user_pass = LF.password.data

		try:
			existing_user_data = list([u for u in UT.get_users() if u[1] == typed_user_name][0])
		except:
			existing_user_data = None
		if not existing_user_data:
			error = 'User not found.'
			flash(error)
		else:
			user_id = existing_user_data[0]
			required_pass = existing_user_data[2]
			if check_password_hash(required_pass, typed_user_pass):
				login_user( User(user_id))
				UT.update_user( {'last_login': time_now()}, user_id)
				session['username'] = typed_user_name 
				session['user_id'] = user_id
				session['_fresh'] = True
				admin_name = [ud for i, ud in enumerate(UT.get_user(1)[0]) if i == 1][0]
				if typed_user_name == admin_name:
					session['role'] = 'admin'
				else:
					session['role'] = 'user'
				return redirect('/')
			else:
				error = 'Invalid pass. Try again.'
				flash(error)
	  
	return render_template('login.html', error=error, form=LF)

@user_system_bp.route('/singup', methods=['GET', 'POST'])
def singup():
	SF = SignupForm(request.form)
	error = None
	if request.method == 'POST' and SF.validate():
		user_data = {}
		user_data['name'] = SF.name.data
		user_data['email'] = SF.email.data
		user_data['password'] = SF.password.data
		user_data['info'] = SF.info.data
		user_data['created_at'] = time_now()
		user_data['last_login'] = time_now()

		existing_user_names = [ user[1] for user in UT.get_users()]

		# First user gets admin role by default.
		if not existing_user_names:
			user_data['role'] = 'admin'
		else:
			user_data['role'] = 'user'

		if user_data['name'] in existing_user_names:
			error = 'Login already exists.'
			flash(error)

		confirm_password = SF.confirm_password.data
		if user_data['password'] != confirm_password:
			error = "Passwords don't match."
			flash(error)
		
		if user_data['name'] not in existing_user_names and user_data['password'] == confirm_password: 
			user_data['password'] = generate_password_hash(user_data['password'], method='sha256')
			UT.create_user(user_data)
			return redirect('/login')

	return render_template('singup.html', error=error, form=SF)

@user_system_bp.route('/user/<username>')
def user_profile(username):
	pass

@user_system_bp.route('/user/<username>/edit')
def edit_user_profile(username):
	pass

@user_system_bp.route('/inner_page', methods=['GET', 'POST'])
@login_required
def inner_page():
	return render_template('inner_page.html')

@user_system_bp.route("/logout")
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

@login_manager.unauthorized_handler
def unauthorized():
	flash('You must be logged in to view that page.')
	return redirect('/login')

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error('Page not found: %s', (request.path))
	return render_template('404.html'), 404