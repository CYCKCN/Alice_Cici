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
    '''
    roomInfo={
        0:{'name':'5554','lift':'27-28','date':'August 21','time':'19:00-21:00'},
        1:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        2:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        3:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        4:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        5:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
        6:{'name':'4223','lift':'23','date':'September 21','time':'1:00-3:00'},
    }'''
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
            print(deviceName)
            deviceID = roomdb.getDeviceID(room_id, deviceName)
            print("DDDD")
            print(deviceID)
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
                print(c[0])
                deviceID = roomdb.getDeviceID(room_id, c[0])
                print(deviceID)
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

steps={
    'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
    'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
    'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
    'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
    'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
}

device111={
    'Device 1':{'name':'device 1'},
    'Device 2':{'name':'device 2'},
    'Device 3':{'name':'device 3'},
    'Device 4':{'name':'device 4'},
    'Device 5':{'name':'device 5'},
    'Apple':{'name':'Apple'},
    'Windows':{'name':'Windows'},
}

cases={
    'Case 1':{
        'devices':{
            'device 1':{'name':'device 1'},
            'device 3':{'name':'device 3'},
            'device 5':{'name':'device 5'},
        },
        'steps':{
            'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
        }
    },
    'Case 2':{
        'devices':{
            'device 2':{'name':'device 2'},
            'device 4':{'name':'device 4'},
        },
        'steps':{
            'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
        }
    },
    'Case 3':{
        'devices':{
        },
        'steps':{
            'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
            'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
        }
    }
}

@admin_blue.route("/control", methods=['GET', 'POST'])
# @check_admin
def control():
    type_dict=systemdb.getSystemList()
    print(type_dict)
    return render_template('admin_control_list.html', type_dict=type_dict)

@admin_blue.route("/control_device", methods=['GET', 'POST'])
@check_admin
def control_device():
    room_id = request.args.get('room_id')
    return render_template('admin_control_device_list.html',room_id=room_id,steps=steps)

@admin_blue.route("/control_case", methods=['GET', 'POST'])
@check_admin
def control_case():
    room_id = request.args.get('room_id')
    return render_template('admin_control_case_list.html',room_id=room_id,steps=steps)

@admin_blue.route("/control_case_instruction", methods=['GET', 'POST'])
@check_admin
def control_case_instruction():
    room_id = request.args.get('room_id')
    return render_template('admin_control_case_instruction.html',
                            case_id="Case 1",
                            room_id=room_id,
                            steps=steps,
                            device111=device111,
                            choose_dev=cases['Case 1']['devices'])

@admin_blue.route("/control_case_steps", methods=['GET', 'POST'])
@check_admin
def control_case_steps():
    room_id = request.args.get('room_id')
    return render_template('admin_control_case_steps.html',room_id=room_id,steps=steps)

# '''
# steps={
#    'step 1':{'text':'Find the HDMI cable underneath the conference table', 'image':'', 'command':"print('instruction_initial_list')\r\nprint(steps)", 'help':''},
#    'step 2':{'text':'Find the HDMI cable underneath the conference table', 'image':'8bdd60db4a154e428fd47f7d857b8cf9', 'command':"print('instruction_initial_list')\r\nprint(steps)", 'help':'helpxxxxxxxx xxxxxxxxxxxxxxx xxxxxxxxxxxx xxxxxxxxxxxx xxxxxxxxxxx'},
#    'step 3':{'text':'Plug the HDMI cable to your laptop', 'image':'8bdd60db4a154e428fd47f7d857b8cf9', 'command':'', 'help':''},
# }
# '''
# @admin_blue.route("/instruction_initial_list", methods=['POST','GET'])
# def instruction_initial_list():
#     room_id = request.args.get('room_id')
#     #print("instruction_initial_list")
#     #print(steps)
#     #print(devices_dict)
#     step=utils.get_instruction_init_step(room_id)

