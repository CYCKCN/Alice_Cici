import argparse
from unicodedata import name
import pymongo
from pymongo import MongoClient
from gridfs import GridFS
from db import AccountDB, DeviceDB, RoomDB
import argparse

# def get_parser():
#     parser = argparse.ArgumentParser(description="database development test")
#     parser.add_argument("--url", type=str, required=True, help="mongodb atlas connect your application")
#     parser.add_argument("--dbname", type=str, required=True, choices=['AVATA', 'AVATA_room', 'AVATA_account'])
#     return parser.parse_args()

def connection(dbname):
    # mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/myFirstDatabase?retryWrites=true"&"w=majority
    addr = "mongodb+srv://shaunxu:Xyz20010131@cluster0.llrsd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(addr)
    db = client[dbname]
    return db

def testdevicedb(db):
    devicedb = DeviceDB(db)
    devicedb.cleardb()

    devicedb.addDevice(0, "IEDA Conference Room, Room 5554", "project_1", "display_projector_WIFI", "000.00.000.000:0000", 1, 2)
    devicedb.addDevice(1, "IEDA Conference Room, Room 5554", "project_2", "display_projector_WIFI", "000.00.000.000:0000", 1, 2)
    devicedb.addDevice(2, "IEDA Conference Room, Room 5554", "project_3", "display_projector_WIFI", "000.00.000.000:0000", 1, 2)
    devicedb.addDevice(2, "IEDA Conference Room, Room 5554", "project_4", "display_projector_WIFI", "000.00.000.000:0000", 1, 2)
    devicedb.addDevice(3, "IEDA Conference Room, Room 5554", "project_7", "display_projector_WIFI", "000.00.000.000:0000", 1, 2)

    devicedb.printDeviceList("5554")

    devicedb.delDevice(0, "IEDA Conference Room, Room 5554")

    devicedb.printDeviceList("5554")

def testroomdb(db):
    roomdb = RoomDB(db)
    devicedb = DeviceDB(db)
    roomdb.cleardb()

    roomdb.addRoom("IEDA Conference Room, Room 5554", "", "Academic Building")
    roomdb.addRoom("Room 5554", "", "Academic Building")

    roomdb.printRoomList()

    roomdb.delRoom("Room 5554")

    roomdb.printRoomList()

    # roomdb.addInsInitialStep("IEDA Conference Room, Room 5554", 0, "et1", "ei1", "ec1", "eh1")
    # roomdb.addInsInitialStep("IEDA Conference Room, Room 5554", 1, "et2", "ei2", "ec2", "eh2")
    # roomdb.addInsInitialStep("IEDA Conference Room, Room 5554", 1, "et3", "ei3", "ec3", "eh3")
    # roomdb.addInsInitialStep("IEDA Conference Room, Room 5554", 2, "et7", "ei7", "ec7", "eh7")

    # roomdb.printInsInitialStepList("IEDA Conference Room, Room 5554")
    # roomdb.delInsInitialStep("IEDA Conference Room, Room 5554", 1)
    # roomdb.printInsInitialStepList("IEDA Conference Room, Room 5554")

    # devicelist = devicedb.checkDeviceList("IEDA Conference Room, Room 5554")
    # roomdb.checkInsTurnonStepList("IEDA Conference Room, Room 5554", devicelist)

    # roomdb.addInsTurnonStep("IEDA Conference Room, Room 5554", "project_2", 0, "et1", "ei1", "ec1", "eh1")
    # roomdb.addInsTurnonStep("IEDA Conference Room, Room 5554", "project_2", 1, "et2", "ei2", "ec2", "eh2")
    # roomdb.addInsTurnonStep("IEDA Conference Room, Room 5554", "project_2", 1, "et3", "ei3", "ec3", "eh3")
    # roomdb.addInsTurnonStep("IEDA Conference Room, Room 5554", "project_2", 2, "et9", "ei9", "ec9", "eh9")
    # roomdb.addInsTurnonStep("IEDA Conference Room, Room 5554", "project_7", 0, "et7", "ei7", "ec7", "eh7")

    # roomdb.printInsTurnonStepList("IEDA Conference Room, Room 5554", devicelist)

    # roomdb.delInsTurnonStep("IEDA Conference Room, Room 5554", "project_2", 1)

    # roomdb.printInsTurnonStepList("IEDA Conference Room, Room 5554", devicelist)

    # roomdb.addInsPair("IEDA Conference Room, Room 5554", 0)
    # roomdb.updateInsPairDev("IEDA Conference Room, Room 5554", 0, ["project_2", "project_4"])

    # roomdb.addInsPairStep("IEDA Conference Room, Room 5554", 0, 0, "et1", "ei1", "ec1", "eh1")
    # roomdb.addInsPairStep("IEDA Conference Room, Room 5554", 0, 1, "et2", "ei2", "ec2", "eh2")
    # roomdb.addInsPairStep("IEDA Conference Room, Room 5554", 0, 1, "et3", "ei3", "ec3", "eh3")
    # roomdb.addInsPairStep("IEDA Conference Room, Room 5554", 0, 2, "et9", "ei9", "ec9", "eh9")
    # roomdb.delInsPairStep("IEDA Conference Room, Room 5554", 0, 1)

    # roomdb.printInsPairList("IEDA Conference Room, Room 5554")
    # roomdb.printInsPairStepList("IEDA Conference Room, Room 5554", 0)

    roomdb.addInsZoom("IEDA Conference Room, Room 5554", 'video', 0, "et1", "ei1")
    roomdb.addInsZoom("IEDA Conference Room, Room 5554", 'video', 1, "et2", "ei2")
    roomdb.addInsZoom("IEDA Conference Room, Room 5554", 'video', 1, "et3", "ei3")
    roomdb.addInsZoom("IEDA Conference Room, Room 5554", 'video', 2, "et9", "ei9")
    roomdb.delInsZoom("IEDA Conference Room, Room 5554", 'video', 1)
    roomdb.addInsZoom("IEDA Conference Room, Room 5554", 'audio', 0, "et7", "ei7")

    roomdb.printInsZoomList("IEDA Conference Room, Room 5554")


if __name__ == '__main__':
    # args = get_parser()
    db = connection("AVATA")

    # print("successful")

    accountdb = AccountDB(db)   

    # testdevicedb(db)
    testroomdb(db)
    
    # devices = db["devices"]
    # controllers = db["controllers"]
    # fs = GridFS(db)
    # file = "ieda.jpg"
    # with open(file, 'rb') as f:
    #     image = f.read()
    # stored = fs.put(image, filename='files')

    