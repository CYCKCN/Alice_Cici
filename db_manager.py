from app.database.db import accountdb, devicedb, roomdb
from werkzeug.security import generate_password_hash, check_password_hash
import argparse

if __name__ == '__main__':
    # accountdb.cleardb()
    # devicedb.cleardb()
    # roomdb.cleardb()

    # roomdb.addRoom("5554", "", "Academic Building")
    # roomdb.addRoom("4223", "", "Academic Building")
    pwd = "11111111"
    # accountdb.register("cyckcn@gmail.com", pwd)
    # accountdb.register("cyckcn@ust.com", pwd)
    # accountdb.register("admin@ust.com", pwd)
    # accountdb.updateAdminID("admin@ust.com")
    # roomdb.setRoomBookByUser("5554", "20220630", "admin@ust.com", "1100", "1300")
    # roomdb.setRoomBookByUser("5554", "20220730", "admin@ust.com", "0800", "1000")
    # roomdb.setRoomBookByUser("5554", "20220630", "admin@ust.com", "0900", "1000")

    # roomdb.setRoomBookByUser("4223", "20220630", "admin@ust.com", "0800", "0900")
    
    # bookInfo_list = roomdb.checkUserBooking("admin@ust.com")
    # bookInfo_dict = dict.fromkeys(bookInfo_list)
    # print(bookInfo_list)

    # devicedb.addDevice("5554", "device001", "", "", "358", "782")
    # devicedb.addDevice("5554", "device002", "", "", "654", "468")

    # roomdb.addInsInitialStep("5554", 0, "et1", "ei1", "ec1", "eh1")
    # roomdb.addInsInitialStep("5554", 1, "et2", "ei2", "ec2", "eh2")
    # roomdb.addInsInitialStep("5554", 1, "et3", "ei3", "ec3", "eh3")
    # roomdb.addInsInitialStep("5554", 2, "et7", "ei7", "ec7", "eh7")

    # roomdb.printInsInitialStepList("5554")
    # roomdb.db.update_one({"roomName": "4223"}, {'$set': {'bookTime': {}}})
    # roomdb.db.update_one({"roomName": "4223"}, {'$set': {'bookBy': {}}})
    accountdb.db.update_one({"accountEmail": "cyckcn@gmail.com"}, {'$set': {'room': "", 'personal': "", "device": []} })

    