#     if request.method == "POST":
#         # add
#         if request.form.get(f'add-step'):
#             #print("add")
#             step_length = f"step {len(step.keys())+1}"
#             #new_dict = {step_length:{'text':'', 'image':'', 'command':'', 'help':''}}
#             #steps.update(new_dict)
#             #print(steps)
#             utils.add_instruction_init_step(room_id,step_length)
#             return redirect(url_for('admin.instruction_initial',room_id=room_id,step_id=step_length))
        
#         #for step_id in steps.keys():
#         for step_id in step.keys():
#             # edit
#             if request.form.get(f'edit_{step_id}'):
#                 #print("edit", step_id)
#                 return redirect(url_for('admin.instruction_initial',room_id=room_id,step_id=step_id))
#             # delete
#             if request.form.get(f'delete_{step_id}'):
#                 #print("delete", step_id)
#                 utils.delete_instruction_init_step(room_id,step_id)
#                 step=utils.get_instruction_init_step(room_id)
#                 return render_template('admin_instruction_initial_list.html',room_id=room_id,steps=step)
#         confirm=request.form.get('confirm')
#         if  confirm:
#             return redirect(url_for('admin.instruction_turnon_main',room_id=room_id))
#         back=request.form.get('back')
#         if back:
#             return redirect(url_for('admin.device_info',room_id=room_id))
    
#     #return render_template('admin_instruction_initial_list.html',room_id=room_id,steps=steps)
#     return render_template('admin_instruction_initial_list.html',room_id=room_id,steps=step)

# @admin_blue.route("/instruction_initial", methods=['POST','GET'])
# def instruction_initial():
#     #print("instruction_initial")
#     #print(devices_dict)
#     #print(steps)
#     room_id = request.args.get('room_id')
#     step_id = request.args.get('step_id')
#     if request.method == "POST":
#         step_text=request.form.get('step_text') if not request.form.get('step_text')=='' else None
#         img_base64=request.form.get('imgSrc')
#         step_command=request.form.get('step_command') if not request.form.get('step_command')=='' else None
#         step_help=request.form.get('step_help') if not request.form.get('step_help')=='' else None
#         step_image=(img_base64.split(','))[-1] if img_base64 else None
#         #print(step_text)
#         #print(img_base64)
#         #print(step_command)
#         #print(step_help)
#         confirm=request.form.get('confirm')
#         if confirm:
#             #steps[step_id]["text"]=step_text
#             #steps[step_id]["image"]=img_base64  # debug
#             #steps[step_id]["command"]=step_command
#             #steps[step_id]["help"]=step_help
#             #print(steps)
#             utils.update_instruction_init_step(
#                 name=room_id,
#                 id=step_id,
#                 text=step_text,
#                 image=step_image,
#                 com=step_command,
#                 help=step_help
#             )
#             return redirect(url_for('admin.instruction_initial_list',room_id=room_id))
    
#     step=utils.get_instruction_init_step(room_id)
#     return render_template('admin_instruction_initial.html',room_id=room_id,step_id=step_id,steps=step)

# @admin_blue.route("/instruction_turnon_main", methods=['POST','GET'])
# def instruction_turnon_main(): 
#     room_id = request.args.get('room_id')
#     #print(devices_dict)
#     devices=utils.get_all_devices_with_room(room_id)
#     if request.method == "POST":
#         #for device_id in range(0, len(devices_dict[room_id].devices)):
#         for device_id, device_info in devices.items():
#             # edit
#             if request.form.get(f'edit_{device_id}'):
#                 print("edit", device_id)
#                 device_id+=1
#                 return redirect(url_for('admin.instruction_turnon_list',
#                                         room_id=room_id,
#                                         device_id=device_id,
#                                         device_name=device_info['name']
#                                     ))
#         confirm=request.form.get('confirm')
#         if confirm:
#             return redirect(url_for('admin.instruction_pair_main',room_id=room_id))
#             #return redirect(url_for('admin.instruction_pair_main',devices_obj=devices_dict[room_id],room_id=room_id))
#         back=request.form.get('back')
#         if back:
#             return redirect(url_for('admin.instruction_initial_list',room_id=room_id))
#     #return render_template('admin_instruction_turnon_main.html',devices_obj=devices_dict[room_id],room_id=room_id)
#     return render_template('admin_instruction_turnon_main.html',devices=devices,room_id=room_id)

