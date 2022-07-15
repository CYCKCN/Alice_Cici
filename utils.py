import os
import uuid
import shutil
from app import db
from app.img_trans import *

def path_exist_or_mkdir(path:str):
    #找地址 找不到就创建
    if not os.path.exists(path):
        os.makedirs(path)
    return True

#-----------------------------------------
#-------------- admin flow ---------------
#-----------------------------------------

#------------ Room utils ---------------

def find_room_with_name(name:str):
    #用name找room 找不到返回false
    _db=db['room']
    room=_db.find_one({'roomName':name})
    if room: return room
    else: return False

def room_is_exist(name:str):
    #检查room存不存在 存在true不存在false name不合法false
    if name==None:  return False
    _db=db['room']
    if _db.find_one({'roomName':name}): return True
    else: return False

def room_has_attribute(name:str,attr:str):
    _db=db['room']
    room=_db.find_one({'roomName':name,attr:{'$exists': True}})
    if room: return True
    else: return False

def get_room_location_with_name(name:str):
    room=find_room_with_name(name)
    return room['roomLoc']

def create_room_with_name_image_loc(name:str, image:str, loc:str):
    #用name image loc创建新的room
    exist=f'app/static/images/test/room{name}'
    path_exist_or_mkdir(exist)

    #if room['roomImage']==None: return False
    path=f'app/static/images/test/room{name}/_basic_upload.png'
    image_decoder(image,path)

    _db=db['room']
    _dict={
        'roomName':name,
        'roomImage':'_basic_upload',
        'roomLoc':loc,
        'bookBy':{},
        'bookTime':{}
    }
    _db.insert_one(_dict)
    return True

def update_room_with_name_image_loc(room_id:str ,name:str=None, image:str=None, loc:str=None):
    #room_id是现在这个room的名字
    #name是更改后房间的名字 image loc同理
    #name image loc可以全改或改几个 全都不改返回True
    #room_id当前房间的名字要是不存在 返回false
    #name更改后房间的名字存在会冲突 返回false
    if not room_is_exist(room_id): return False
    if room_is_exist(name): return False
    if name==None and image==None and loc==None: return True
    _db=db['room']
    room=find_room_with_name(room_id)
    _dict={}
    if name: _dict['roomName']=name
    if image: #_dict['roomImage']=image
        path=f'app/static/images/test/room{name}/_basic_upload.png'
        image_decoder(image,path)
    if loc: _dict['roomLoc']=loc
    _db.update_one(
        {'_id': room['_id']}, 
        {'$set': _dict}
    )
    return True

'''
def download_room_basic_image_with_name(name:str):
    #缓存当前房间basic的图片
    room=find_room_with_name(name)
    if room==None: return False
    exist=f'app/static/images/test/room{name}'
    path_exist_or_mkdir(exist)

    #if room['roomImage']==None: return False
    path=f'app/static/images/test/room{name}/_basic_upload.png'
    image_decoder(room['roomImage'],path)

    return True
'''

def get_all_room_basic():
    #date和time还没有加 后面记得加
    _db=db['room']
    if _db.count_documents({})==0: return False

    rooms=_db.find({})
    _dict={}
    i=0
    for room in rooms:
        _d={}
        _d['name']=room['roomName']
        _d['lift']=room['roomLoc']
        #_d['date']=
        #_d['time']=

        _dict[i]=_d
        #download_room_basic_image_with_name(_d['name'])
        i+=1
    
    return _dict

def delete_room_with_name(name:str):
    if name==None: return False
    if not room_is_exist(name): return False
    _db=db['room']
    _db.delete_one({'roomName':name})
    path=f'app/static/images/test/room{name}'

    path_exist_or_mkdir(path)
    shutil.rmtree(path)

    db['device'].delete_many({'roomName':name})

    return True

def add_room_360image_with_name(name:str,image:str=None):
    #print(name,len(image),room_is_exist(name))
    if name==None: return False
    if image==None: return True
    if not room_is_exist(name): return False

    exist=f'app/static/images/test/room{name}'
    path_exist_or_mkdir(exist)

    #if not room_has_attribute(name,'room360Image'): return False
    path=f'app/static/images/test/room{name}/_360_upload.png'
    image_decoder(image,path)
    #print(len(image),os.path.exists(path))

    _db=db['room']
    _db.update_one(
        {'roomName':name},
        {'$set':{'room360Image':'_360_upload'}}
    )
    return True

