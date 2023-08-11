from unittest import TestCase 
from models import db, connect_db, User, Post, Api

from app import session, app, session





app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///test_motivate"
db.create_all()
app.config['WTF_CSRF_ENABLED']=False 
class UserViewTestCase(TestCase): 

    def setUp(self):
        """ Deletes user, api and post before each test """
        User.query.delete()
        Api.query.delete()
        Post.query.delete()

        

        """allows you to simulate http requests(get and post)"""
        self.client = app.test_client()


        """ Creates user in db """
        self.tester = User.signup(
            name="Jay",
            username="coder21",
            password="password",
            img=""
                )
        id = 10
        self.tester.id = id
        db.session.commit()





    def tearDown(self):
            resp = super().tearDown()

            "Makes sure that changes made to not persist to database"
            
            db.session.rollback()
            return resp

    def test_home(self):
            """tests that correct user is logged in for home instantly """
            with self.client as c:
                resp = c.post('/login', data={
                "username": "coder21",
                "password": "password"
                })
                resp2 = c.get(f"/home/{10}")
                self.assertIn("coder21", str(resp2.data))  
    
    def test_register_and_firstredirect(self):
            """tests that after registering the user is redirected to home page """


            """test if user isn't logged in to direct to register"""
            with self.client as c:
                resp = c.get("/")
                self.assertEquals(resp.location, "/register")



                """checks if user is registered or logged in, user is redirect to home  """
                u = {
                    "name": "ish",
                    "username": "ishkabibbles",
                    "password" : "iamagreatcoder",
                    "img":""
                    }
    
                resp2 = c.post("/register", data = u )
                self.assertEqual(resp2.status_code, 302)

                user = User.query.filter(User.name == "ish").first()
                self.assertEqual(resp2.location, f"/home/{user.id}")




  
          




    def test_logout(self): 
        """test that user can log in, log out and is redirected to register"""
    
        with self.client as c:
            resp = c.post('/login', data={
                "username": "coder21",
                "password": "password"
            },follow_redirects = True)
            self.assertEquals(resp.status_code, 200)
    

        resp2 =  c.get('/logout')
        self.assertEqual(resp2.location, "/login")



    def test_redirect_and_post(self):
        """Test that user can create post and it shows on home page and user page"""
        with self.client as c:
            resp = c.post('/login', data={
                "username": "coder21",
                "password": "password"
            })
            self.assertEquals(resp.status_code, 302)


            user = User.query.filter(User.username == "coder21").first()
            resp2 = c.post(f'/home/{user.id}', data={
                "text": "hello there!",
                "user_id": user.id
            }, follow_redirects = True)
            self.assertIn("\\r\\nhello there!</textarea>\\n", str(resp2.data))

            resp3 = c.get(f"/user/{user.id}", follow_redirects = True)
            self.assertIn("\\n  hello there!", str(resp3.data))


    def test_edit_user(self):
        """test that user can be edited and saved"""

        with self.client as c:
            resp = c.post('/login', data={
                "username": "coder21",
                "password": "password"
            })
            self.assertEquals(resp.status_code, 302)


            user = User.query.filter(User.username == "coder21").first()

            resp2 = c.post(f'/user/{user.id}/edit', data={
                "username": "6figureearner",
                "img": "qqqqq.png"
            }, follow_redirects = True)


    
            self.assertEqual(user.username, "6figureearner")



    def test_edit_and_delete(self):
        """test that post can be edited and deleted"""

        with self.client as c:
            resp = c.post('/login', data={
                "username": "coder21",
                "password": "password"
            })
            self.assertEquals(resp.status_code, 302)


            user = User.query.filter(User.username == "coder21").first()
            
            resp2 = c.post(f'/home/{user.id}', data={
            
                "text": "hello there!",
                "user_id": user.id
            }, follow_redirects = True)
           
            post = Post.query.filter(Post.text.like('%hello there%')).first()

            
            resp3 = c.post(f'/post/{post.id}/edit', data={
                "text": "There is light in everyday"
            }, follow_redirects = True)
            

            resp4 = c.get(f"/user/{user.id}", follow_redirects = True)
            self.assertIn("\\n  There is light in everyday", str(resp4.data))

            resp5 = c.post(f'/post/{post.id}/delete')
            self.assertEquals(len(Post.query.all()), 0)
            
    


    def test_user_delete(self):
            """test that route deletes user"""
            with self.client as c:
                resp = c.post('/login', data={
                    "username": "coder21",
                    "password": "password"
                })
               
                resp2 = c.post(f"/user/{10}/delete")
                self.assertEquals(len(User.query.all()), 0)

        










            
    






       
       
       
        













