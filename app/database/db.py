import os
import shutil
import base64
from pymongo.mongo_client import MongoClient
from .utils import Account, Room, System, time, compare_date_and_time, sort_bookInfo_list
from werkzeug.security import generate_password_hash, check_password_hash
from functools import cmp_to_key

def connection(dbname):
    # mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/myFirstDatabase?retryWrites=true"&"w=majority
    addr = "mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(addr)
    db = client[dbname]
    return db

def Convert(lst):
    res_dct = { str(i) : lst[i] for i in range(0, len(lst)) }
    return res_dct

def path_exist_or_mkdir(path:str):
    if not os.path.exists(path):
        os.makedirs(path)
    return True

# def image_encoder(image_path: str):
#     img = open(image_path,"rb")
#     img_encode = base64.b64encode(img.read())
#     img.close()
#     img_string = img_encode.decode('utf-8')
#     return img_string

def image_decoder(encoded_image: str, save_path: str = "write.png"): #decode string from encoder
    img_encode = encoded_image.encode('utf-8')
    img = base64.b64decode(img_encode)
    out = open(save_path,"wb")
    out.write(img)
    out.close()

# def generateDeviceTypeList(devicetype):
#     deviceTypeList = []
#     for type in devicetype:
#         if type not in deviceTypeList:
#             deviceTypeList.append(type)
#     return deviceTypeList

class AccountDB():
    def __init__(self, db):
        self.db = db["account"]
    
    def cleardb(self):
        self.db.delete_many({})

    def signup(self, accountEmail, accountPw):
        if self.db.find_one({"accountEmail": accountEmail}):
            return "Err: Account Exists!"
        newAccount = Account(accountEmail, accountPw)
        self.db.insert_one(newAccount.__dict__)
        return "Info: Register USER Account Successfully"

    def login(self, accountEmail, accountPw, loginID):
        account = self.db.find_one({"accountEmail": accountEmail})
        # print(account["accountID"])
        if account is None:
            return "Err: Not Registered!"
        elif check_password_hash(account["accountPw"], accountPw) == False:
            # print(account["accountPw"])
            # print(accountPw)
            return "Err: Wrong Password!"
        elif account["accountID"] != 'ADMIN' and loginID == 'ADMIN':
            return "Err: You Are Not Authorized!"
        else:
            return "Info: Login successfully!"
        

    def logout(self, accountEmail):
        self.db.update_one({"accountEmail": accountEmail}, {'$set': {'room': "", 'personal': "", "device": []} })
        return "Info: Logout Successfully!"

    def register(self, accountEmail, accountPw):
        accountID = "GUEST"
        if "ust" in accountEmail: accountID = "USER"
        newAccount = Account(accountEmail, generate_password_hash(accountPw), accountID)
        self.db.insert_one(newAccount.__dict__)
        return "Info: Registered As " + accountID

    def checkAccountPw(self, accountEmail):
        account = self.db.find_one({"accountEmail": accountEmail})
        if account is None:
            return "Err: Not Registered!"
        return account["accountPw"]
    
    def checkAccountID(self, accountEmail):
        account = self.db.find_one({"accountEmail": accountEmail})
        if account is None:
            return "Err: Not Registered!"
        return account["accountID"]

    def updateAdminID(self, accountEmail):
        account = self.db.find_one({"accountEmail": accountEmail})
        if account is None:
            return "Err: Not Registered!"
        self.db.update_one({"accountEmail": accountEmail}, {'$set': {'accountID': "ADMIN"}})
        return "Info: Update Successfully!"
    
    def updateRoom(self, accountEmail, roomName):
        account = self.db.find_one({"accountEmail": accountEmail})
        if account is None:
            return "Err: Not Registered!"
        self.db.update_one({"accountEmail": accountEmail}, {'$set': {'room': roomName}})
        return "Info: Update Successfully!"
    
    def updatePersonal(self, accountEmail, personal):
        account = self.db.find_one({"accountEmail": accountEmail})
        if account is None:
            return "Err: Not Registered!"
        self.db.update_one({"accountEmail": accountEmail}, {'$set': {'personal': personal}})
        return "Info: Update Successfully!"
    
    def updateDevice(self, accountEmail, device):
        account = self.db.find_one({"accountEmail": accountEmail})
        if account is None:
            return "Err: Not Registered!"
        self.db.update_one({"accountEmail": accountEmail}, {'$set': {'device': device}})
        return "Info: Update Successfully!"
    
    def findUser(self, accountEmail):
        return self.db.find_one({"accountEmail": accountEmail})

