from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
import peewee

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
def create_new_artist():
	payload = request.get_json()
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
	except peewee.DoesNotExist:
		return jsonify(
			data={},
			message='Error fetching artist',
			status=400), 400