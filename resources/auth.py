from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user

import models

auth = Blueprint('auth', 'auth')

# user login route
@auth.route('/login', methods=['POST'])
def user_login():
	payload = request.get_json()
	try:
		user_to_login = models.User.get(models.User.email == payload['email'])
		user_dict = model_to_dict(user_to_login)
		password_is_correct = check_password_hash(user_dict['password'], payload['password'])
		if password_is_correct:
			login_user(user_to_login)
			user_dict.pop('password')
			return jsonify(
				data=user_dict,
				message='User succesfully logged in',
				status=200), 200
		else:
			return jsonify(
				message='Invalid email or password',
				status=401), 401
	except models.DoesNotExist:
		return jsonify(
			message='Invalid email or password',
			status=401), 401		

# user registration route
@auth.route('/register', methods=['POST'])
def register_user():
	payload = request.get_json()
	try:
		models.User.get(models.User.email == payload['email'])
		return jsonify(
			message='User with that email already exists',
			status=401), 401
	except models.DoesNotExist:
		try:
			models.User.get(models.User.username == payload['username'])
			return jsonify(
				message='User with that username already exists',
				status=401), 401
		except models.DoesNotExist:
			payload['password'] = generate_password_hash(payload['password'])
			created_user = models.User.create(**payload)
			login_user(created_user)
			user_dict = model_to_dict(created_user)
			user_dict.pop('password')
			return jsonify(
				data=user_dict,
				message='User succesfully created',
				status=201), 201

# get current user
@auth.route('/current_user', methods=['GET'])
def get_current_user():
	if current_user.is_authenticated:
		user_dict = model_to_dict(current_user)
		user_dict.pop('password')
		return jsonify(
			data=user_dict,
			message='Returned current user',
			status=200), 200
	else:
		return jsonify(
			data={},
			message='No user currently logged in',
			status=401), 401

@auth.route('/logout', methods=['GET'])
def logout():
	logout_user()
	return jsonify(
		data={},
		message='User logged out',
		status=200), 200