'''
def download_room_360image_with_name(name:str):
    if name==None: return False
    if not room_is_exist(name): return False
    room=find_room_with_name(name)
    exist=f'app/static/images/test/room{name}'
    path_exist_or_mkdir(exist)

    if not room_has_attribute(name,'room360Image'): return False
    path=f'app/static/images/test/room{name}/_360_upload.png'
    image_decoder(room['room360Image'],path)

    return True
'''

#------------ Device utils ---------------

#old version
def device_is_exist(room:str,id:int):
    _db=db['device']
    device=_db.find_one({'roomName':room,'deviceId':id})
    if device: return True
    else: return False

def create_device_with_room_id_name_type_x_y_id(
    room:str,name:str,type:str,x:float,y:float,ip:str):
    _db=db['device']
    _dict={
        'roomName':room,
        'deviceId':-1,
        'deviceName':name,
        'deviceType':type,
        'deviceIP':ip,
        'deviceLocX':x,
        'deviceLocY':y,
        'chosen':False
    }
    _db.insert_one(_dict)
    return True


def update_device_with_name_type_x_y_id(room:str,id:int,name:str=None,type:str=None,x:float=None,y:float=None,ip:str=None):
    _db=db['device']
    #if not device_is_exist(room,id): return False
    if name==None and name==None and type==None and x==None and y==None and ip==None: return True
    _dict={}
    _dict['deviceId']=id
    if name: _dict['deviceName']=name
    if type: _dict['deviceType']=type
    if x: _dict['deviceLocX']=x
    if y: _dict['deviceLocY']=y
    if ip: _dict['deviceIP']=ip
    _db.update_one(
        {'roomName':room, 'deviceId':id},
        {'$set':_dict}
    )
    return True

def choose_a_device_with_room_id(room:str,id:int):
    #if not device_is_exist(room,id): return False
    _db=db['device']
    _db.update_many(
        {'roomName':room},
        {'$set':{'chosen':False}}
    )
    _db.update_one(
        {'roomName':room, 'deviceId':id},
        {'$set':{'chosen':True}}
    )
    return True


def find_device_with_room_id(room:str,id:int):
    _db=db['device']
    device=_db.find_one({'roomName':room,'deviceId':id})
    if device: return device
    else: return False

def delete_device_with_room_id(room:str, id:int):
    _db=db['device']
    if not device_is_exist(room,id): return False
    device=find_device_with_room_id(room,id)
    _db.update_many({"deviceID": {'$gt': device["deviceID"]}}, {'$inc': {"deviceID": -1}})
    _db.delete_one({"_id": device["_id"]})
    return True
    
def delete_device_with_room_name(room:str, name:str):
    _db=db['device']
    device=_db.find_one({'roomName':room,'deviceName':name})
    if device==None: return False
    _db.update_many({"deviceID": {'$gt': device["deviceID"]}}, {'$inc': {"deviceID": -1}})
    _db.delete_one({"_id": device["_id"]})
    return True

def clean_choose_device_with_room(room:str):
    _db=db['device']
    _db.update_many(
        {'roomName':room},
        {'$set':{'chosen':False}}
    )
    return False

#new version: remove id
def device_has_attribute(room_name:str,device_name:str,attr:str):
    _db=db['device']
    device=_db.find_one({'roomName':room_name,'deviceName':device_name ,attr:{'$exists': True}})
    if device: return True
    else: return False

def udpate_device_with_name_type_ip(room:str, old_name:str, new_name:str, type:str, ip:str):
    _db=db['device']
    exist=_db.find_one({'roomName':room,'deviceName':new_name})
    if exist: return False
    _db.update_one(
        {'roomName':room, 'deviceName':old_name},
        {'$set':
            {'deviceName':new_name, 'deviceType':type, 'deviceIP':ip}
        }
    )
    return True

