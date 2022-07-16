import os
from flask import Blueprint, render_template, redirect, url_for, request
#from .authen import check_login
from .auth import check_login, check_admin
from .img_trans import *
# import utils
from .database.db import accountdb, systemdb, roomdb
from flask_login import logout_user

admin_blue=Blueprint('admin',__name__)

@admin_blue.route('/')
def enter():
    return 'admin flow'

# @admin_blue.route("/login", methods=['POST','GET'])
# def login():
#     if request.method == "POST":
#         text = request.form.get('email')
#         password = request.form.get('pwd')
#         if text or password:
#             return redirect(url_for('admin.main'))
#     return render_template('admin_login.html')

@admin_blue.route("/main", methods=['POST','GET'])
@check_admin
def main():
    error=request.args.get('error')
    if request.method == "POST":
        room_id=request.form.get('room_id') if not request.form.get('room_id')=='' else request.form.get('roomid')
        add=request.form.get('add')
        btn_profile=request.form.get('profile')
        btn_control = request.form.get('control')
        room = roomdb.getroom(room_id)

        if add:
            return redirect(url_for('admin.basic_info',room_id=room_id,is_addRoom=True))

        if btn_profile and room_id=='':
            return redirect(url_for('admin.profile'))

        if btn_control and room_id=='':
            return redirect(url_for('admin.control', room_id=room_id))
        
        if not room:
            return redirect(url_for('admin.main',error='Room not exists!'))

        if room_id:
            return redirect(url_for('admin.room',room_id=room_id))
            
    roomInfo = roomdb.getroomInfo()
    # roomInfo=utils.get_all_room_basic()
    #print(roomInfo)
    return render_template('admin_main.html', roomInfo=roomInfo, error=error if error else '')