# @admin_blue.route("/instruction_turnon_list", methods=['POST','GET'])
# def instruction_turnon_list():  
#     room_id = request.args.get('room_id')
#     device_id = request.args.get('device_id')
#     device_name = request.args.get('device_name')
#     #print("instruction_turnon_list")
#     #print(steps)
#     steps=utils.get_instruction_turnon_step(room_id,device_name)
#     if request.method == "POST":
#         # add
#         if request.form.get(f'add-step'):
#             #print("add")
#             step_length = f"step {len(steps.keys())+1}"
#             #new_dict = {step_length:{'text':'', 'image':'', 'command':'', 'help':''}}
#             #steps.update(new_dict)
#             #print(steps)
#             utils.add_instruction_turnon_step(room_id,device_name,step_length)
#             return redirect(url_for('admin.instruction_turnon',
#                             device_id=device_id,
#                             room_id=room_id,
#                             step_id=step_length,
#                             device_name=device_name
#                         ))
        
#         for step_id in steps.keys():
#             # edit
#             if request.form.get(f'edit_{step_id}'):
#                 #print("edit", step_id)
#                 # not implemented delete function
#                 return redirect(url_for('admin.instruction_turnon',
#                                 device_id=device_id,
#                                 room_id=room_id,
#                                 step_id=step_id,
#                                 device_name=device_name
#                             ))
#             # delete
#             if request.form.get(f'delete_{step_id}'):
#                 #print("delete", step_id)
#                 utils.delete_instruction_turnon_step(room_id,device_name,step_id)
#                 steps=utils.get_instruction_turnon_step(room_id,device_name)
#                 return render_template('admin_instruction_turnon_list.html',
#                                         device_id=device_id,
#                                         room_id=room_id,
#                                         steps=steps,
#                                         device_name=device_name)
#         confirm=request.form.get('confirm')
#         if confirm:
#             return redirect(url_for('admin.instruction_turnon_main',room_id=room_id))
#             #return redirect(url_for('admin.instruction_turnon_main',devices_obj=devices_dict[room_id],room_id=room_id))
#     return render_template('admin_instruction_turnon_list.html',device_id=device_id,room_id=room_id,steps=steps,device_name=device_name)

# @admin_blue.route("/instruction_turnon", methods=['POST','GET'])
# def instruction_turnon():
#     #print("instruction_turnon")
#     #print(steps)
#     room_id = request.args.get('room_id')
#     step_id = request.args.get('step_id')
#     device_id = request.args.get('device_id')
#     device_name = request.args.get('device_name')
#     if request.method == "POST":
#         step_text=request.form.get('step_text') if not request.form.get('step_text')=='' else None
#         img_base64=request.form.get('imgSrc')
#         step_command=request.form.get('step_command') if not request.form.get('step_command')=='' else None
#         step_help=request.form.get('step_help') if not request.form.get('step_help')=='' else None
#         step_image=(img_base64.split(','))[-1] if img_base64 else None
#         #print(step_text)
#         #print(img_base64)
#         #print(step_command)
#         #print(step_help)
#         confirm=request.form.get('confirm')
#         if confirm:
#             #steps[step_id]["text"]=step_text
#             #steps[step_id]["image"]=img_base64  # debug
#             #steps[step_id]["command"]=step_command
#             #steps[step_id]["help"]=step_help
#             #print(steps)
#             utils.update_instruction_turnon_step(
#                 room_name=room_id,
#                 device_name=device_name,
#                 id=step_id,
#                 text=step_text,
#                 image=step_image,
#                 com=step_command,
#                 help=step_help
#             )
#             return redirect(url_for('admin.instruction_turnon_list',device_id=device_id,room_id=room_id,device_name=device_name))
    