def delete_device_with_name(room:str, name:str):
    _db=db['device']
    _db.delete_one({'roomName':room, 'deviceName':name})
    return True

def create_device_with_name_type_ip(room:str, name:str, type:str, ip:str, x:float, y:float):
    _db=db['device']
    exist=_db.find_one({'roomName':room,'deviceName':name})
    if exist: return False
    _db.insert_one({
        'roomName':room,
        'deviceName':name,
        'deviceType':type,
        'deviceIP':ip,
        'deviceLocX':x,
        'deviceLocY':y,
        'chosen':False
    })
    return True

def choose_device_with_name(room:str, name:str):
    _db=db['device']
    _db.update_one(
        {'roomName':room, 'deviceName':name},
        {'$set':{'chosen':True}}
    )
    return True

def get_all_devices_with_room(name:str):
    _db=db['device']

    _dict={}
    if _db.count_documents({'roomName':name})==0: return _dict
    devices=_db.find({'roomName':name})
    
    for device in devices:
        _d={
            'name':device['deviceName'],
            'type':device['deviceType'],
            'ip':device['deviceIP'],
            'x':device['deviceLocX'],
            'y':device['deviceLocY']
        }
        _dict[len(_dict)]=_d
    return _dict

def get_choose_device_with_room(room:str):
    _db=db['device']
    _dict={}
    if _db.count_documents({'roomName':room})==0: return _dict
    devices=_db.find({'roomName':room})
    for device in devices:
        if not device_has_attribute(room,device['deviceName'],'chosen'):
            _db.update_one(
                {'roomName':room, 'deviceName':device['deviceName']},
                {'$set':{'chosen':False}}
            )
            _dict[len(_dict)]=[device['deviceName'], 0]
            continue

        if device['chosen']:
            _dict[len(_dict)]=[device['deviceName'], 1]
        else:
            _dict[len(_dict)]=[device['deviceName'], 0]
    return _dict

def get_devices_and_chosen_devices(room:str):
    devices=get_all_devices_with_room(room)
    devices_choose=get_choose_device_with_room(room)
    return devices, devices_choose

def clean_chosen_device(room:str):
    _db=db['device']
    _db.update_many(
        {'roomName':room},
        {'$set':{'chosen':False}}
    )
    return True

#------------ Instruction utils ---------------

#------ Instruction init --------
def get_instruction_init_step(name:str):
    _db=db['room']
    room=_db.find_one({"roomName": name})
    if room_has_attribute(name,'insInitial'):
        return room['insInitial']
    else:
        return {}

def add_instruction_init_step(name:str,id:str):
    _db=db['room']
    room=_db.find_one({"roomName": name})
    add={
        id:{'text':'', 'image':'', 'command':'', 'help':''}
    }
    if room_has_attribute(name,'insInitial'):
        ins=room['insInitial']
        ins.update(add)
        _db.update_one(
            {"_id": room["_id"]}, 
            {'$set': {"insInitial": ins}}
        )
    else:
        _db.update_one(
            {"_id": room["_id"]}, 
            {'$set': {"insInitial": add}}
        )

def update_instruction_init_step(
    name:str, id:str, 
    text:str=None, image:str=None, com:str=None, help:str=None):

    _db=db['room']
    room=_db.find_one({"roomName": name})
    ins=room['insInitial']
    if text==None and image==None and com==None and help==None: return True
    if text and not ins[id]['text']==text: ins[id]['text']=text
    if com and not ins[id]['command']==com: ins[id]['command']=com
    if help and not ins[id]['help']==help: ins[id]['help']=help
    if image: 
        img_hex=uuid.uuid4().hex
        img_hex_old=ins[id]['image']
        ins[id]['image']=img_hex

        exist=f'app/static/images/test/room{name}/instruction'
        path_exist_or_mkdir(exist)
        path=f'app/static/images/test/room{name}/instruction/{img_hex}.png'
        image_decoder(image,path)

        if not img_hex_old=='':
            remove=f'app/static/images/test/room{name}/instruction/{img_hex_old}.png'
            os.remove(remove)
    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': {"insInitial": ins}}
    )
    
