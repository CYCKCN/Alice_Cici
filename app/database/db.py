from pymongo.mongo_client import MongoClient
from .object import Account, Device, Room, time, format_data, compare_date_and_time, sort_bookInfo_list
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

class DeviceDB():
    def __init__(self, db):
        self.db = db["device"]

    def cleardb(self):
        self.db.delete_many({})

    def addDevice(self, roomName, deviceName, deviceType, deviceIP, deviceLocX, deviceLocY):
        device = self.db.find_one({"roomName": roomName, "deviceLocX": deviceLocX, "deviceLocY": deviceLocY})
        
        if device:
            self.db.update_one({"_id": device["_id"]}, \
                {'$set': {"deviceName": deviceName, "deviceType": deviceType, "deviceIP": deviceIP, "deviceLocX": deviceLocX, "deviceLocY": deviceLocY}})
            return "Info: Edit Device Successfully!"
        else:
            newDevice = Device(roomName, deviceName, deviceType, deviceIP, deviceLocX, deviceLocY)
            self.db.insert_one(newDevice.__dict__)
            return "Info: Add Device Successfully!"
            
    def delDevice(self, roomName, deviceName):
        device = self.db.find_one({"deviceName": deviceName, "roomName": roomName})
        if device is None:
            return "Err: Device Invalid!"
        self.db.delete_one({"_id": device["_id"]})
        return "Info: Delete Successfully!"
    
    def checkDeviceList(self, roomName, V, U):
        devices = self.db.find({"roomName": roomName})
        deviceInfo_list = []
        for device in devices:
            deviceInfo = {}
            deviceInfo['name'] = device["deviceName"]
            deviceInfo['v'] = str(int(int(device['deviceLocX'])/V*100))+'%'
            deviceInfo['u'] = str(int(int(device['deviceLocY'])/U*100))+'%'
            deviceInfo_list.append(deviceInfo)
        return Convert(deviceInfo_list)
    
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
    
    def checkRoomAvailable(self, roomName, date=None, extend_access_date=None, get_occupy=False):
        print(roomName)
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
        print(roomName)
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

    def addRoom(self, roomName, roomImg, roomLoc):
        room = self.db.find_one({"roomName": roomName})

        if room:
            self.db.update_one({"_id": room["_id"]}, {'$set': {"roomName": roomName, "roomImg": roomImg, "roomLoc": roomLoc}})
            return "Info: Edit Room Successfully!"
        else:
            newRoom = Room(roomName, roomImg, roomLoc)
            self.db.insert_one(newRoom.__dict__)
            return "Info: Add Room Successfully!"

    def delRoom(self, roomName):
        room = self.db.find_one({"roomName": roomName})
        if room is None:
            return "Err: Room Invalid!"
        self.db.delete_one({"_id": room["_id"]})
        return "Info: Delete Successfully!"

    def upload360Img(self, roomName, room360Img):
        self.db.update_one({"roomName": roomName}, {"room360Img": room360Img})
        return "Info: Upload Successfully!"

    # def checkRoomList(self):
    #     rooms = self.db.find({})
    #     return rooms
    
    def printRoomList(self):
        rooms = self.checkRoomList("")
        for r in rooms:
            print("Room Name: " + r["roomName"] + "\nRoom Img: " + r["roomImg"] + "\nRoom Location" + r["roomLoc"] + "\n")
        return

    def addInsInitialStep(self, roomName, stepID, stepText='', stepImg='', stepCom='', stepHelp=''):
        room = self.db.find_one({"roomName": roomName})
        roomInsInitialStep = room["insInitial"]

        stepInfo = {}
        stepInfo['text'] = stepText
        stepInfo['image'] = stepImg
        stepInfo['command'] = stepCom
        stepInfo['help'] = stepHelp

        if len(roomInsInitialStep) > stepID:
            roomInsInitialStep[stepID] = stepInfo
        else:
            roomInsInitialStep.append(stepInfo)

        self.db.update_one({"_id": room["_id"]}, {'$set': {"insInitial": roomInsInitialStep}})

    def delInsInitialStep(self, roomName, stepID):
        room = self.db.find_one({"roomName": roomName})
        roomInsInitialStep = room["insInitial"]
        if len(roomInsInitialStep) > stepID:
            roomInsInitialStep.pop(stepID)
        else:
            return "Err: Invalid StepID!"
        self.db.update_one({"_id": room["_id"]}, {'$set': {"insInitial": roomInsInitialStep}})
    
    def checkInsInitialStepList(self, roomName):
        print("*****" + roomName)
        room = self.db.find_one({"roomName": roomName})
        roomInsInitialStep = room["insInitial"]
        step_list = {}
        for i in range(0, len(roomInsInitialStep)):
            step = {}
            step['text'] = roomInsInitialStep[i]['text']
            step['image'] = roomInsInitialStep[i]['image']
            step['command'] = roomInsInitialStep[i]['command']
            step_list[i] = step
        return step_list

    # def printInsInitialStepList(self, roomName):
    #     roomInsInitialStep = self.checkInsInitialStepList(roomName)
    #     for i in range(0, len(roomInsInitialStep)):
    #         print("Step " + str(i) + ": " + roomInsInitialStep[i]['text'] + " " + roomInsInitialStep[i]['image'] + " " + roomInsInitialStep[i]['command'] + " " + roomInsInitialStep[i]['help'])
    #     print('')
    #     return 

    def insTurnonInit(self, room, deviceList):
        roomInsTurnonStep = {}
        for dev in deviceList:
            roomInsTurnonStep[dev["deviceName"]] = []
        self.db.update_one({"_id": room["_id"]}, {'$set': {"insTurnon": roomInsTurnonStep}})
        return roomInsTurnonStep

    def addInsTurnonStep(self, roomName, deviceName, stepID, stepText='', stepImg='', stepCom='', stepHelp=''):
        room = self.db.find_one({"roomName": roomName})
        roomInsTurnonStep = room["insTurnon"]
        if roomInsTurnonStep.get(deviceName) is None:
            return "Err: Invalid Device Name!"
        
        stepInfo = {}
        stepInfo['text'] = stepText
        stepInfo['image'] = stepImg
        stepInfo['command'] = stepCom
        stepInfo['help'] = stepHelp

        if len(roomInsTurnonStep[deviceName]) > stepID:
            roomInsTurnonStep[deviceName][stepID] = stepInfo
        else:
            roomInsTurnonStep[deviceName].append(stepInfo)

        self.db.update_one({"_id": room["_id"]}, {'$set': {"insTurnon": roomInsTurnonStep}})

    def delInsTurnonStep(self, roomName, deviceName, stepID):
        room = self.db.find_one({"roomName": roomName})
        roomInsTurnonStep = room["insTurnon"]
        if roomInsTurnonStep.get(deviceName) is None:
            print("Err: Invalid Device Name")
        elif len(roomInsTurnonStep[deviceName]) <= stepID:
            return "Err: Invalid StepID!"
        else:
            roomInsTurnonStep[deviceName].pop(stepID)

        self.db.update_one({"_id": room["_id"]}, {'$set': {"insTurnon": roomInsTurnonStep}})
        return

    def checkInsTurnonStepList(self, roomName, deviceList):
        room = self.db.find_one({"roomName": roomName})
        if room["insTurnon"] == {}: return self.insTurnonInit(room, deviceList)
        else: return room["insTurnon"]

    def printInsTurnonStepList(self, roomName, deviceList):
        roomInsTurnonStep = self.checkInsTurnonStepList(roomName, deviceList)
        # print(roomInsTurnonStep)
        for dev, step in roomInsTurnonStep.items():
            print(dev + ": ")
            for i in range(0, len(step)):
                print("Step " + str(i) + ": " + step[i]['text'] + " " + step[i]['image'] + " " + step[i]['command'] + " " + step[i]['help'])
        print()
        return

    def updateInsPairDev(self, roomName, pairID, deviceInvolved):
        room = self.db.find_one({"roomName": roomName})
        roomInsPairList = room["insPair"]
        if len(roomInsPairList) <= pairID: return "Err: Invalid PairID!"
        roomInsPairList[pairID]["devices"] = deviceInvolved
        self.db.update_one({"_id": room["_id"]}, {'$set': {"insPair": roomInsPairList}})
    
    def addInsPairStep(self, roomName, pairID, stepID, stepText='', stepImg='', stepCom='', stepHelp=''):
        room = self.db.find_one({"roomName": roomName})
        roomInsPairList = room["insPair"]
        if len(roomInsPairList) <= pairID: return "Err: Invalid PairID!"
        
        stepInfo = {}
        stepInfo['text'] = stepText
        stepInfo['image'] = stepImg
        stepInfo['command'] = stepCom
        stepInfo['help'] = stepHelp

        if len(roomInsPairList[pairID]["instruction"]) > stepID:
            roomInsPairList[pairID]["instruction"][stepID] = stepInfo
        else:
            roomInsPairList[pairID]["instruction"].append(stepInfo)

        self.db.update_one({"_id": room["_id"]}, {'$set': {"insPair": roomInsPairList}})
    
    def delInsPairStep(self, roomName, pairID, stepID):
        room = self.db.find_one({"roomName": roomName})
        roomInsPairList = room["insPair"]
        if len(roomInsPairList) <= pairID: return "Err: Invalid PairID!"
        elif len(roomInsPairList[pairID]["instruction"]) <= stepID: return "Err: Invalid StepID!"
        else: roomInsPairList[pairID]["instruction"].pop(stepID)

        self.db.update_one({"_id": room["_id"]}, {'$set': {"insPair": roomInsPairList}})

    def addInsPair(self, roomName, pairID):
        room = self.db.find_one({"roomName": roomName})
        roomInsPairList = room["insPair"]
        init = {"devices": [], "instruction": []}
        if len(roomInsPairList) <= pairID: roomInsPairList.append(init)
        self.db.update_one({"_id": room["_id"]}, {'$set': {"insPair": roomInsPairList}})

    def delInsPair(self, roomName, pairID):
        room = self.db.find_one({"roomName": roomName})
        roomInsPairList = room["insPair"]
        if len(roomInsPairList) > pairID: roomInsPairList.pop(pairID)
        self.db.update_one({"_id": room["_id"]}, {'$set': {"insPair": roomInsPairList}})
        return

    def checkInsPairStepList(self, roomName, pairID):
        room = self.db.find_one({"roomName": roomName})
        roomInsPairList = room["insPair"]
        if len(roomInsPairList) <= pairID: return "Err: Invalid PairID!"
        return roomInsPairList[pairID]

    def printInsPairStepList(self, roomName, pairID):
        roomInsPairStep = self.checkInsPairStepList(roomName, pairID)
        for i in range(0, len(roomInsPairStep["instruction"])):
            print("Step: " + str(i))
            print(roomInsPairStep["instruction"][i])

    def checkInsPairList(self, roomName):
        room = self.db.find_one({"roomName": roomName})
        roomInsPairList = room["insPair"]
        return roomInsPairList

    def printInsPairList(self, roomName):
        roomInsPairList = self.checkInsPairList(roomName)
        for i in range(0, len(roomInsPairList)):
            print("Case: " + str(i))
            print("Device Involved: ")
            print(roomInsPairList[i]["devices"])

    def addInsZoom(self, roomName, devtype, stepID, stepText='', stepImg=''):
        room = self.db.find_one({"roomName": roomName})
        roomInsZoomList = room["insZoom"]

        stepInfo = {}
        stepInfo['text'] = stepText
        stepInfo['image'] = stepImg
        
        if len(roomInsZoomList[devtype]) > stepID: roomInsZoomList[devtype][stepID] = stepInfo
        else: roomInsZoomList[devtype].append(stepInfo)

        self.db.update_one({"_id": room["_id"]}, {'$set': {"insZoom": roomInsZoomList}})

    def delInsZoom(self, roomName, devtype, stepID):
        room = self.db.find_one({"roomName": roomName})
        roomInsZoomList = room["insZoom"]
        if len(roomInsZoomList[devtype]) <= stepID: return "Err: Invalid stepID!"
        else: roomInsZoomList[devtype].pop(stepID)

        self.db.update_one({"_id": room["_id"]}, {'$set': {"insZoom": roomInsZoomList}})

    def checkInsZoomList(self, roomName):
        room = self.db.find_one({"roomName": roomName})
        roomInsZoomList = room["insZoom"]
        return roomInsZoomList

    def printInsZoomList(self, roomName):
        roomInsZoomList = self.checkInsZoomList(roomName)
        print("video")
        for i in range(0, len(roomInsZoomList["video"])):
            print("Step: " + str(i))
            print(roomInsZoomList["video"][i])
        print("audio")
        for i in range(0, len(roomInsZoomList["audio"])):
            print("Step: " + str(i))
            print(roomInsZoomList["audio"][i])
        return

db = connection("AVATA")
accountdb = AccountDB(db)
devicedb = DeviceDB(db)
roomdb = RoomDB(db)