# class DeviceDB():
#     def __init__(self, db):
#         self.db = db["device"]

#     def cleardb(self):
#         self.db.delete_many({})

#     def addDevice(self, roomName, deviceName, deviceType, deviceIP, deviceLocX, deviceLocY):
#         device = self.db.find_one({"roomName": roomName, "deviceLocX": deviceLocX, "deviceLocY": deviceLocY})
        
#         if device:
#             self.db.update_one({"_id": device["_id"]}, \
#                 {'$set': {"deviceName": deviceName, "deviceType": deviceType, "deviceIP": deviceIP, "deviceLocX": deviceLocX, "deviceLocY": deviceLocY}})
#             return "Info: Edit Device Successfully!"
#         else:
#             newDevice = Device(roomName, deviceName, deviceType, deviceIP, deviceLocX, deviceLocY)
#             self.db.insert_one(newDevice.__dict__)
#             return "Info: Add Device Successfully!"
            
#     def delDevice(self, roomName, deviceName):
#         device = self.db.find_one({"deviceName": deviceName, "roomName": roomName})
#         if device is None:
#             return "Err: Device Invalid!"
#         self.db.delete_one({"_id": device["_id"]})
#         return "Info: Delete Successfully!"
    
#     def checkDeviceList(self, roomName, V, U):
#         devices = self.db.find({"roomName": roomName})
#         deviceInfo_list = []
#         for device in devices:
#             deviceInfo = {}
#             deviceInfo['name'] = device["deviceName"]
#             deviceInfo['v'] = str(int(int(device['deviceLocX'])/V*100))+'%'
#             deviceInfo['u'] = str(int(int(device['deviceLocY'])/U*100))+'%'
#             deviceInfo_list.append(deviceInfo)
#         return Convert(deviceInfo_list)
    
#     def generateDeviceTypeList(self, roomName):
#         devices = self.db.find({"roomName": roomName})
#         deviceTypeList = []
#         for device in devices:
#             if device["deviceType"] not in deviceTypeList:
#                 deviceTypeList.append(device["deviceType"])
#         return deviceTypeList
    
    # def printDeviceList(self, roomName):
    #     devices = self.checkDeviceList(roomName)
    #     for dev in devices:
    #         print("Device ID: " + str(dev["deviceID"]) + "\nDevice Name: " + dev["deviceName"] + "\nDevice Type: " + dev["deviceName"] + "\nDevice IP" + dev["deviceIP"] + "\n")

