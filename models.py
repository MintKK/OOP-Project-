from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, \
AnonymousUserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from werkzeug import generate_password_hash, check_password_hash

sqldb = SQLAlchemy()

class Organisations(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    name = sqldb.Column(sqldb.String())
    email = sqldb.Column(sqldb.String())
    address = sqldb.Column(sqldb.String())
    phone = sqldb.Column(sqldb.String())

class Employees(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key = True)
    name = sqldb.Column(sqldb.String())
    email = sqldb.Column(sqldb.String())
    position = sqldb.Column(sqldb.String())
    phone = sqldb.Column(sqldb.String())

class Events(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key = True)
    name = sqldb.Column(sqldb.String())
    organisations = sqldb.Column(sqldb.String())
    things = sqldb.Column(sqldb.String())
    date = sqldb.Column(sqldb.String())
    website = sqldb.Column(sqldb.String())

class User(UserMixin, sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key = True)
    username = sqldb.Column(sqldb.String(100), unique= True)
    email = sqldb.Column(sqldb.String(120), unique = True)
    pwdhash = sqldb.Column(sqldb.String(54))

    def __init__(self, username = '', firstname= '', lastname= '', email= '', password= ''):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.username = username
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    