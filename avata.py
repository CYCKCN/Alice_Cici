import os
from flask import Blueprint, render_template, redirect, url_for, request
from flask import Flask
from easydict import EasyDict
from pprint import pprint

import demo_utils
from test_data import ROOM, PERSONAL_TYPE, MONTH_ABBR

PATH_templates='frontend/templates'
PATH_static='frontend/static'

app = Flask(__name__, template_folder=PATH_templates, static_folder=PATH_static)
#app = Flask(__name__)

CURRENT_ROOM=ROOM(oscwd=os.getcwd())

@app.route("/")
def hello():
    return 'hello'

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        if email:
            return redirect(url_for('search'))

    return render_template('login.html')

@app.route("/verification/<email>", methods=['POST','GET'])
def verification(email):
    if request.method == "POST":
        code = request.form.get('code')
        if code:
            return redirect(url_for('search'))

    return render_template('verification-code.html', userEmail=email)

@app.route("/device/<room_id>", methods=['POST','GET'])
def device(room_id):
    #global CURRENT_ROOM
    if request.method == "POST":
        personal = request.form.get('personal')
        confirm = request.form.get('confirm')  # how to run confirm button
        if personal:
            device=[]
            for d in PERSONAL_TYPE:
                if request.form.get(d):
                    device.append(d)

            CURRENT_ROOM.get_data_choose_devices()
            CURRENT_ROOM.get_data_personal_device(device)
            CURRENT_ROOM.set_data_instruction()
            return redirect(url_for('instructor_choose'))

    dic=CURRENT_ROOM.set_data_choose_devices(use_related=True)
    img=CURRENT_ROOM.image_360
    #print(dic)
    return render_template('device.html',dic=dic,img=img)

@app.route("/search", methods=['POST','GET'])
def search():
    room_id=''
    if request.method == "POST":
        room_id=request.form.get('room_id')
        return redirect(url_for('room',room_id=room_id))

    return render_template('search.html',room_id=room_id)

@app.route("/room/<room_id>", methods=['POST','GET'])
def room(room_id):
    if request.method == "POST":
        CURRENT_ROOM(room_id=room_id)
        if request.form.get('enter'):
            return redirect(url_for('device',room_id=CURRENT_ROOM.room_id))
        elif request.form.get('book'):
            return redirect(url_for('booking',room_name='5554'))
    
    return render_template('room.html')

@app.route("/booking/<room_name>", methods=['POST','GET'])
def booking(room_name):
    if request.method == "POST":
        if request.form.get('back'):
            return redirect(url_for('room',room_id=room_name))
        elif request.form.get('home'):
            return render_template('search.html',room_id=room_name)
        elif request.form.get('book'):
            CURRENT_ROOM.get_booking_result()
            return  redirect(url_for('room',room_id=room_name))

    time=CURRENT_ROOM.booking_time
    week=CURRENT_ROOM.set_booking_week()
    month=MONTH_ABBR[CURRENT_ROOM.today_date[1]]
    year=CURRENT_ROOM.today_date[0]
    occupy=CURRENT_ROOM.set_booking_occupy()
    return render_template('booking.html',room=room_name,time=time,week=week,month=month,year=year,occupy=occupy)

@app.route("/personal-device", methods=['POST','GET'])
def personal_device():
    if request.method == "POST":
        device=[]
        for d in PERSONAL_TYPE:
            if request.form.get(d):
                device.append(d)

        #global CURRENT_ROOM
        CURRENT_ROOM.get_data_personal_device(device)
        CURRENT_ROOM.set_data_instruction()

        return redirect(url_for('instructor_choose'))

    return render_template('personal-device.html')

@app.route("/instruction-choose", methods=['POST','GET'])
def instructor_choose():
    #global CURRENT_ROOM
    if request.method == "POST":
        device=request.form.get('input')
        CURRENT_ROOM.create_guide_queue(device)
        return redirect(url_for('instruction'))
    
    img=CURRENT_ROOM.image_360
    dic=CURRENT_ROOM.choose_devices_relative(use_related=False)
    order=CURRENT_ROOM.get_guide_order()
    #pprint(dic)
    #pprint(CURRENT_ROOM.image_360_deivces)
    #pprint(CURRENT_ROOM.image_360_deivces_related)
    return render_template('instruction-choose.html',dic=dic, image_path=img, order=order)

@app.route("/instruction", methods=['POST','GET'])
def instruction():
    #global CURRENT_ROOM
    guide=None
    if request.method == "POST":
        if len(CURRENT_ROOM.guide_queque)==0:
            return redirect(url_for('instructor_choose'))
        else:
            guide=CURRENT_ROOM.pop_guide_queue()
            return render_template('instruction.html',title="Guide of "+CURRENT_ROOM.guide_device,guide=guide)

    guide=CURRENT_ROOM.pop_guide_queue()
    return render_template('instruction.html',title="Guide of "+CURRENT_ROOM.guide_device,guide=guide)


@app.route("/code", methods=['POST','GET'])
def code():
    if request.method == "POST":
        text = request.form.get('text')
        code = request.form.get('code')
        if text or code:
            return "<h1>" + text + " " + code + "</h1>"

    return render_template('code.html')

devices_dict = {}
from objects_admin import *

@app.route("/point", methods=['POST','GET'])
def point():
    k = '4223'  # Three point initalization
    global devices_test_admin
    devices_dict[k] = devices_test_admin

    if request.method == "POST":
        update_from_admin_request(devices_dict[k])
    
    return render_template('point.html', devices=devices_dict[k].getJson(),devices_choose=devices_dict[k].chooseDevice())

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)