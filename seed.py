from models import User, Post, Like, Comment, db
from app import app 
from api import fetchapidata, convert_apidb_to_postdb

db.drop_all()
db.create_all()



fetchapidata()

convert_apidb_to_postdb()