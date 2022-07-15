#------------------ Flask Config

import secrets

class ConfigClass(object):
    SECRET_KEY = secrets.token_hex(16)

    MONGODB_SETTINGS = {
        'db': 'AVATA',
        'host': 'mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/AVATA?retryWrites=true&w=majority'
    }

    USER_APP_NAME = "AVATA" 
    USER_ENABLE_EMAIL = False     
    USER_ENABLE_USERNAME = True  
    USER_REQUIRE_RETYPE_PASSWORD = False  

    USER_LOGIN_TEMPLATE = 'login.html'
    USER_REGISTER_TEMPLATE = 'register.html'

#------------------ MongoEngine

from app import mongo as db
from flask_user import UserMixin

class User(db.Document, UserMixin):
    meta = {'collection':'accounts'}

    username = db.StringField(default='', required=True)
    password = db.StringField(required=True)

    email = db.StringField(default='', required=True)
    room = db.StringField(default='', required=True)

    roles = db.StringField(default='USER', required=True)

#------------------ wtforms

from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import InputRequired, Email, Length, Regexp

class RegisterForm(FlaskForm):
    password = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])
    passwordRepeat = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])
    email = wtforms.StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])

class LoginForm(FlaskForm):
    email = wtforms.StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])

class ResetForm(FlaskForm):
    email = wtforms.StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    oldpassword = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])
    newpassword = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])

class RoomBasicForm(FlaskForm):
    roomName = wtforms.StringField('roomName', validators=[InputRequired(), Length(max=10)])
    roomImage = wtforms.FileField('roomImage', validators=[InputRequired(), Regexp('([^\\s]+(\\.(?i)(jpe?g|png|bmp))$)')])
    roomLoc = wtforms.StringField('roomLoc', validators=[InputRequired(), Length(max=30)])

#------------------ MongeClient
class Account(object):
    def __init__(self, email, password, identity="USER"):
        self.accountEmail = email # "example@example.com"
        self.accountPw = password # "examplePW"
        self.accountID = identity # "USER" / "ADMIN"

class Device(object):
    def __init__(self, deviceID, roomName, deviceName, deviceType, deviceIP, deviceLocX, deviceLocY):
        self.deviceID = deviceID
        self.roomName = roomName # "IEDA Conference Room, Room 5554"
        self.deviceName = deviceName # "project_1"
        self.deviceType = deviceType # "display_projector_WIFI"
        self.deviceIP = deviceIP # "000.00.000.000:0000"
        self.deviceLocX = deviceLocX # 1
        self.deviceLocY = deviceLocY # 2

class Room(object):
    def __init__(self, roomName, roomImg, roomLoc):
        self.roomName = roomName # "IEDA Conference Room, Room 5554"
        self.roomImg = roomImg # ""
        self.roomLoc = roomLoc # "Academic Building"
        self.room360Img = ""
        self.bookBy = {}
        self.bookTime = {}
        self.insInitial = []
        self.insTurnon = {}
        self.insPair = []
        self.insZoom = {"video": [], "audio": []}