class RoomDB():
    def __init__(self, db):
        self.db = db["room"]
        self.access_date = []

    def cleardb(self):
        self.db.delete_many({})

    def getroom(self, roomName):
        room = self.db.find_one({"roomName": roomName})
        return room

    def clearChooseDeviceIDList(self, roomName):
        self.db.update_one({"roomName": roomName}, {'$set': {'chooseDeviceIDList': []}})

    def chooseDevice(self, roomName, deviceID):
        room = self.db.find_one({"roomName": roomName})
        if deviceID not in room["chooseDeviceIDList"]: room["chooseDeviceIDList"].append(deviceID)
        # print(room["chooseDeviceIDList"])
        self.db.update_one({"roomName": roomName}, {'$set': {'chooseDeviceIDList': room["chooseDeviceIDList"]}})
    
    def getChooseDeviceList(self, roomName):
        room = self.db.find_one({"roomName": roomName})
        chooseDeviceList = {}
        for i in range(4, len(room["deviceNameList"])):
            if str(i) in room["chooseDeviceIDList"]:
                chooseDeviceList[i - 4] = [room["deviceNameList"][str(i)], 1]
            else:
                chooseDeviceList[i - 4] = [room["deviceNameList"][str(i)], 0]
        return chooseDeviceList
    
    def getroomInfo(self):
        roomInfo = {}
        index = 0
        roomList = self.db.find({})
        for room in roomList:
            roomInfo[index] = {}
            roomInfo[index]['name'] = room['roomName']
            roomInfo[index]['lift'] = room['roomLoc']
        return roomInfo

    def checkRoomAvailable(self, roomName, date=None, extend_access_date=None, get_occupy=False):
        # print(roomName)
        room = self.db.find_one({"roomName": roomName})
        bookTime = room["bookTime"]
        if date:
            if bookTime.get(date) is None:
                bookTime[date] = []
                self.db.update_one({"roomName": roomName}, {'$set': {'bookTime': bookTime}})
        if extend_access_date: self.access_date.extend(extend_access_date)
        if get_occupy:
            occupy = {}
            for t in time:
                for d in self.access_date:
                    _t=t[:2]+' : '+t[2:]
                    _d=int(d.split('/')[2])
                    if not bookTime.get(d) is None and t in bookTime[d]:
                        occupy[(_t,_d)]='y'
                    else:
                        occupy[(_t,_d)]='n'
            return occupy

        return bookTime
        # for t in time:
        #     if t in bookTime[date]: continue
        #     time_data = date + " " + t[:2] + ':' + t[2:] + ':00'
            # print(time_data)
            #print(datetime.strptime(time_data, format_data))

    def setRoomBookByUser(self, roomName, date, accountEmail, ft, tt):
        self.checkRoomAvailable(roomName, date)
        room = self.db.find_one({"roomName": roomName})
        bookTime = room["bookTime"]
        # ft, tt, user = map(str, input("from time & to time & use id: 0800 0900 ust.hk\n").split())
        for i in range(time.index(ft), time.index(tt)):
            if time[i] in bookTime[date]: 
                print("Not Available Time")
                return "Err: Time Not Available!"
        for i in range(time.index(ft), time.index(tt)): 
            bookTime[date].append(time[i])
        self.db.update_one({"roomName": roomName}, {'$set': {'bookTime': bookTime}})
        bookBy = room['bookBy']
        if bookBy.get(accountEmail) is None: 
            bookBy[accountEmail] = [[date, ft, tt]]
        else:
            booklist = []
            booklist = bookBy[accountEmail]
            booklist.append([date, ft, tt])
            # print(booklist)
            bookBy[accountEmail] = sorted(booklist, key=cmp_to_key(compare_date_and_time))
            # print(bookBy[accountEmail])
            # bookBy[accountEmail] = booklist
        self.db.update_one({"roomName": roomName}, {'$set': {'bookBy': bookBy}})
        return "Info: Book Successully!"

    def checkUserBooking(self, accountEmail):
        room_list = self.db.find({})
        bookInfo_list = []
        for room in room_list:
            bookBy = room['bookBy']
            if bookBy.get(accountEmail):
                bookInfo = {}
                bookInfo['name'] = room['roomName']
                bookInfo['lift'] = room['roomLoc']
                bookInfo['date'] = bookBy[accountEmail][0][0]
                bookInfo['time'] = bookBy[accountEmail][0][1:]
                bookInfo_list.append(bookInfo)
        bookInfo_list = sorted(bookInfo_list, key=cmp_to_key(sort_bookInfo_list))
        return Convert(bookInfo_list)

    def checkSearchRoom(self, roomName, accountEmail):
        # print(roomName)
        room_list = self.db.find({"roomName": {'$regex': roomName}})
        roomInfo_list = []
        for room in room_list:
            roomInfo = {}
            roomInfo['name'] = room['roomName']
            roomInfo['lift'] = room['roomLoc']
            bookBy = room['bookBy']
            if bookBy.get(accountEmail):
                roomInfo['date'] = bookBy[accountEmail][0][0]
                roomInfo['time'] = bookBy[accountEmail][0][1:]
            else:
                roomInfo['date'] = ""
                roomInfo['time'] = ""
            roomInfo_list.append(roomInfo)
        return Convert(roomInfo_list)

    def addDevice(self, roomName, deviceID, deviceName, deviceType, deviceIP, deviceLocX=-1, deviceLocY=-1):
        room = self.db.find_one({"roomName": roomName})
        # print(deviceID)
        if deviceID == "-1": deviceID = str(len(room["deviceNameList"]))
        # print(deviceID)
        room["deviceNameList"][deviceID] = deviceName
        room["deviceTypeList"][deviceID] = deviceType
        room["deviceIPList"][deviceID] = deviceIP
        if deviceLocX != -1: room["deviceLocXList"][deviceID] = deviceLocX
        if deviceLocY != -1: room["deviceLocYList"][deviceID] = deviceLocY
        self.db.update_one({"roomName": roomName}, \
            {'$set': {"deviceNameList": room["deviceNameList"], "deviceTypeList": room["deviceTypeList"], "deviceIPList": room["deviceIPList"], "deviceLocXList": room["deviceLocXList"], "deviceLocYList": room["deviceLocYList"]}})
    
    def delDevice(self, roomName, deviceID):
        room = self.db.find_one({"roomName": roomName})
        if deviceID == "-1": return "Err: Invalid Devive!"
        for i in range(int(deviceID) + 1, len(room["deviceNameList"])): room["deviceNameList"][str(i - 1)] = room["deviceNameList"].pop(str(i))
        for i in range(int(deviceID) + 1, len(room["deviceTypeList"])): room["deviceTypeList"][str(i - 1)] = room["deviceTypeList"].pop(str(i))
        for i in range(int(deviceID) + 1, len(room["deviceIPList"])): room["deviceIPList"][str(i - 1)] = room["deviceIPList"].pop(str(i))
        for i in range(int(deviceID) + 1, len(room["deviceLocXList"])): room["deviceLocXList"][str(i - 1)] = room["deviceLocXList"].pop(str(i))
        for i in range(int(deviceID) + 1, len(room["deviceLocYList"])): room["deviceLocYList"][str(i - 1)] = room["deviceLocYList"].pop(str(i))
        self.db.update_one({"roomName": roomName}, \
            {'$set': {"deviceNameList": room["deviceNameList"], "deviceTypeList": room["deviceTypeList"], "deviceIPList": room["deviceIPList"], "deviceLocXList": room["deviceLocXList"], "deviceLocYList": room["deviceLocYList"]}})

    def getDeviceID(self, roomName, deviceName):
        deviceID = "-1"
        room = self.db.find_one({"roomName": roomName})
        for k, v in room["deviceNameList"].items():
            if v == deviceName: return k
        return deviceID

    def getDeviceInfo(self, roomName):
        deviceInfo = {}
        room = self.db.find_one({"roomName": roomName})
        if not room: return deviceInfo
        for i in range(4, len(room["deviceNameList"])):
            deviceInfo[i - 4] = {
                'name': room['deviceNameList'][str(i)],
                'type': room['deviceTypeList'][str(i)],
                'ip'  : room['deviceIPList'][str(i)],
                'x'   : room['deviceLocXList'][str(i)],
                'y'   : room['deviceLocYList'][str(i)],
            }
            
        return deviceInfo

    def getDeviceTypeList(self, roomName):
        room = self.db.find_one({"roomName": roomName})
        deviceTypeList = {}
        for deviceType in room["deviceTypeList"].values():
            if deviceType not in deviceTypeList.values():
                deviceTypeList[len(deviceTypeList)] = deviceType
        return deviceTypeList

    def addRoom(self, roomName, roomLoc, controlSystem):
        room = self.db.find_one({"roomName": roomName})
        if not room:
            newRoom = Room(roomName, roomLoc, controlSystem)
            self.db.insert_one(newRoom.__dict__)
            return "Info: Add Room Successfully!"
        else:
            return "Err: Room Exist!"

    def editRoom(self, roomName, newRoomName, newRoomLoc, newControlSystem):
        room = self.db.find_one({"roomName": roomName})
        if not room:
            return "Err: Room Not Exist!"
        elif self.getroom(newRoomName):
            return "Err: Rename Invalid!"            
        else:
            if newRoomName: room["roomName"] = newRoomName
            if newRoomLoc: room["roomLoc"] = newRoomLoc
            if newControlSystem: room["controlSystem"] = newControlSystem
            self.db.update_one({"_id": room["_id"]}, {'$set': {"roomName": room["roomName"], "roomLoc": room["roomLoc"] , "controlSystem": room["controlSystem"]}})
            return "Info: Edit Room Successfully!"

    def delRoom(self, roomName):
        room = self.db.find_one({"roomName": roomName})
        if room is None: return "Err: Room Invalid!"
        self.db.delete_one({"_id": room["_id"]})

        path=f'app/static/images/test/room{roomName}'
        path_exist_or_mkdir(path)
        shutil.rmtree(path)

        return "Info: Delete Successfully!"
    
    def uploadImage(self, roomName, roomImg, imgType):
        if not roomImg: return "Err: Invalid Image!"
        exist=f'app/static/images/test/room{roomName}'
        path_exist_or_mkdir(exist)
        path=f'app/static/images/test/room{roomName}/{imgType}'
        image_decoder(roomImg,path)

    # def upload360Img(self, roomName, room360Img):
    #     self.db.update_one({"roomName": roomName}, {"room360Img": room360Img})
    #     return "Info: Upload Successfully!"

    # def generatePreview(self, roomName, roomInsDevice, roomInsCases):
    #     room = self.db.find_one({"roomName": roomName})
    #     roomInsPreview = {}
    #     for caseID in range(len(roomInsCases)):
    #         roomInsPreview[str(caseID)] = {}

    #         deviceNameList = []
    #         for i in range(len(room["deviceNameList"])):
    #             if room["deviceTypeList"][str(i)] in roomInsDevice[str(caseID)]:
    #                 deviceNameList.append(room["deviceNameList"][str(i)])
                
    #         roomInsPreview[str(caseID)]["devices"] = deviceNameList

    #         for stepID in range(len(roomInsCases[str(caseID)])):
    #             stepName = "step" + str(stepID + 1)
    #             roomInsPreview[str(caseID)][stepName] = roomInsCases[str(caseID)][str(stepID)]
    #             roomInsPreview[str(caseID)][stepName]["help"] = ""
    #     return roomInsPreview

    # preview data structure:
    # {0:
    #   {"devices": [device name list],
    #    "step1": {"text": , "image": , "command": , "help": },
    #    "step2": {"text": , "image": , "command": , "help": }, 
    #   }
    #  1:
    #   {"devices": [],
    #    "step1": {"text": , "image": , "command": , "help": },
    #    "step2": {"text": , "image": , "command": , "help": }, 
    #   }
    # }
    
    def generateIns(self, deviceTypeList, insDevice, insCases):
        # print(deviceTypeList)
        roomInsDevice = {}
        roomInsCases = {}
        index = 0
        for i in range(0, len(insCases)):
            # print(i)
            valid = True
            for dev in insDevice[str(i)]:
                if dev not in deviceTypeList.values():
                    valid = False
            if valid == True: 
                roomInsDevice[str(index)] = insDevice[str(i)]
                roomInsCases[str(index)] = insCases[str(i)]
                index += 1
        return roomInsDevice, roomInsCases

    def generatePreview(self, deviceNameList, deviceTypeList, insDevice, insCases):
            insPreview = {}
            for caseID in range(len(insCases)):
                insPreview[str(caseID)] = {}
                insPreview[str(caseID)]["devices"] = []
                for deviceID in range(len(deviceTypeList)):
                    if deviceTypeList[str(deviceID)] in insDevice[str(caseID)]:
                        insPreview[str(caseID)]["devices"].append(deviceNameList[str(deviceID)])
                for stepID in range(len(insCases[str(caseID)])):
                    stepName = "step" + str(stepID + 1)
                    insPreview[str(caseID)][stepName] = insCases[str(caseID)][str(stepID)]
                    if "help" not in insPreview[str(caseID)][stepName]: insPreview[str(caseID)][stepName]["help"] = ""
            return insPreview

    def generateRoomPreview(self, roomName, insDevice, insCases):
        room = self.db.find_one({"roomName": roomName})
        # print(room["deviceTypeList"])
        roomInsDevice, roomInsCases = self.generateIns(room["deviceTypeList"], insDevice, insCases)
        # print(roomInsDevice)
        self.db.update_one({"roomName": roomName}, {'$set': {"roomInsDevice": roomInsDevice, "roomInsCases": roomInsCases}})
        return self.generatePreview(room["deviceNameList"], room["deviceTypeList"], roomInsDevice, roomInsCases) 

    def generateUserPreview(self, roomName, userDeviceIDList):
        room = self.db.find_one({"roomName": roomName})
        userDeviceTypeList = {}
        userDeviceNameList = {}
        index = 0

        for deviceID in userDeviceIDList:
            userDeviceTypeList[str(index)] = room["deviceTypeList"][deviceID]
            userDeviceNameList[str(index)] = room["deviceNameList"][deviceID]
            index += 1

        insDevice, insCases = self.generateIns(userDeviceTypeList, room["roomInsDevice"], room["roomInsCases"])
        return self.generatePreview(userDeviceNameList, userDeviceTypeList, insDevice, insCases)
        # roomInsPreview = {}
        # for caseID in range(len(roomInsCases)):
        #     roomInsPreview[str(caseID)] = {}

        #     deviceNameList = []
        #     for i in range(len(room["deviceNameList"])):
        #         if room["deviceTypeList"][str(i)] in roomInsDevice[str(caseID)]:
        #             deviceNameList.append(room["deviceNameList"][str(i)])
                
        #     roomInsPreview[str(caseID)]["devices"] = deviceNameList

        #     for stepID in range(len(roomInsCases[str(caseID)])):
        #         stepName = "step" + str(stepID + 1)
        #         roomInsPreview[str(caseID)][stepName] = roomInsCases[str(caseID)][str(stepID)]
        #         roomInsPreview[str(caseID)][stepName]["help"] = ""
        # return roomInsPreview
    
    # def generateUserIns(self, roomName, userDeviceIDList):
    #     room = self.db.find_one({"roomName": roomName})
    #     if device["deviceType"] not in deviceTypeList:
    #             deviceTypeList.append(device["deviceType"])
    #     return userInsPreview 

    def addHelp(self, roomName, caseID, stepID, helpInfo):
        room = self.db.find_one({"roomName": roomName})
        roomInsCases = room["roomInsCases"]
        roomInsCases[caseID][stepID]["help"] = helpInfo
        self.db.update_one({"roomName": roomName}, {'$set': {"roomInsCases": roomInsCases}})