def delete_instruction_init_step(name:str, id:str):
    _db=db['room']
    room=_db.find_one({"roomName": name})
    ins=room['insInitial']
    _dict={}
    for k, v in ins.items():
        if k<id: _dict[k]=v
        elif k>id:
            id_new=f'step {len(_dict)+1}'
            _dict[id_new]=v
        else:
            img_hex=v['image']
            if img_hex=='': continue
            remove=f'app/static/images/test/room{name}/instruction/{img_hex}.png'
            os.remove(remove)

    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': {"insInitial": _dict}}
    )

#------ Instruction turnon --------

#old version: storage in devices
'''
def get_instruction_turnon_step(room_name:str,device_name:str):
    _db=db['device']
    device=_db.find_one({"roomName": room_name, 'deviceName':device_name})
    if device_has_attribute(room_name,device_name,'insTurnon'):
        return device['insTurnon']
    else:
        return {}

def add_instruction_turnon_step(room_name:str,device_name:str,id:str):
    _db=db['device']
    device=_db.find_one({"roomName": room_name, 'deviceName':device_name})
    add={
        id:{'text':'', 'image':'', 'command':'', 'help':''}
    }
    if device_has_attribute(room_name,device_name,'insTurnon'):
        ins=device['insTurnon']
        ins.update(add)
        _db.update_one(
            {"_id": device["_id"]}, 
            {'$set': {"insTurnon": ins}}
        )
    else:
        _db.update_one(
            {"_id": device["_id"]}, 
            {'$set': {"insTurnon": add}}
        )

def update_instruction_turnon_step(
    room_name:str,device_name:str, id:str, 
    text:str=None, image:str=None, com:str=None, help:str=None):

    _db=db['device']
    device=_db.find_one({"roomName": room_name, 'deviceName':device_name})
    ins=device['insTurnon']
    if text==None and image==None and com==None and help==None: return True
    if text and not ins[id]['text']==text: ins[id]['text']=text
    if com and not ins[id]['command']==com: ins[id]['command']=com
    if help and not ins[id]['help']==help: ins[id]['help']=help
    if image: 
        img_hex=uuid.uuid4().hex
        img_hex_old=ins[id]['image']
        ins[id]['image']=img_hex

        exist=f'app/static/images/test/room{room_name}/instruction'
        path_exist_or_mkdir(exist)
        path=f'app/static/images/test/room{room_name}/instruction/{img_hex}.png'
        image_decoder(image,path)

        if not img_hex_old=='':
            remove=f'app/static/images/test/room{room_name}/instruction/{img_hex_old}.png'
            os.remove(remove)
    _db.update_one(
        {"_id": device["_id"]}, 
        {'$set': {"insTurnon": ins}}
    )

def delete_instruction_turnon_step(room_name:str,device_name:str, id:str):
    _db=db['device']
    device=_db.find_one({"roomName": room_name, 'deviceName':device_name})
    ins=device['insTurnon']
    _dict={}
    for k, v in ins.items():
        if k<id: _dict[k]=v
        elif k>id:
            id_new=f'step {len(_dict)+1}'
            _dict[id_new]=v
        else:
            img_hex=v['image']
            if img_hex=='': continue
            remove=f'app/static/images/test/room{room_name}/instruction/{img_hex}.png'
            os.remove(remove)

    _db.update_one(
        {"_id": device["_id"]}, 
        {'$set': {"insTurnon": _dict}}
    )
'''

#new version: storage in rooms
def get_instruction_turnon_step(room_name:str,device_name:str):
    _db=db['room']
    room=find_room_with_name(room_name)
    if room_has_attribute(room_name,'insTurnon'):
        ins=room['insTurnon']
        if device_name in ins.keys():
            return ins[device_name]

    return {}

def add_instruction_turnon_step(room_name:str,device_name:str,id:str):
    _db=db['room']
    room=find_room_with_name(room_name)
    add={
        id:{'text':'', 'image':'', 'command':'', 'help':''}
    }
    if room_has_attribute(room_name,'insTurnon'):
        ins=room['insTurnon'][device_name]
        ins.update(add)
        _db.update_one(
            {"_id": room["_id"]}, 
            {'$set': {f"insTurnon.{device_name}": ins}}
        )
    else:
        _db.update_one(
            {"_id": room["_id"]}, 
            {'$set': {f"insTurnon.{device_name}": add}}
        )

