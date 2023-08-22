
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import CheckConstraint

 

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable = False)
    username  = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    img = db.Column(db.Text, nullable = True)
    likes = db.relationship("Like", backref = 'users')
    posts = db.relationship("Post", backref = "user")

    @classmethod
    def signup(cls, name, username, password, img):
        '''Sign up class method on user.
        creates hashed password to keep password protected '''
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            name=name,
            username=username,
            password=hashed_pwd,
            img= img,
        )

        db.session.add(user)
        return user
        
    @classmethod
    def authenticate(cls, username, password):
        '''for login of user
        searches user by username and check if password is same, if so user log in successful '''
        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
         
                return user





class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable = False)
    youtuber = db.Column(db.Text, nullable = True)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = "CASCADE"), nullable = True)
    api_id = db.Column(db.Integer, db.ForeignKey('apis.id', ondelete = "CASCADE"), nullable = True)
    api_info = db.relationship("Api", backref="posts_info")
    likes = db.relationship("Like", backref='posts',
                            cascade="all, delete-orphan", passive_deletes=True)
    comments = db.relationship("Comment", backref = 'posts')
    ''' Checks that either user_id or api_id will be used
    both cannot be filled or can they both be null'''
    __table_args__= (
        CheckConstraint('(user_id IS NULL AND api_id IS NOT NULL) OR (user_id IS NOT NULL AND api_id IS NULL)' ),
    )


class Api(db.Model):
    __tablename__ = 'apis'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    content = db.Column(db.String(500))
    img = db.Column(db.Text, nullable = True)
    url = db.Column(db.Text)
    channeltitle = db.Column(db.Text, nullable = True)
    videoid = db.Column(db.Text, nullable = True)
    name = db.Column(db.Text, nullable = True)





    def serialize(api):
        '''serialize a api sqlaalchemy obj to dictionary '''
        return {
            "id": api.id,
            "title": api.title, 
            "content": api.content, 
            "img": api.img, 
            "url": api.url,
            "channeltitle": api.channeltitle,
            "videoid": api.videoid  
                  }





class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = "CASCADE"), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete = "CASCADE"), nullable = False)




class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = "CASCADE"), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete = "CASCADE"), nullable = False)
   