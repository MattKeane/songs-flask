# modules
from flask import Flask

PORT = 8000
DEBUG = True

app = Flask(__name__)

@app.route('/')
def test():
	return 'test route works!'

if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)