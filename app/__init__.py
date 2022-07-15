import flask
import secrets
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_user import UserManager, UserMixin

from flask_login import LoginManager
from .database.utils import User
from .database.db import accountdb, connection

'''
print("##")
from .models import ConfigClass
print("##")
'''
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

app = Flask(__name__)
app.config.from_object(ConfigClass)

login_manager = LoginManager()
login_manager.login_view = "main"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    account = accountdb.findUser(user_id)
    if not account: return None
    return User(email=account["accountEmail"], room=account["room"], identity=account["accountID"], deviceIDList=account["deviceIDList"])

#mongo = MongoEngine(app)

#from .models import User

#user_manager = UserManager(app, mongo, User)

#from .database import connection#, AccountDB, DeviceDB, RoomDB

db = connection("test")
#accountdb = AccountDB(db)
#devicedb = DeviceDB(db)
#roomdb = RoomDB(db)

from app import routes
from .user import user
from .admin import admin_blue
#from .authen import authen_blue
from .auth import auth

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(admin_blue, url_prefix='/admin')
#app.register_blueprint(authen_blue)
app.register_blueprint(auth, url_prefix='/auth')