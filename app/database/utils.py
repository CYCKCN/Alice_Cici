from os import access
from flask_login import UserMixin
from flask_wtf import FlaskForm
from pymysql import DatabaseError
import wtforms
from wtforms.validators import InputRequired, Email, Length, Regexp
from datetime import datetime
from calendar import monthrange

time = ["0800", "0830", "0900", "0930", "1000", "1030", "1100", "1130", "1200", "1230", "1300", "1330", "1400", "1430", "1500",
        "1530", "1600", "1630", "1700", "1730", "1800", "1830", "1900", '1930', "2000", "2030", "2100", "2130", "2200"]
format_data = "%Y/%m/%d %H:%M:%S"
PERSONAL_TYPE=['mac','win','none']
MONTH_ABBR={
    1:'Jan',
    2:'Feb',
    3:'Mar',
    4:'Apr',
    5:'May',
    6:'June',
    7:'July',
    8:'Aug',
    9:'Sept',
    10:'Oct',
    11:'Nov',
    12:'Dec'
}
WEEK_ABBR={
    0:'Mon',
    1:'Tue',
    2:'Wed',
    3:'Thu',
    4:'Fri',
    5:'Sat',
    6:'Sun'
}

def compare_date_and_time(booking1, booking2):
    # print(booking1[0])
    if booking1[0] < booking2[0] or (booking1[0] == booking2[0] and booking1[1] < booking2[1]):
        return -1
    elif booking1[0] > booking2[0] or (booking1[0] == booking2[0] and booking1[1] > booking2[1]):
        return 1
    else:
        return 0

def sort_bookInfo_list(room1, room2):
    if room1['date'] < room2['date'] or (room1['date'] == room2['date'] and room1['time'][0] < room2['time'][0]):
        return -1
    elif room1['date'] > room2['date'] or (room1['date'] == room2['date'] and room1['time'][0] > room2['time'][0]):
        return 1
    else:
        return 0

def get_today_date():
    return list(map(int,(datetime.today().strftime('%Y %m %d')+' '+str(datetime.today().weekday())).split(' ')))

def get_booking_week():
    booking={}
    access_date = []
    today_date = get_today_date()
    _,month_days=monthrange(today_date[0],today_date[1])
    for i in range(7):
        week=(today_date[3]+i)%7
        day=today_date[2]+i
        if day>month_days: day=day-month_days
        booking[WEEK_ABBR[week]]=day

        if today_date[2]+i>month_days: #didn't consider next year
            date="{:d}/{:0>2d}/{:0>2d}".format(today_date[0], today_date[1]+1, today_date[2]+i-month_days)
        else:
            date="{:d}/{:0>2d}/{:0>2d}".format(today_date[0], today_date[1], today_date[2]+i)
        access_date.append(date)
    
    return booking, access_date

class User(UserMixin):
    def __init__(self, email, identity="", room="", deviceIDList=[]):
        self.email = email
        self.room = room
        self.deviceIDList = deviceIDList
        self.identity = identity

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.email

class Account(object):
    def __init__(self, email, password, identity="USER", room="", deviceIDList=[]):
        self.accountEmail = email # "example@example.com"
        self.accountPw = password # "examplePW"
        self.accountID = identity # "USER" / "ADMIN" / "GUEST"
        self.room = room # "5554"
        self.deviceIDList = deviceIDList # deviceIDList

class Device(object):
    def __init__(self, roomName, deviceName, deviceType, deviceIP, deviceLocX, deviceLocY):
        self.roomName = roomName # "5554"
        self.deviceName = deviceName # "project-1"
        self.deviceType = deviceType # "projector & screen"
        self.deviceIP = deviceIP # "000.00.000.000:0000"
        self.deviceLocX = deviceLocX # 1
        self.deviceLocY = deviceLocY # 2

class Room(object):
    def __init__(self, roomName, roomLoc, controlSystem):
        self.roomName = roomName # "IEDA Conference Room, Room 5554"
        self.roomLoc = roomLoc # "Academic Building"
        self.controlSystem = controlSystem
        self.bookBy = {}
        self.bookTime = {}

        # device List for room
        self.deviceNameList = {"0": "personal windows", "1": "personal apple", "2": "zoom", "3": "additional iPad"} # "project-1"
        self.deviceTypeList = {"0": "win", "1": "apple", "2": "zoom", "3": "additional iPad"} # "projector & screen"
        self.deviceIPList = {"0": "-1", "1": "-1", "2": "-1", "3": "-1"} # "000.00.000.000:0000"
        self.deviceLocXList = {"0": -1, "1": -1, "2": -1, "3": -1} # 1
        self.deviceLocYList = {"0": -1, "1": -1, "2": -1, "3": -1} # 2
        self.chooseDeviceIDList = []

        # maximum instruction for room
        self.roomInsDevice = {} # {0: [], 1: ["projector & screen"], 2: ["win", "projector & screen"], ...}
        self.roomInsCases = {} 
        # {0: -> device list
        #   {0: -> step number
        #       {"text": , "image": , "command": , "help": }, 
        #    1: 
        #       {"text": , "image": , "command": , "help": }
        #   }, 
        #  1:
        #   {0: 
        #       {"text": , "image": , "command": , "help": }, 
        #    1: 
        #       {"text": , "image": , "command": , "help": }
        #   }, 
        # ...}


class System(object):
    def __init__(self, controlSystem):
        self.controlSystem = controlSystem # "AMX"
        self.deviceTypeList = ["win", "apple", "zoom", "additional iPad"] # ["speaker", "projector & screen", "Display TV"...]

        # maximum instruction for the whole controling system

        self.insDevice = {} # {0: [], 1: ["projector & screen"], 2: ["win", "projector & screen"], ...}
        self.insCases = {} 
        # {0: -> evice list
        #   {0: -> step number
        #       {"text": , "image": , "command": }, 
        #    1: 
        #       {"text": , "image": , "command": }
        #   }, 
        #  1:
        #   {0: 
        #       {"text": , "image": , "command": }, 
        #    1: 
        #       {"text": , "image": , "command": }
        #   }, 
        # ...}


class RegisterForm(FlaskForm):
    username = wtforms.StringField('username', validators=[InputRequired(), Length(max=10)])
    password = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])
    passwordRepeat = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])

    email = wtforms.StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    room = wtforms.StringField('room', validators=[InputRequired(), Length(max=30)])

    roles = wtforms.RadioField('roles', validators=[InputRequired()], choices=[('USER', 'User'), ('ADMIN', 'Admin')])

class LoginForm(FlaskForm):
    email = wtforms.StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])

class ResetForm(FlaskForm):
    email = wtforms.StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])
    passwordRepeat = wtforms.PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])

class RoomBasicForm(FlaskForm):
    roomName = wtforms.StringField('roomName', validators=[InputRequired(), Length(max=10)])
    roomImage = wtforms.FileField('roomImage', validators=[InputRequired(), Regexp('([^\\s]+(\\.(?i)(jpe?g|png|bmp))$)')])
    roomLoc = wtforms.StringField('roomLoc', validators=[InputRequired(), Length(max=30)])

