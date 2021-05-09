# modules
from flask import Flask
from dotenv import load_dotenv
import os

import models

load_dotenv()
PORT = os.environ.get('PORT')
DEBUG = True

app = Flask(__name__)

from resources.artists import artists
from resources.auth import auth
app.register_blueprint(artists, url_prefix='/api/v1/artists')
app.register_blueprint(auth, url_prefix='/api/v1/auth')

@app.route('/')
def test():
	return 'test route works!'

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)