#     steps=utils.get_instruction_turnon_step(room_id,device_name)
#     return render_template('admin_instruction_turnon.html',device_id=device_id,room_id=room_id,step_id=step_id,steps=steps,device_name=device_name)

# @admin_blue.route("/instruction_zoom_main", methods=['POST','GET'])
# def instruction_zoom_main(): 
#     room_id = request.args.get('room_id')
#     video=request.form.get('edit_VIDEO')
#     if request.method == "POST":
#         if video:
#             return redirect(url_for('admin.instruction_zoom_list',zoom_type='Video', room_id=room_id))
#         audio=request.form.get('edit_AUDIO')
#         if audio:
#             return redirect(url_for('admin.instruction_zoom_list',zoom_type='Audio', room_id=room_id))
#         confirm=request.form.get('confirm')
#         if  confirm:
#             return redirect(url_for('admin.room',room_id=room_id))
#         back=request.form.get('back')
#         if back:
#             #return redirect(url_for('admin.instruction_pair_main',devices_obj=devices_dict[room_id],room_id=room_id))
#             return redirect(url_for('admin.instruction_pair_main',room_id=room_id))
#     utils.create_instruction_zoom(room_id)
#     return render_template('admin_instruction_zoom_main.html',room_id=room_id)

# @admin_blue.route("/instruction_zoom_list", methods=['POST','GET'])
# def instruction_zoom_list():  
#     room_id = request.args.get('room_id')
#     zoom_type = request.args.get('zoom_type')
#     #print("instruction_zoom_list")
#     #print(steps)
#     steps=utils.get_instruction_zoom_step(room_id,zoom_type)

#     if request.method == "POST":
#         # add
#         if request.form.get(f'add-step'):
#             #print("add")
#             step_length = f"step {len(steps.keys())+1}"
#             #new_dict = {step_length:{'text':'', 'image':'', 'command':'', 'help':''}}
#             #steps.update(new_dict)
#             #print(steps)
#             utils.add_instruction_zoom_step(room_id,zoom_type,step_length)
#             return redirect(url_for('admin.instruction_zoom',room_id=room_id,step_id=step_length,zoom_type=zoom_type))
        
#         for step_id in steps.keys():
#             # edit
#             if request.form.get(f'edit_{step_id}'):
#                 #print("edit", step_id)
#                 # not implemented delete function
#                 return redirect(url_for('admin.instruction_zoom',room_id=room_id,step_id=step_id,zoom_type=zoom_type))
#             # delete
#             if request.form.get(f'delete_{step_id}'):
#                 #print("delete", step_id)
#                 utils.delete_instruction_zoom_step(room_id,zoom_type,step_id)
#                 steps=utils.get_instruction_zoom_step(room_id,zoom_type)
#                 return render_template('admin_instruction_zoom_list.html',room_id=room_id,steps=steps,zoom_type=zoom_type)
#         confirm=request.form.get('confirm')
#         if  confirm:
#             return redirect(url_for('admin.instruction_zoom_main',room_id=room_id,steps=steps, zoom_type=zoom_type))
#     return render_template('admin_instruction_zoom_list.html',room_id=room_id,steps=steps, zoom_type=zoom_type)

