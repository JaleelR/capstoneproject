from unittest import TestCase
from api import fetchapidata, convert_apidb_to_postdb
from models import db, Api, Post
from app import app


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///test_motivate"




class ApiModelTestCase(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def test_fetchapidata_convert(self):
        "test that the get request for youtube and gnew api works and return correct amount with correct attributes"
        fetchapidata()
        convert_apidb_to_postdb()
        self.assertEquals(len(Api.query.filter(Api.channeltitle != None).all()), 25)
        self.assertEquals(len(Api.query.filter(Api.channeltitle == None).all()), 10)
        self.assertEquals(len(Post.query.all()), 35)


        