from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

artists = Blueprint('artists', 'artists')

@artists.route('/', methods=['GET'])
def get_all_artists():
	all_artists = models.Artist.select()
	artist_dicts = []
	for artist_entry in all_artists:
		artist_dict = model_to_dict(artist_entry)
		artist_dict['added_by'].pop('password')
		artist_dicts.append(artist_dict)
	return jsonify(
		data=artist_dicts,
		message=f'Returned {len(artist_dicts)} artists.',
		status=200), 200

@artists.route('/', methods=['POST'])
@login_required
def create_new_artist():
	payload = request.get_json()
	payload['added_by'] = current_user.id
	new_artist = models.Artist.create(**payload)
	new_artist_dict = model_to_dict(new_artist)
	new_artist_dict['added_by'].pop('password')
	return jsonify(
		data=new_artist_dict,
		message='Artist succesfully created',
		status=201), 201

@artists.route('/<id>', methods=['GET'])
def get_artist(id):
	try:
		found_artist = models.Artist.get_by_id(id)
		artist_dict = model_to_dict(found_artist)
		return jsonify(
			data=artist_dict,
			message='Artist returned.',
			status=200), 200
	except models.DoesNotExist:
		return jsonify(
			data={},
			message='Error fetching artist',
			status=400), 400

@artists.route('/<id>', methods=['PUT'])
@login_required
def update_artist(id):
	payload = request.get_json()
	try:
		artist_to_update = models.Artist.get_by_id(id)
		if artist_to_update.added_by.id == current_user.id:
			(artist_to_update
				.update(**payload)
				.execute())
			updated_artist = models.Artist.get_by_id(id)
			artist_dict = model_to_dict(updated_artist)
			artist_dict['added_by'].pop('password')
			return jsonify(
				data=artist_dict,
				message='Successfully updated artist.',
				status=200), 200
		else:
			return jsonify(
				data={},
				message='You are not authorized to do that',
				status=401), 401
		return jsonify(
			data=artist_dict,
			message='Succesfully updated artist.',
			status=200), 200
	except models.DoesNotExist:
		return jsonify(
			data={},
			message='Artist does not exist.',
			status=400), 400

@artists.route('/<id>', methods=['DELETE'])
@login_required
def delete_artist(id):
	try:
		artist_to_delete = models.Artist.get_by_id(id)
		if artist_to_delete.added_by.id == current_user.id:
			artist_to_delete.delete_instance()
			return jsonify(
				message='Artist successfully deleted',
				status=200), 200
		else:
			return jsonify(
				message='You are not authorized to do that',
				status=401), 401
	except models.DoesNotExist:
		return jsonify(
			message='Artist does not exist',
			status=400), 400