def update_instruction_turnon_step(
    room_name:str,device_name:str, id:str, 
    text:str=None, image:str=None, com:str=None, help:str=None):

    _db=db['room']
    room=find_room_with_name(room_name)
    ins=room['insTurnon'][device_name]
    if text==None and image==None and com==None and help==None: return True
    if text and not ins[id]['text']==text: ins[id]['text']=text
    if com and not ins[id]['command']==com: ins[id]['command']=com
    if help and not ins[id]['help']==help: ins[id]['help']=help
    if image: 
        img_hex=uuid.uuid4().hex
        img_hex_old=ins[id]['image']
        ins[id]['image']=img_hex

        exist=f'app/static/images/test/room{room_name}/instruction'
        path_exist_or_mkdir(exist)
        path=f'app/static/images/test/room{room_name}/instruction/{img_hex}.png'
        image_decoder(image,path)

        if not img_hex_old=='':
            remove=f'app/static/images/test/room{room_name}/instruction/{img_hex_old}.png'
            os.remove(remove)
    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': {f"insTurnon.{device_name}": ins}}
    )

def delete_instruction_turnon_step(room_name:str,device_name:str, id:str):
    _db=db['room']
    room=find_room_with_name(room_name)
    ins=room['insTurnon'][device_name]
    _dict={}
    for k, v in ins.items():
        if k<id: _dict[k]=v
        elif k>id:
            id_new=f'step {len(_dict)+1}'
            _dict[id_new]=v
        else:
            img_hex=v['image']
            if img_hex=='': continue
            remove=f'app/static/images/test/room{room_name}/instruction/{img_hex}.png'
            os.remove(remove)

    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': {f"insTurnon.{device_name}": _dict}}
    )

#------ Instruction pair --------

def get_instruction_pair_case(name:str):
    _db=db['room']
    room=_db.find_one({"roomName": name})
    if room_has_attribute(name,'insPair'):
        return room['insPair']
    else:
        return {}

def add_instruction_pair_case(name:str,id:str):
    _db=db['room']
    room=_db.find_one({"roomName": name})
    add={
        id:{'devices':{}, 'steps':{}}
    }
    if room_has_attribute(name,'insPair'):
        ins=room['insPair']
        ins.update(add)
        _db.update_one(
            {"_id": room["_id"]}, 
            {'$set': {"insPair": ins}}
        )
    else:
        _db.update_one(
            {"_id": room["_id"]}, 
            {'$set': {"insPair": add}}
        )

def delete_instruction_pair_case(room_name:str,case_name:str):
    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    ins_pair=room['insPair']

    if not case_name in ins_pair.keys(): return False
    _dict={}
    for k,v in ins_pair.items():
        if k<case_name: _dict[k]=v
        elif k>case_name:
            id_new=f'case {len(_dict)+1}'
            _dict[id_new]=v
        else:
            steps=v['steps']
            for i,j in steps.items():
                img_hex=j['image']
                if img_hex=='': continue
                remove=f'app/static/images/test/room{room_name}/instruction/{img_hex}.png'
                os.remove(remove)

    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': {"insPair": _dict}}
    )

def get_instruction_pair_case_step(room_name:str,case_name:str):
    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    ins_pair=room['insPair']
    ins_case=ins_pair[case_name]['steps']
    return ins_case

def add_instruction_pair_case_step(room_name:str,case_name:str,step_name:str):
    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    ins_pair=room['insPair']
    ins_case=ins_pair[case_name]['steps']

    add={
        step_name:{'text':'', 'image':'', 'command':'', 'help':''}
    }
    ins_case.update(add)
    ins_pair[case_name]['steps']=ins_case
    #这里采取了update整个case
    #但是不知道这样会不会很慢
    #有另一个方法还没试过:
    # {'$set': { f'insPair.{case_name}.steps' : ins_case}}
    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': { f'insPair.{case_name}.steps' : ins_case}}
    )

