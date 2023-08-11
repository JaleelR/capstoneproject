from flask import Flask, render_template,redirect, request, flash, session, g, url_for, send_from_directory
from Forms import EditUserForm, RegisterForm,  EditPostForm, LoginForm, MakePostForm
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Like, Post, Api, Comment
from api import convert_apidb_to_postdb, fetchapidata
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads')
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///motivate"
app.config['SECRET_KEY'] = 'Naruto7'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

migrate = Migrate(app, db)
ctx = app.app_context()
ctx.push()



# db.drop_all()
# db.create_all()

@app.before_request 
def beforerequest():
    '''checks if user is logged in. If so make g.user the user.id if not put none'''
    if 'user_id' in session:
        g.user = session['user_id']
    else:
        g.user = None
        




@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def logoutuser():
    del session['user_id']


def loginuser(user):
    session['user_id'] = user.id


routesnotneededforlogin = ["/register","/login" ]
fetchapidata()
convert_apidb_to_postdb()



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    uploads user profile pictures from device to uplodes file

    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/register", methods =["POST", "GET"])
def register(): 

    """  registers user   """
    form = RegisterForm() 
    try:
        if form.validate_on_submit():
            name = form.name.data
            username = form.username.data
            password = form.password.data
            if form.img.data:
                """ takes file from uploads folder and saves it ad form.img.data"""
                filename = secure_filename(form.img.data.filename)
                form.img.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                img = filename    
            else:
                img = ""
            user = User.signup(name = name, username = username, password = password, img = img)
            db.session.add(user)
            db.session.commit()
            loginuser(user)
        
            return redirect(f"/home/{user.id}")
    except IntegrityError as e:
        flash("Username already taken, Please choose another", "error")
    return render_template('register.html',form = form)


@app.route("/login", methods=["GET","POST"])
def login(): 
    """
    logs in user
    checks for valid username and password
    """
    form = LoginForm()

    """logs in user"""
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate( username = username, password = password)
       
        if  user is None:
           flash("wrong username or password", "danger")

        else:
            loginuser(user)
            return redirect(f"/home/{user.id}")
    
    return render_template('login.html', form = form)


@app.route("/logout")
def logout():

    """logs out user"""

    if "user_id" in session:
        logoutuser()
        flash("successfully logged out", "success")
    return redirect("/login")



@app.route("/home/<int:user_id>", methods = ["POST", "GET"])
def home(user_id): 
    fetchapidata()
   
    """ 
    - displays main page of site
    - seperates video posts from article posts 
    - allows user to add post on the page 
    
    """ 
    
    print(f"______@@@@@@@@@@@@@@@__{fetchapidata()}")
    if not g.user:
        flash("please sign up first", "danger")
        return redirect("/register")
    try:     
        user = User.query.get_or_404(user_id)
        vidpost = Post.query.filter(Post.youtuber != None).all()

        form = MakePostForm()
        if form.validate_on_submit(): 
            post = Post(text = form.text.data, user_id = user.id)
            user.posts.append(post)
            db.session.commit() 
            
        textpost = Post.query.filter(Post.youtuber == None).order_by(Post.timestamp.desc()).all()
        return render_template("home.html", user = user, form = form, vids = vidpost, post = textpost)
    except KeyError: 
        flash("please sign up first", "warning")
        return redirect('/register')




@app.route("/")
def redirectfirstpage():


    """
    redirects user to home if signed in
    redirects users to register if not signed in
    """


    try:
        user = User.query.filter(User.id == session["user_id"]).first()
        return redirect(f"/home/{user.id}") 
    except:
        flash("Please login or register first", "warning")
        return redirect("/register")


@app.route("/user/<int:user_id>")
def userdetails(user_id): 
    if not g.user:
        flash("please sign up first", "danger")
        return redirect("/register")
    user = User.query.get_or_404(user_id)
    return render_template('users/userdetails.html', user = user)





@app.route("/user/<int:user_id>/edit", methods = ["GET","POST"])
def edituser(user_id): 
    """edits users """
    if not g.user:
        flash("please sign up first", "danger")
        return redirect("/register")
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj = user)
    if form.validate_on_submit():

        """
        checks if an img was selected for form.img.data. 
        if true takes img from uploads
        """

        if form.img.data:

            """saves the file name upladed and saves file to img"""

            filename = secure_filename(form.img.data.filename)
            form.img.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = filename
        else:
            img = ""
        user.username = form.username.data
        user.img = img
        db.session.commit()
        return redirect(f"/user/{user.id}")

    return render_template('users/edituser.html',form = form)




@app.route("/user/<int:user_id>/delete", methods = ["POST"])
def deleteprofile(user_id): 

    "delete Users"

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/register")



@app.route("/post/<int:post_id>/edit", methods = ["GET","POST"])
def editpost(post_id): 

    """"edits users posts"""

    if not g.user:
        flash("please sign up first", "danger")
        return redirect("/register")
        
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user.id)
    form = EditPostForm(obj = post)
    if form.validate_on_submit():
        post.text = form.text.data
        db.session.commit()
        return redirect(f"/user/{user.id}")

    return render_template('users/edituser.html',form = form)





@app.route("/post/<int:post_id>/delete", methods =["POST"])
def deletepost(post_id): 

    "delete post"

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user.id)
    db.session.delete(post)
    db.session.commit()
    flash("Successfully deleted post","success")
    return redirect(f"/home/{user.id}")






