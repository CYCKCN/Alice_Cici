import email
from platform import system
from app.database.db import accountdb, roomdb, systemdb
from werkzeug.security import generate_password_hash, check_password_hash
import argparse

if __name__ == '__main__':
    print("Input Existing Email to Identify as ADMIN (input q to quit): ")
    while(1):
        emailID = input()
        if emailID == 'q': break
        account = accountdb.findUser(emailID)
        if account:
            accountdb.updateAdminID(emailID)
            print("Update   " + emailID + "   successfully as ADMIN!")
            print("Input Another Existing Email to Identify as ADMIN (input q to quit): ")
        else:
            print("please input existing eamil (input q to quit): ")