def update_instruction_pair_case_step(
    room_name:str,case_name:str,step_name:str,
    text:str=None, image:str=None, com:str=None, help:str=None):

    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    ins_pair=room['insPair']
    ins_case=ins_pair[case_name]['steps']

    if text==None and image==None and com==None and help==None: return True
    if text and not ins_case[step_name]['text']==text: ins_case[step_name]['text']=text
    if com and not ins_case[step_name]['command']==com: ins_case[step_name]['command']=com
    if help and not ins_case[step_name]['help']==help: ins_case[step_name]['help']=help
    if image: 
        img_hex=uuid.uuid4().hex
        img_hex_old=ins_case[step_name]['image']
        ins_case[step_name]['image']=img_hex

        exist=f'app/static/images/test/room{room_name}/instruction'
        path_exist_or_mkdir(exist)
        path=f'app/static/images/test/room{room_name}/instruction/{img_hex}.png'
        image_decoder(image,path)

        if not img_hex_old=='':
            remove=f'app/static/images/test/room{room_name}/instruction/{img_hex_old}.png'
            os.remove(remove)

    # {'$set': { f'insPair.{case_name}.steps' : ins_case}}
    ins_pair[case_name]['steps']=ins_case
    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': { f'insPair.{case_name}.steps' : ins_case}}
    )

def delete_instruction_pair_case_step(room_name:str,case_name:str,step_name:str):
    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    ins_pair=room['insPair']
    ins_case=ins_pair[case_name]['steps']

    _dict={}
    for k, v in ins_case.items():
        if k<step_name: _dict[k]=v
        elif k>step_name:
            id_new=f'step {len(_dict)+1}'
            _dict[id_new]=v
        else:
            img_hex=v['image']
            if img_hex=='': continue
            remove=f'app/static/images/test/room{room_name}/instruction/{img_hex}.png'
            os.remove(remove)

    # {'$set': { f'insPair.{case_name}.steps' : _dict}}
    ins_pair[case_name]['steps']=_dict
    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': { f'insPair.{case_name}.steps' : _dict}}
    )

def get_instruction_pair_case_device(room_name:str,case_name:str):
    _db=db['device']

    _dict={}
    devices=_db.find({'roomName':room_name},{'deviceName':1})
    
    for device in devices:
        _d={
            'name':device['deviceName']
        }
        _dict[f'Device {len(_dict)+1}']=_d

    _dict['Apple']={'name':'Apple'}
    _dict['Windows']={'name':'Windows'}

    return _dict

def get_instruction_pair_case_chosen_device(room_name:str,case_name:str):
    _db=db['device']
    room=_db.find_one({"roomName": room_name})
    ins_pair=room['insPair']
    ins_device=ins_pair[case_name]['devices']
    return ins_device

def choose_instruction_pair_device(room_name:str,case_name:str,device_id:str,device_name:str):
    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    ins_pair=room['insPair']
    ins_device=ins_pair[case_name]['devices']

    _dict={}
    _dict[device_id]={'name':device_name}
    ins_device.update(_dict)
    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': {f"insPair.{case_name}.devices": ins_device}}
    )

def undo_choose_instruction_pair_device(room_name:str,case_name:str,device_id:str,device_name:str):
    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    ins_pair=room['insPair']
    ins_device=ins_pair[case_name]['devices']

    _dict=ins_device.copy()
    for k,v in ins_device.items():
        if device_name==v['name']:
            _dict.pop(k)
    
    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': {f"insPair.{case_name}.devices": _dict}}
    )

#------ Instruction zoom --------

def create_instruction_zoom(room_name:str):
    if room_has_attribute(room_name,'insZoom'): return True
    _db=db['room']
    _db.update_one(
        {"roomName": room_name}, 
        {'$set': 
            {"insZoom": 
                {
                    'Video':{},
                    'Audio':{}
                }
            }
        }
    )

def get_instruction_zoom_step(room_name:str,zoom_type:str):
    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    return room['insZoom'][zoom_type]
    