# @admin_blue.route("/instruction_zoom", methods=['POST','GET'])
# def instruction_zoom():
#     #print("instruction_zoom")
#     #print(steps)
#     room_id = request.args.get('room_id')
#     step_id = request.args.get('step_id')
#     zoom_type = request.args.get('zoom_type')
#     if request.method == "POST":
#         step_text=request.form.get('step_text') if not request.form.get('step_text')=='' else None
#         img_base64=request.form.get('imgSrc')
#         step_command=request.form.get('step_command') if not request.form.get('step_command')=='' else None
#         step_help=request.form.get('step_help') if not request.form.get('step_help')=='' else None
#         step_image=(img_base64.split(','))[-1] if img_base64 else None
#         #print(step_text)
#         #print(img_base64)
#         #print(step_command)
#         #print(step_help)
#         confirm=request.form.get('confirm')
#         if confirm:
#             #steps[step_id]["text"]=step_text
#             #steps[step_id]["image"]=img_base64  # debug
#             #steps[step_id]["command"]=step_command
#             #steps[step_id]["help"]=step_help
#             #print(steps)
#             utils.update_instruction_zoom_step(
#                 room_name=room_id,
#                 zoom_type=zoom_type,
#                 step_name=step_id,
#                 text=step_text,
#                 image=step_image,
#                 com=step_command,
#                 help=step_help
#             )
#             return redirect(url_for('admin.instruction_zoom_list',room_id=room_id,zoom_type=zoom_type))
    
#     steps=utils.get_instruction_zoom_step(room_id,zoom_type)
#     return render_template('admin_instruction_zoom.html',room_id=room_id,step_id=step_id,steps=steps,zoom_type=zoom_type)
# '''
# cases={
#     'Case 1':{
#         'devices':{
#             'device 1':{'name':'device 1'},
#             'device 3':{'name':'device 3'},
#             'device 5':{'name':'device 5'},
#         },
#         'steps':{
#             'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
#         }
#     },
#     'Case 2':{
#         'devices':{
#             'device 2':{'name':'device 2'},
#             'device 4':{'name':'device 4'},
#         },
#         'steps':{
#             'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
#         }
#     },
#     'Case 3':{
#         'devices':{
#         },
#         'steps':{
#             'step 1':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 2':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 3':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 4':{'text':'', 'image':'', 'command':'', 'help':''},
#             'step 5':{'text':'', 'image':'', 'command':'', 'help':''},
#         }
#     }
# }

# '''
# @admin_blue.route("/instruction_pair_main", methods=['POST','GET'])
# def instruction_pair_main():
#     room_id = request.args.get('room_id')
#     #print("instruction_pair_main")
#     cases=utils.get_instruction_pair_case(room_id)

#     if request.method == "POST":
#         # add
#         if request.form.get(f'add-step'):
#             #print("add")
#             case_length = f"case {len(cases.keys())+1}"
#             #new_dict = {case_length:{'devices':'', 'steps':''}}
#             #cases.update(new_dict)
#             #print(cases)
#             utils.add_instruction_pair_case(room_id,case_length)
#             return redirect(url_for('admin.instruction_pair_list',room_id=room_id,case_id=case_length))
        
#         for case_id in cases.keys():
#             # edit
#             if request.form.get(f'edit_{case_id}'):
#                 #print("edit", case_id)
#                 return redirect(url_for('admin.instruction_pair_list',room_id=room_id,case_id=case_id))
#             # delete
#             if request.form.get(f'delete_{case_id}'):
#                 #print("delete", case_id)
#                 utils.delete_instruction_pair_case(room_id,case_id)
#                 cases=utils.get_instruction_pair_case(room_id)
#                 return render_template('admin_instruction_pair_main.html',room_id=room_id,cases=cases)
#         confirm=request.form.get('confirm')
#         if  confirm:
#             return redirect(url_for('admin.instruction_zoom_main',room_id=room_id))
#         back=request.form.get('back')
#         if back:
#             return redirect(url_for('admin.instruction_turnon_main',room_id=room_id))
    
#     return render_template('admin_instruction_pair_main.html',room_id=room_id,cases=cases)

