from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash
from flask_login import login_user

import models

auth = Blueprint('auth', 'auth')

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