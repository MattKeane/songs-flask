from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

import models

songs = Blueprint('songs', 'songs')

@songs.route('/', methods=['POST'])
@login_required
def add_new_song():
    payload = request.get_json()
    payload['added_by'] = current_user.id
    created_song = models.Song.create(**payload)
    song_dict = model_to_dict(created_song)
    song_dict['artist'].pop('added_by')
    song_dict['added_by'].pop('password')
    return jsonify(
        data=song_dict,
        message='Successfully created song',
        status=201), 201

@songs.route('/', methods=['GET'])
def get_all_songs():
    all_songs = models.Song.select()
    song_dicts = []
    for song in all_songs:
        song_dict = model_to_dict(song)
        song_dict['added_by'].pop('password')
        song_dict['artist'].pop('added_by')
        song_dicts.append(song_dict)
    return jsonify(
        data=song_dicts,
        message=f'Returned {len(song_dicts)} songs',
        status=200), 200