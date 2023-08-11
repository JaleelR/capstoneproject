

from unittest import TestCase
from models import db, Post, User, Api, Like, Comment
from app import app
from sqlalchemy.exc import IntegrityError

'Connects tests_ to test motivate db'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///test_motivate"

db.create_all()

class UserModelTestCase(TestCase):
    "Test User models"
    def setUp(self):
        "ran after each test"
        "deletes user, post and api instances and creates test client"
        
        User.query.delete()
        Api.query.delete()
        Post.query.delete()

       
        
        self.client = app.test_client()
        
        """Allows you to similate a http request and observe responses """
      


    def test_user_signup_model(self): 
        "does the user model correctly sign up user?"
        u = User.signup(
            name = "Jaleel",
            username="coder211",
            password="password", 
            img=""
        )
        
        db.session.commit() 

        self.assertEqual(len(u.posts), 0)   
        self.assertEqual((u.username), "coder211")   
        self.assertEqual(len(u.likes), 0)   
    
    

    def test_user_sign_in(self):
        "Does sign in work"
        u = User.signup(
            name = "Jaleel",
            username="coder211",
            password="password", 
            img=""
        )
        db.session.commit()
    
        u2 = User.authenticate( username = u.username, password = u.password)
        self.assertEqual((u2), u2)



    def test_unique_username_model(self): 
        u = User(
            name = "Jaleel",
            username="coder21",
            password="password"
        )
        u2 = User(
            name = "Jal",
            username="coder21",
            password="passw"
        )

        db.session.add_all([u, u2])
        try: 
            db.session.commit()
        except IntegrityError as e:
            self.assertIn(" duplicate key value violates unique constraint ", str(e)) 
            db.session.rollback()


