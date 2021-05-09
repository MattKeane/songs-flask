from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

artists = Blueprint('artists', 'artists')

@artists.route('/', methods=['GET'])
def get_all_artists():
	all_artists = models.Artist.select()
	artist_dicts = [model_to_dict(artist) for artist in all_artists]
	return jsonify(
		data=artist_dicts,
		message=f'Returned {len(artist_dicts)} artists.',
		status=200), 200

@artists.route('/', methods=['POST'])
@login_required
def create_new_artist():
	payload = request.get_json()
	payload['added_by'] = current_user
	new_artist = models.Artist.create(**payload)
	new_artist_dict = model_to_dict(new_artist)
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
def update_artist(id):
	payload = request.get_json()
	try:
		(models.Artist
			.update(**payload)
			.where(models.Artist.id == id)
			.execute())
		updated_artist = models.Artist.get_by_id(id)
		artist_dict = model_to_dict(updated_artist)
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
def delete_artist(id):
	try:
		artist_to_delete = models.Artist.get_by_id(id)
		artist_to_delete.delete_instance()
		return jsonify(
			message='Artist successfully deleted',
			status=200), 200
	except models.DoesNotExist:
		return jsonify(
			message='Artist does not exist',
			status=400), 400