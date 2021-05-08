# modules
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
PORT = os.environ.get('PORT')
DEBUG = True

app = Flask(__name__)

@app.route('/')
def test():
	return 'test route works!'

if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)