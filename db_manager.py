from platform import system
from app.database.db import accountdb, roomdb, systemdb
from werkzeug.security import generate_password_hash, check_password_hash
import argparse

test_case_device = {
    0: [],
    1: ["projector-screen"],
    2: ["win"],
    3: ["win", "projector-screen"],
    4: ["apple"],
    5: ["apple", "projector-screen"],
    6: ["pc"],
    7: ["visulizer"],
    8: ["mic4me"],
    9: ["hand-held mic"],
    10: ["table-mic"],
    11: ["mic4me", "speaker"],
    12: ["hand-held mic", "speaker"],
    13: ["table-mic", "speaker"],
    14: ["zoom", "mic4me"],
    15: ["error", "need to be delete"],
    16: ["zoom", "webcam"],
    17: ["zoom", "speaker"],
    18: ["zoom"],
}
test_case_step = {
    0: {
        0: {"text": "Find the control box.", "image": "", "command": ""},
        1: {"text": "Press “System On” on the control box.", "image": "", "command": ""},
    },
    1: {
        0: {"text": "Press on the device logo on the control box to turn on the corresponding projector.", "image": "projector-screen-1.JPG", "command": ""},
        1: {"text": "Press on the “Freeze” button on the control box to keep the current sharing staying on the screen. Press again to stop freezing.", "image": "projector-screen-2.JPG", "command": ""},
        2: {"text": "Press on the “Screen” button on the control box to enter the screen up and down controlling page.", "image": "projector-screen-3.JPG", "command": ""},
    },
    2: {
        0: {"text": "Select “Notebook” on the control box.", "image": "win_projector-screen-1.JPG", "command": ""},
        1: {"text": "Find HDMI cable below the lectern table.", "image": "win_projector-screen-2.JPG", "command": ""},
        0: {"text": "Plug the HDMI in your laptop.", "image": "win_projector-screen-3.JPG", "command": ""},
    },
    3: {
        0: {"text": "Press “Fn” and “F7” on your laptop keyboard.", "image": "win_projector-screen-4.JPG", "command": ""},
        1: {"text": "Select “Duplicate” on pop-up window.", "image": "win_projector-screen-5.JPG", "command": ""},
    },
    4: {
        0: {"text": "Select “Apple TV” on the control box", "image": "apple_projector-screen-1.png", "command": ""},
        1: {"text": "Make sure that your Apple device is connecting to the same Wi-Fi as the Apple TV.", "image": "", "command": ""},
    },
    5: {
        0: {"text": "Open the control center on your Apple device and select corresponding Apple TV in Screen Mirroring.", "image": "apple_projector-screen-3.png", "command": ""},
        1: {"text": "Enter the AirPlay code shown on the screen to pop-up box on your Apple device", "image": "apple_projector-screen-4.png", "command": ""},
    },
    6: {
        0: {"text": "Find the host below the lectern table and press the power button.", "image": "pc-1.JPG", "command": ""},
        1: {"text": "Press the power button on the right bottom corner of the monitor.", "image": "pc-2.JPG", "command": ""},
        2: {"text": "Select “Lectern PC” on the control box", "image": "pc_projector-screen-1.JPG", "command": ""},
    },
    7: {
        0: {"text": "Pull the visualizer camera up.", "image": "visualizer-1.JPG", "command": ""},
        1: {"text": "Press on the “Freeze” button on the visualizer to keep the current sharing staying on the screen. Press again to stop freezing.", "image": "", "command": ""},
        2: {"text": "Press on the “Focus” button on the visualizer.", "image": "", "command": ""},
        3: {"text": "Press on the “Light” button on the visualizer.", "image": "", "command": ""},
        4: {"text": "err", "image": "err", "command": ""},
        5: {"text": "Press on the “Extern” button on the visualizer.", "image": "", "command": ""},
        6: {"text": "Select “Visualizer” on the control box.", "image": "visualizer_projector-screen-1.JPG", "command": ""},
    },
    8: {
        0: {"text": "", "image": "", "command": ""},
    },
    9: {
        0: {"text": "", "image": "", "command": ""},
    },
    10: {
        0: {"text": "", "image": "", "command": ""},
    },
    11: {
        0: {"text": "", "image": "", "command": ""},
    },
    12: {
        0: {"text": "", "image": "", "command": ""},
    },
    13: {
        0: {"text": "", "image": "", "command": ""},
    },
    14: {
        0: {"text": "", "image": "", "command": ""},
    },
    15: {
        0: {"text": "err", "image": "err", "command": "err"},
    },
    16: {
        0: {"text": "", "image": "", "command": ""},
    },
    17: {
        0: {"text": "", "image": "", "command": ""},
    },
    18: {
        0: {"text": "If you want to share the computer sound, please select the left bottom option “Share sound”.", "image": "zoom-1.png", "command": ""},
    },
}

addDeviceNameList = ["projector-1", "projector-2", "Speaker", "Microphone", "Visualizer", "Lectern PC"]
addDeviceTypeList = ["projector-screen", "projector-screen", "speaker", "mic4me", "visualizer", "pc"]

if __name__ == '__main__':
    systemdb.cleardb()
    # systemdb.createSystem("AMX")
    # deviceTypeList = ["speaker", "projector-screen", "mic4me", "hand-held mic", "table mic", "webcam", "visualizer", "pc", "display TV"]
    # for deviceType in deviceTypeList:
    #     systemdb.addDeviceType("AMX", deviceType)
    # systemdb.delDeviceType("AMX", "display TV")
    # # print(systemdb.checkDeviceTypeDict("AMX"))
    # for caseID in range(19):
    #     for stepID in range(len(test_case_step[caseID])):
    #         systemdb.addCaseStep("AMX", str(caseID), str(stepID), test_case_step[caseID][stepID]["text"], test_case_step[caseID][stepID]["image"], test_case_step[caseID][stepID]["command"])
    #     systemdb.addCaseDevice("AMX", str(caseID), test_case_device[caseID])
    # systemdb.delCaseStep("AMX", "7", "4")
    # systemdb.deleteCase("AMX", "15")
    roomdb.cleardb()
    # # devicedb.cleardb()
    # roomdb.addRoom("4504", "Academic Building, 4F, Lift 25-26", "AMX")
    # for i in range(len(addDeviceNameList)):
    #     roomdb.addDevice("4504", str(i + 4), addDeviceNameList[i], addDeviceTypeList[i], "", i + 4, i + 4)

    # room = roomdb.getroom("4504")
    # system = systemdb.getsystem("AMX")
    # roomInsPreview = roomdb.generateRoomPreview("4504", system["insDevice"], system["insCases"])

    # for i in range(len(roomInsPreview)):
    #     print(i)
    #     for k,v in roomInsPreview[str(i)].items():
    #         print(k)
    #         print(v)

    # print(roomInsPreview)
    # roomdb.addHelp("4504", "0", "0", "Location description of control box")
    # roomdb.addHelp("4504", "4", "1", "Wi-Fi name and password")
    # roomdb.addHelp("4504", "5", "0", "Apple TV name")

    # userDeviceIDList = ["1", "4", "6", "7"]
    # userpreview = roomdb.generateUserPreview("4504", userDeviceIDList)

    # for i in range(len(userpreview)):
    #     print(i)
    #     for k,v in userpreview[str(i)].items():
    #         print(k)
    #         print(v)
    
    # pwd = "11111111"
    # accountdb.register("admin@ust.com", pwd)
    # accountdb.updateAdminID("admin@ust.com")


    