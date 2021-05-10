# modules
from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from flask_login import LoginManager

import models

load_dotenv()
PORT = os.environ.get('PORT')
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True

app = Flask(__name__)

# Setting up sessions
app.secret_key = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)

def handle_unauthorized():
	return jsonify(
		data={},
		message='You must be logged in to do that!',
		status=401), 401

login_manager.unauthorized_handler(handle_unauthorized)

@login_manager.user_loader
def load_user(user_id):
	try:
		user = models.User.get_by_id(user_id)
		return user
	except models.DoesNotExist:
		return None

# Registering Blueprints
from resources.artists import artists
from resources.auth import auth
from resources.songs import songs
app.register_blueprint(artists, url_prefix='/api/v1/artists')
app.register_blueprint(auth, url_prefix='/api/v1/auth')
app.register_blueprint(songs, url_prefix='/api/v1/songs')

@app.route('/')
def test():
	return 'test route works!'

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)