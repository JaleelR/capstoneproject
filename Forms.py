from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import Optional, InputRequired, Length
from flask_wtf.file import FileField, FileAllowed


class RegisterForm(FlaskForm):
    name = StringField("name", validators=[InputRequired()])
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired(), (Length(min=8))])
    img = FileField("Profile picture", validators= [FileAllowed(["jpg", "jpeg", "png", "gif"])])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class EditUserForm(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
    img = FileField("Profile Picture", validators= [FileAllowed(["jpg", "jpeg", "png", "gif"])])


class MakePostForm(FlaskForm):
    text = StringField("text", validators=[InputRequired()])


class EditPostForm(FlaskForm):
    text = TextAreaField("content", validators=[InputRequired()])