def add_instruction_zoom_step(room_name:str,zoom_type:str,step_name:str):
    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    ins_zoom_type=room['insZoom'][zoom_type]

    add={
        step_name:{'text':'', 'image':'', 'command':'', 'help':''}
    }
    ins_zoom_type.update(add)
    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': {f"insZoom.{zoom_type}": ins_zoom_type}}
    )

def delete_instruction_zoom_step(room_name:str,zoom_type:str,step_name:str):
    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    ins_zoom_type=room['insZoom'][zoom_type]

    _dict={}
    for k, v in ins_zoom_type.items():
        if k<step_name: _dict[k]=v
        elif k>step_name:
            id_new=f'step {len(_dict)+1}'
            _dict[id_new]=v
        else:
            img_hex=v['image']
            if img_hex=='': continue
            remove=f'app/static/images/test/room{room_name}/instruction/{img_hex}.png'
            os.remove(remove)

    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': { f'insZoom.{zoom_type}' : _dict}}
    )

def update_instruction_zoom_step(
    room_name:str,zoom_type:str, step_name:str, 
    text:str=None, image:str=None, com:str=None, help:str=None):

    _db=db['room']
    room=_db.find_one({"roomName": room_name})
    ins_zoom=room['insZoom'][zoom_type]
    if text==None and image==None and com==None and help==None: return True
    if text and not ins_zoom[step_name]['text']==text: ins_zoom[step_name]['text']=text
    if com and not ins_zoom[step_name]['command']==com: ins_zoom[step_name]['command']=com
    if help and not ins_zoom[step_name]['help']==help: ins_zoom[step_name]['help']=help
    if image: 
        img_hex=uuid.uuid4().hex
        img_hex_old=ins_zoom[step_name]['image']
        ins_zoom[step_name]['image']=img_hex

        exist=f'app/static/images/test/room{room_name}/instruction'
        path_exist_or_mkdir(exist)
        path=f'app/static/images/test/room{room_name}/instruction/{img_hex}.png'
        image_decoder(image,path)

        if not img_hex_old=='':
            remove=f'app/static/images/test/room{room_name}/instruction/{img_hex_old}.png'
            os.remove(remove)
    
    _db.update_one(
        {"_id": room["_id"]}, 
        {'$set': { f'insZoom.{zoom_type}' : ins_zoom}}
    )

#-----------------------------------------
#-------------- user flow ---------------
#-----------------------------------------

#import cv2
def get_all_device_user(name:str):
    _db=db['device']
    devices=_db.find({"roomName": name})
    #path=f'app/static/images/test/room{name}/_360_upload.png'
    #img=cv2.imread(path)
    #img_u=img.shape[1]
    #img_v=img.shape[0]
    _dict={}
    for device in devices:
        deviceInfo = {}
        deviceInfo['name'] = device["deviceName"]
        #deviceInfo['v'] = str(round(device['deviceLocX']/img_u*100,1))+'%'
        #deviceInfo['u'] = str(round(device['deviceLocY']/img_v*100,1))+'%'
        deviceInfo['v'] = str(device['deviceLocY'])+'%'
        deviceInfo['u'] = str(device['deviceLocX'])+'%'
        _dict[len(_dict)]=deviceInfo
    return _dict

def get_all_occupy_user(email:str,time,access_date):
    _db=db['room']
    rooms=_db.find(
        {},
        {'bookBy':1, 'bookTime':1, 'roomName':1}
    )
    occupy = {}
    for room in rooms:
        bookTime=room["bookTime"]
        bookBy=room["bookBy"]
        if not email in bookBy.keys(): continue
        for t in time:
            for d in access_date:
                _t=t[:2]+' : '+t[2:]
                _d=int(d.split('/')[2])
                if not bookTime.get(d) is None and t in bookTime[d]:
                    occupy[(_t,_d)]=room["roomName"]
                    #if (_t,_d) in occupy.keys() and not occupy[(_t,_d)]=='n':
                    #    occupy[(_t,_d)]='Conflict'
                    #else:
                    #    occupy[(_t,_d)]=room["roomName"]
                else:
                    if (_t,_d) in occupy.keys():
                        continue
                    else:
                        occupy[(_t,_d)]='n'
    return occupy