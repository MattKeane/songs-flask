from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('songs.sqlite')

class User(UserMixin, Model):
	username = CharField()
	email = CharField()
	password = CharField()

	class Meta:
		database = DATABASE

class Artist(Model):
	name = CharField()
	born = IntegerField()
	still_alive = BooleanField()

	class Meta:
		database = DATABASE

class Song(Model):
	title = CharField()
	released = IntegerField()
	artist = ForeignKeyField(User, backref='songs')

	class Meta:
		database = DATABASE

models = [User, Artist, Song]

def initialize():
	DATABASE.connect()
	DATABASE.create_tables(models, safe=True)
	print('Connected to database')
	DATABASE.close()