class SystemDB():
    def __init__(self, db):
        self.db = db["system"]

    def cleardb(self):
        self.db.delete_many({})

    def getsystem(self, controlSystem):
        system = self.db.find_one({"controlSystem": controlSystem})
        return system

    def getSystemList(self):
        systemList = self.db.find({})
        systemListInfo = {}
        for system in systemList:
            systemListInfo[len(systemListInfo)] = system["controlSystem"]
        return systemListInfo

    def createSystem(self, controlSystem):
        system = self.db.find_one({"controlSystem": controlSystem})

        if system: return "Err: System Exist!"
        else:
            newSystem = System(controlSystem)
            self.db.insert_one(newSystem.__dict__)
            return "Info: Add System Successfully!"
    
    def addDeviceType(self, controlSystem, deviceType):
        system = self.db.find_one({"controlSystem": controlSystem})
        if not system: return "Err: System Not Exist!"
        deviceTypeList = system["deviceTypeList"]
        deviceTypeList.append(deviceType)
        self.db.update_one({"controlSystem": controlSystem}, {'$set': {"deviceTypeList": deviceTypeList}})
        return "Info: Add Device Type Successfully!"
    
    def delDeviceType(self, controlSystem, deviceType):
        system = self.db.find_one({"controlSystem": controlSystem})
        if not system: return "Err: System Not Exist!"
        deviceTypeList = system["deviceTypeList"]
        if deviceType in deviceTypeList:
            deviceTypeList.remove(deviceType)
            self.db.update_one({"controlSystem": controlSystem}, {'$set': {"deviceTypeList": deviceTypeList}})
            return "Info: Delete Device Type Successfully!"
    
    def checkDeviceTypeDict(self, controlSystem):
        system = self.db.find_one({"controlSystem": controlSystem})
        if not system: return "Err: System Not Exist!"
        deviceTypeList = system["deviceTypeList"]
        deviceTypeDict = {}
        for i in range(0, len(deviceTypeList)):
            deviceTypeDict[i] = deviceTypeList[i]
        return deviceTypeDict

    def addCaseDevice(self, controlSystem, caseID, deviceList):
        system = self.db.find_one({"controlSystem": controlSystem})
        if not system: return "Err: System Not Exist!"
        insDevice = system["insDevice"]
        if caseID not in insDevice: insDevice[caseID] = []
        insDevice[caseID] = deviceList
        self.db.update_one({"controlSystem": controlSystem}, {'$set': {"insDevice": insDevice}})
        return "Info: Edit Successfully!"

    def deleteCase(self, controlSystem, caseID):
        system = self.db.find_one({"controlSystem": controlSystem})
        if not system: return "Err: System Not Exist!"
        insDevice = system["insDevice"]
        # print(insDevice)
        # insDevice.pop(caseID)
        for i in range(int(caseID) + 1, len(insDevice)): insDevice[str(i - 1)] = insDevice.pop(str(i))
        self.db.update_one({"controlSystem": controlSystem}, {'$set': {"insDevice": insDevice}})
        insCases = system["insCases"]
        # insCases.pop(caseID)
        for i in range(int(caseID) + 1, len(insCases)): insCases[str(i - 1)] = insCases.pop(str(i))
        self.db.update_one({"controlSystem": controlSystem}, {'$set': {"insCases": insCases}})
        return "Info: Delete Successfully!"

    def addCaseStep(self, controlSystem, caseID, stepID, text="", image="", command=""):
        system = self.db.find_one({"controlSystem": controlSystem})
        if not system: return "Err: System Not Exist!"
        insCases = system["insCases"]
        if caseID not in insCases: insCases[caseID] = {}
        if stepID not in insCases[caseID]: insCases[caseID][stepID] = {}
        insCases[caseID][stepID]["text"] = text
        insCases[caseID][stepID]["image"] = image
        insCases[caseID][stepID]["command"] = command
        self.db.update_one({"controlSystem": controlSystem}, {'$set': {"insCases": insCases}})
        return "Info: Edit Successfully!"

    def delCaseStep(self, controlSystem, caseID, stepID):
        system = self.db.find_one({"controlSystem": controlSystem})
        if not system: return "Err: System Not Exist!"
        insCases = system["insCases"]
        if caseID not in insCases: return "Err"
        # insCases[caseID].pop(stepID)
        for i in range(int(stepID) + 1, len(insCases[caseID])): insCases[caseID][str(i - 1)] = insCases[caseID].pop(str(i))
        self.db.update_one({"controlSystem": controlSystem}, {'$set': {"insCases": insCases}})
        return "Info: Delete Successfully!"

    def getDeviceTypeList(self, controlSystem):
        system = self.db.find_one({"controlSystem": controlSystem})
        deviceTypeList = {}
        for deviceType in system["deviceTypeList"]:
            if deviceType not in deviceTypeList.values():
                deviceTypeList[len(deviceTypeList)] = deviceType
        return deviceTypeList

    
db = connection("test")
accountdb = AccountDB(db)
roomdb = RoomDB(db)
systemdb = SystemDB(db)