# #dev_choose_idx_list=set()
# @admin_blue.route("/instruction_pair_list", methods=['POST','GET'])
# def instruction_pair_list():  
#     room_id = request.args.get('room_id')
#     case_id = request.args.get('case_id')
#     #print("instruction_turnon_list")
#     #print(steps)
#     cases=utils.get_instruction_pair_case(room_id)
#     steps=utils.get_instruction_pair_case_step(room_id,case_id)
#     device111=utils.get_instruction_pair_case_device(room_id,case_id)
#     #choose_dev=utils.get_instruction_pair_case_chosen_device(room_id,case_id)

#     if request.method == "POST":
#         # add
#         if request.form.get(f'add-step'):
#             #print("add")
#             step_length = f"step {len(steps.keys())+1}"
#             #new_dict = {step_length:{'text':'', 'image':'', 'command':'', 'help':''}}
#             #steps.update(new_dict)
#             #print(steps)
#             utils.add_instruction_pair_case_step(room_id,case_id,step_length)
#             return redirect(url_for('admin.instruction_pair',case_id=case_id,room_id=room_id,step_id=step_length))
        
#         for step_id in steps.keys():
#             # edit
#             if request.form.get(f'edit_{step_id}'):
#                 #print("edit", step_id)
#                 # not implemented delete function
#                 return redirect(url_for('admin.instruction_pair',case_id=case_id,room_id=room_id,step_id=step_id))
#             # delete
#             if request.form.get(f'delete_{step_id}'):
#                 #print("delete", step_id)
#                 utils.delete_instruction_pair_case_step(room_id,case_id,step_id)
#                 steps=utils.get_instruction_pair_case_step(room_id,case_id)
#                 return render_template('admin_instruction_pair_list.html',
#                             case_id=case_id,
#                             room_id=room_id,
#                             steps=steps,
#                             device111=device111,
#                             choose_dev=cases[case_id]['devices'])
#         '''
#         i=0
#         for k, v in device111.items():
#             device_temp=request.form.get(f'Device_{k}')
#             if device_temp:
#                 dev_choose_idx_list.add(i)
#             elif i in dev_choose_idx_list:
#                 dev_choose_idx_list.remove(i)
#             i+=1
#         '''
        
#         '''
#         for i, k, v in enumerate(device111.items()):
#             device_temp=request.form.get(f'Device_{k}')
#             if device_temp:
#                 dev_choose_idx_list.add(i)
#             elif i in dev_choose_idx_list:
#                 dev_choose_idx_list.remove(i)
#         '''
#         #print(dev_choose_idx_list)
        
        
#         confirm=request.form.get('confirm')
#         if confirm:
#             for k, v in device111.items():
#                 device_temp=request.form.get(f'Device_{k}')
#                 if device_temp:
#                     utils.choose_instruction_pair_device(room_id,case_id,k,v['name'])
#                 else:
#                     utils.undo_choose_instruction_pair_device(room_id,case_id,k,v['name'])

#             #print(cases)
#             #choose_dev=utils.get_instruction_pair_case_chosen_device(room_id,case_id)
#             return redirect(url_for('admin.instruction_pair_main',room_id=room_id))
#     #return render_template('admin_instruction_pair_list.html',case_id=case_id,room_id=room_id,steps=steps,device111=device111,choose_dev=cases[case_id]['devices'])
#     return render_template('admin_instruction_pair_list.html',
#                         case_id=case_id,
#                         room_id=room_id,
#                         steps=steps,
#                         device111=device111,
#                         choose_dev=cases[case_id]['devices'])

