from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

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