@admin_blue.route("/room/<room_id>", methods=['POST','GET'])
@check_admin
def room(room_id):
    error=request.args.get('error')
    
    if request.method == "POST":
        edit=request.form.get('edit')
        if edit:
            return redirect(url_for('admin.basic_info',room_id=room_id,is_editRoom=True))
        delete=request.form.get('delete')
        if delete:
            roomdb.delRoom(room_id)
            # utils.delete_room_with_name(room_id)
            return redirect(url_for('admin.main'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.main'))
    room = roomdb.getroom(room_id)
    #utils.download_room_basic_image_with_name(room_id)
    return render_template('admin_room.html', room_id=room_id, room_loc=room["roomLoc"], room_cs=room["controlSystem"], error=error if error else '')

@admin_blue.route("/basic_info", methods=['POST','GET'])
@check_login 
def basic_info():
    room_id = request.args.get('room_id')
    is_addRoom = request.args.get('is_addRoom')
    is_editRoom = request.args.get('is_editRoom')

    #if is_editRoom:
        #utils.download_room_basic_image_with_name(room_id)

    if request.method == "POST":
        continue_=request.form.get('continue')
        if is_addRoom and continue_:
            #roomName
            roomName=request.form.get('room_id')
            print(roomName)
            room = roomdb.getroom(roomName)
            if room:
                return redirect(url_for('admin.room',room_id=roomName,is_editRoom=True,error='Room exists, please edit the room.'))

            #roomImage
            img_base64=request.form.get('imgSrc')
            # print(request.form.get('imgUpload'))
            # print(img_base64)
            roomImage=(img_base64.split(','))[-1]
            if len(roomImage)==0:
                return redirect(url_for('admin.basic_info',is_addRoom=True))

            #roomLoc
            roomLoc=request.form.get('room_loc')
            controlSystem=request.form.get('p_type')
            # controlSystem = "AMX" # need to be changed
            roomdb.addRoom(roomName, roomLoc, controlSystem)
            roomdb.uploadImage(roomName, roomImage, "_basic_upload.png")
            # utils.create_room_with_name_image_loc(roomName, roomImage, roomLoc)
            return redirect(url_for('admin.photo_360',room_id=roomName,is_addRoom=True))
        
        if is_editRoom and continue_:
            roomName = request.form.get('room_id') if request.form.get('room_id') else None
            roomLoc = request.form.get('room_loc') if request.form.get('room_loc') else None
            roomControlSystem = request.form.get('p_type') if request.form.get('p_type') != "None" else None
            
            img_base64=request.form.get('imgSrc')
            roomImage=(img_base64.split(','))[-1] if img_base64 else None

            dbInfo = roomdb.editRoom(room_id, roomName, roomLoc, roomControlSystem)
            
            # has_udpate=utils.update_room_with_name_image_loc(room_id, roomName, roomImage, roomLoc)

            if "Err" in dbInfo:
                return redirect(url_for('admin.room', room_id=roomName if roomName else room_id, is_editRoom=True, error='Invalid room name or empty submit!'))
            else:
                roomdb.uploadImage(roomName, roomImage, "_basic_upload.png")
                return redirect(url_for('admin.photo_360', room_id=roomName if roomName else room_id, is_editRoom=True))
       
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.room',room_id=room_id))
            

        #if continue_:
        #    return redirect(url_for('admin.photo_360',room_id=room_id))
    room = roomdb.getroom(room_id)
    type_dict = systemdb.getSystemList()
    # print(room)
    return render_template('admin_basic_info.html',
    room_id=room_id,
    room_loc="Academic Building" if not room else room['roomLoc'],
    is_addRoom=True if is_addRoom else False,
    is_editRoom=True if is_editRoom else False, 
    type_dict=type_dict,
    room_system = "None" if not room else room["controlSystem"])

@admin_blue.route("/photo_360", methods=['POST','GET'])
@check_login 
def photo_360():
    room_id = request.args.get('room_id')
    is_addRoom = request.args.get('is_addRoom')
    is_editRoom = request.args.get('is_editRoom')
    if request.method == "POST":
        continue_=request.form.get('continue')
        
        #if len(room360Image)==0:
        #    return redirect(url_for('admin.photo_360',is_addRoom=True))
        

        #if is_addRoom and continue_:
        #    return redirect(url_for('admin.device_info',room_id=room_id,is_addRoom=True))

        #if is_editRoom and continue_:
        #    return redirect(url_for('admin.device_info',room_id=room_id,is_editRoom=True))

        if continue_:
            img360_base64=request.form.get('img360Src')
            room360Image=(img360_base64.split(','))[-1] if img360_base64 else None
            roomdb.uploadImage(room_id, room360Image, "_360_upload.png")
            return redirect(url_for('admin.device_info',room_id=room_id))

        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.basic_info',room_id=room_id, is_editRoom=True))


        '''
        img360_base64=request.form.get('img360Src')
        image_decoder((img360_base64.split(','))[-1],
        f'app/static/images/test/room{room_id}/_360_upload.png')
        #rint(img360_base64)
        if continue_:
            return redirect(url_for('admin.device_info',room_id=room_id))
        '''

    #utils.download_room_360image_with_name(room_id)
    return render_template('admin_360_photo.html',
    room_id=room_id,
    is_addRoom=True if is_addRoom else False,
    is_editRoom=True if is_editRoom else False)


# #devices_dict = {}
# #from objects_admin import *
# type_dict={
#     0:{'name':'Microphone'},
#     1:{'name':'Projector'},
#     2:{'name':'Screener'},
# }

@admin_blue.route("/device_info", methods=['POST','GET'])
@check_login 
def device_info():
    room_id = request.args.get('room_id')
    #global devices_test_admin  # Three point initalization
    #devices_dict[room_id] = devices_test_admin

    if request.method == "POST":
        continue_=request.form.get('continue')
        checklist=request.form.get('checkList')
        if continue_:
            return redirect(url_for('admin.room_instruction_preview',room_id=room_id))
        if checklist:
            return redirect(url_for('admin.device_list',room_id=room_id))
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.photo_360',room_id=room_id, is_editRoom=True))
        
        #update_from_admin_request(devices_dict[room_id])
        
        point_delete=request.form.get('point_delete')
        point_edit=request.form.get('point_edit')
        point_close=request.form.get('point_close')

        #deviceID=request.form.get('uid')
        deviceName_old=request.form.get('point_name') 
        deviceName=request.form.get('p_name')
        deviceType=request.form.get('p_type')
        deviceIP=request.form.get('p_ip')
        deviceLocX=request.form.get('dup_x')
        deviceLocY=request.form.get('dup_y')
        # print(deviceName_old,deviceName,deviceType,deviceIP,deviceLocX,deviceLocY)
        print(deviceType)

        #save
        #print(point_edit, deviceName, deviceType, deviceIP)
        #print(point_edit and deviceName and deviceType and deviceIP)
        if point_edit and deviceName and deviceType and deviceIP:
            deviceID = roomdb.getDeviceID(room_id, deviceName_old)
            roomdb.addDevice(room_id, deviceID, deviceName, deviceType, deviceID)
            roomdb.clearChooseDeviceIDList(room_id)
            # utils.udpate_device_with_name_type_ip(
            #     room=room_id,
            #     old_name=deviceName_old,
            #     new_name=deviceName,
            #     type=deviceType,
            #     ip=deviceIP
            # )
            # utils.clean_chosen_device(room_id)
        
        #delete
        if point_delete and deviceName:
            deviceID = roomdb.getDeviceID(room_id, deviceName)
            roomdb.delDevice(room_id, deviceID)
            # utils.delete_device_with_name(room_id, deviceName)

        #create
        if deviceLocX and deviceLocY:
            roomdb.addDevice(room_id, "-1", deviceName, deviceType, deviceIP, round(float(deviceLocX),1), round(float(deviceLocY),1))
            deviceID = roomdb.getDeviceID(room_id, deviceName)
            roomdb.chooseDevice(room_id, deviceID)
            # utils.create_device_with_name_type_ip(
            #     room=room_id,
            #     name=deviceName,
            #     type=deviceType,
            #     ip=deviceIP,
            #     x=round(float(deviceLocX),1),
            #     y=round(float(deviceLocY),1)
            # )
            # utils.choose_device_with_name(room_id, deviceName)

        #choose
        choose = roomdb.getChooseDeviceList(room_id)
        # choose=utils.get_choose_device_with_room(room_id)
        for _, c in choose.items():
            d = request.form.get('devices_input_' + c[0])
            if d == ' ':
                roomdb.clearChooseDeviceIDList(room_id)
                # print(c[0])
                deviceID = roomdb.getDeviceID(room_id, c[0])
                # print(deviceID)
                roomdb.chooseDevice(room_id, deviceID)
                # utils.clean_chosen_device(room_id)
                # utils.choose_device_with_name(room_id, c[0])

        #close
        if point_close: roomdb.clearChooseDeviceIDList(room_id)
            # utils.clean_chosen_device(room_id)
    room = roomdb.getroom(room_id)
    devices = roomdb.getDeviceInfo(room_id)
    devices_choose = roomdb.getChooseDeviceList(room_id)
    type_dict = systemdb.getDeviceTypeList(room["controlSystem"])
    # print(type_dict)
    # devices, devices_choose=utils.get_devices_and_chosen_devices(room_id)
    print(devices)
    print(devices_choose)
    #return render_template('admin_device_info.html',room_id=room_id,devices=devices_dict[room_id].getJson(),devices_choose=devices_dict[room_id].chooseDevice())
    return render_template('admin_device_info.html',room_id=room_id,devices=devices,devices_choose=devices_choose,type_dict=type_dict)

@admin_blue.route("/device_list", methods=['GET','POST'])
def device_list():
    room_id = request.args.get('room_id')
    if request.method == "POST":
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.device_info',room_id=room_id))
    devices = roomdb.getDeviceInfo(room_id)
    # devices=utils.get_all_devices_with_room(room_id)
    #return render_template('admin_device_list.html',room_id=room_id,devices=devices_dict[room_id].getJson())
    return render_template('admin_device_list.html',room_id=room_id,devices=devices)

@admin_blue.route("/room_instruction_preview", methods=['GET', 'POST'])
@check_admin
def room_instruction_preview():
    room_id = request.args.get('room_id')
    return room_id

@admin_blue.route("/control", methods=['GET', 'POST'])
# @check_admin
def control():

    type_dict=systemdb.getSystemList()

    if request.method == "POST":
        system_id=request.form.get('cs-name')
        if system_id and system_id != "":
            systemdb.createSystem(system_id)
            return redirect(url_for('admin.control'))

        for cs_id in type_dict.keys():
            # edit
            if request.form.get(f'edit_{cs_id}'):
                #print("edit", step_id)
                return redirect(url_for('admin.control_device', system_id=type_dict[cs_id]))
            # delete
            if request.form.get(f'delete_{cs_id}'):
                #print("delete", step_id)
                systemdb.delSystem(type_dict[cs_id])
                return redirect(url_for('admin.control'))
        
        confirm = request.form.get('confirm')
        if confirm:
            return redirect(url_for('admin.main'))

    return render_template('admin_control_list.html', type_dict=type_dict)

@admin_blue.route("/control_device", methods=['GET', 'POST'])
# @check_admin
def control_device():
    system_id = request.args.get('system_id')
    type_dict = systemdb.getDeviceTypeList(system_id)
    if request.method == "POST":
        deviceType = request.form.get('device-type')
        print(deviceType)
        if deviceType and deviceType != "":
            systemdb.addDeviceType(system_id, deviceType)
            return redirect(url_for('admin.control_device', system_id=system_id))

        confirm = request.form.get('confirm')
        if confirm:
            return redirect(url_for('admin.control_case', system_id=system_id))

        for type_id in type_dict.keys():
            # delete
            if request.form.get(f'delete_{type_id}'):
                systemdb.delDeviceType(system_id, type_dict[type_id])
                return redirect(url_for('admin.control_device', system_id=system_id))
    return render_template('admin_control_device_list.html',system_id=system_id, type_dict=type_dict)

@admin_blue.route("/control_case", methods=['GET', 'POST'])
# @check_admin
def control_case():
    system_id = request.args.get('system_id')
    type_dict = systemdb.getInsDeviceList(system_id)
    
    # print(type_dict)
    if request.method == "POST":
        addbtn = request.form.get('add-case')
        if addbtn:
            system = systemdb.getsystem(system_id)
            return redirect(url_for('admin.control_case_instruction', system_id=system_id, case_id=len(system["insDevice"])))

        for insCase_id in type_dict.keys():
            if request.form.get(f'edit_{insCase_id}'):
                return redirect(url_for('admin.control_case_instruction', system_id=system_id, case_id=insCase_id))
            if request.form.get(f'delete_{insCase_id}'):
                systemdb.deleteCase(system_id, insCase_id)
                return redirect(url_for('admin.control_case', system_id=system_id))

        confirm = request.form.get('confirm')
        if confirm:
            return redirect(url_for('admin.control'))

    return render_template('admin_control_case_list.html',system_id=system_id, type_dict=type_dict)

@admin_blue.route("/control_case_instruction", methods=['GET', 'POST'])
# @check_admin
def control_case_instruction():
    system_id = request.args.get('system_id')
    case_id = request.args.get('case_id')
    type_dict = systemdb.getDeviceTypeList(system_id)
    steps = systemdb.getInsCaseSteps(system_id, case_id)
    
    # print(steps)

    if request.method == "POST":
        addbtn = request.form.get('add-step')
        if addbtn:
            system = systemdb.getsystem(system_id)
            if str(case_id) not in system["insCases"]: length = 0
            else: length = len(system["insCases"][str(case_id)])

            return redirect(url_for('admin.control_case_steps', system_id=system_id, case_id=case_id, step_id=length))

        for insStep_id in steps.keys():
            if request.form.get(f'edit_{insStep_id}'):
                return redirect(url_for('admin.control_case_steps', system_id=system_id, case_id=case_id, step_id=insStep_id))
            if request.form.get(f'delete_{insStep_id}'):
                systemdb.delCaseStep(system_id, case_id, insStep_id)
                return redirect(url_for('admin.control_case_instruction', system_id=system_id, case_id=case_id))
        
        # for k, v in type_dict.items():
        #     device_temp = request.form.get(f'Device_{k}')
        #     print(k, device_temp)

        confirm = request.form.get('confirm')
        if confirm:
            device_list = []
            for k, v in type_dict.items():
                device_temp = request.form.get(f'Device_{k}')
                print(k, device_temp)
                if device_temp: device_list.append(v)
            systemdb.addCaseDevice(system_id, case_id, device_list)
            print(device_list)

            return redirect(url_for('admin.control_case',system_id=system_id))

    system = systemdb.getsystem(system_id)
    choose_dev = {}
    for k, v in type_dict.items():
        if str(case_id) not in system["insDevice"]: break
        if v in system["insDevice"][str(case_id)]: choose_dev[k] = v

    return render_template('admin_control_case_instruction.html',
                            case_id=case_id,
                            system_id=system_id,
                            steps=steps,
                            type_dict=type_dict,
                            choose_dev=choose_dev)

@admin_blue.route("/control_case_steps", methods=['GET', 'POST'])
# @check_admin
def control_case_steps():
    system_id = request.args.get('system_id')
    case_id = request.args.get('case_id')
    step_id = request.args.get('step_id')
    steps = systemdb.getInsCaseSteps(system_id, case_id)

    if request.method == "POST":
        step_text = request.form.get('step_text')
        img_base64 = request.form.get('imgSrc')
        step_image=(img_base64.split(','))[-1]

        confirm = request.form.get('confirm')
        if confirm:
            systemdb.addCaseStep(system_id, str(case_id), str(step_id), step_text, step_image)
            return redirect(url_for('admin.control_case_instruction', system_id=system_id, case_id=case_id))
    print(steps)
    return render_template('admin_control_case_steps.html',system_id=system_id, case_id=case_id, step_id=step_id, steps=steps, \
         _text = "Please add text to describe this step." if step_id not in steps else steps[step_id]["text"])