# @admin_blue.route("/instruction_pair", methods=['POST','GET'])
# def instruction_pair():
#     #print("instruction_pair")
#     #print(steps)
#     room_id = request.args.get('room_id')
#     step_id = request.args.get('step_id')
#     case_id = request.args.get('case_id')
#     if request.method == "POST":
#         step_text=request.form.get('step_text') if not request.form.get('step_text')=='' else None
#         img_base64=request.form.get('imgSrc')
#         step_command=request.form.get('step_command') if not request.form.get('step_command')=='' else None
#         step_help=request.form.get('step_help') if not request.form.get('step_help')=='' else None
#         step_image=(img_base64.split(','))[-1] if img_base64 else None
#         #print(step_text)
#         #print(img_base64)
#         #print(step_command)
#         #print(step_help)
#         confirm=request.form.get('confirm')
#         if confirm:
#             #steps[step_id]["text"]=step_text
#             #steps[step_id]["image"]=img_base64  # debug
#             #steps[step_id]["command"]=step_command
#             #steps[step_id]["help"]=step_help
#             #print(steps)
#             utils.update_instruction_pair_case_step(
#                 room_name=room_id,
#                 case_name=case_id,
#                 step_name=step_id,
#                 text=step_text,
#                 image=step_image,
#                 com=step_command,
#                 help=step_help
#             )
#             return redirect(url_for('admin.instruction_pair_list',case_id=case_id,room_id=room_id))
    
#     steps=utils.get_instruction_pair_case_step(room_id,case_id)
#     return render_template('admin_instruction_pair.html',case_id=case_id,room_id=room_id,step_id=step_id,steps=steps)

@admin_blue.route("/profile", methods=['POST','GET'])
def profile():
    if request.method == "POST":
        btn_profile=request.form.get('profile')
        if btn_profile:
            return redirect(url_for('admin.main'))
        logout=request.form.get('logout')
        if logout:
            return redirect(url_for('admin.logout'))
        back=request.form.get('back')
        if back:
            return redirect(url_for('admin.main'))
    
    return render_template('admin_profile.html')

# @admin_blue.route("/guest-invite", methods=['POST','GET'])
# def guest_invite():
#     if request.method == "POST":
#         pass

#     return render_template('guest-invite.html')

# '''
# @admin_blue.route("/initial", methods=['POST','GET'])
# def initial():
#     print("initial")
#     print(steps)
#     room_id = request.args.get('room_id')
#     if request.method == "POST":
#         next=request.form.get('next')
#         if next:
#             return redirect(url_for('admin.turnon',room_id=room_id))
#         back=request.form.get('back')
#         if back:
#             return redirect(url_for('admin.initial',room_id=room_id))
    
#     return render_template('instruction_initial.html',room_id=room_id,steps=steps)

# @admin_blue.route("/turnon", methods=['POST','GET'])
# def turnon():
#     print("turnon")
#     print(steps)
#     room_id = request.args.get('room_id')
#     if request.method == "POST":
#         next=request.form.get('next')
#         if next:
#             return redirect(url_for('admin.pair',room_id=room_id))
#         back=request.form.get('back')
#         if back:
#             return redirect(url_for('admin.initial',room_id=room_id))
    
#     return render_template('instruction_turnon.html',room_id=room_id,steps=steps)

# @admin_blue.route("/pair", methods=['POST','GET'])
# def pair():
#     print("pair")
#     print(steps)
#     room_id = request.args.get('room_id')
#     if request.method == "POST":
#         next=request.form.get('next')
#         if next:
#             return redirect(url_for('admin.zoom',room_id=room_id))
#         back=request.form.get('back')
#         if back:
#             return redirect(url_for('admin.turnon',room_id=room_id))
    
#     return render_template('instruction_pair.html',room_id=room_id,steps=steps)

# @admin_blue.route("/zoom", methods=['POST','GET'])
# def zoom():
#     print("zoom")
#     print(steps)
#     room_id = request.args.get('room_id')
#     if request.method == "POST":
#         next=request.form.get('next')
#         if next:
#             return redirect(url_for('admin.zoom',room_id=room_id))
#         back=request.form.get('back')
#         if back:
#             return redirect(url_for('admin.pair',room_id=room_id))
    
#     return render_template('instruction_zoom.html',room_id=room_id,steps=steps)
# '''