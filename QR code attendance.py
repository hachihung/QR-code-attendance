import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time

# error importing pyzbar
# Windows fix: download Visual C++ from
# https://www.microsoft.com/en-us/download/confirmation.aspx?id=40784
# install xcode
# MacOS: brew install zbar

# open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1024)   # set screen width
cap.set(4, 768)    # set screen height

# open text files storing visitor's enrollment data and attending session data
with open("enrollment.txt", encoding="utf-8") as f:
    myDataList = f.read().splitlines()

with open("session.txt", encoding="utf-8") as s:
    sessionList = s.read().splitlines()

# open log file, "a" = append, for storing visitor's attendance data
logfile = open("log.txt", "a", encoding="utf-8")
lastData = ""

while True:
    # cap image from webcam
    success, img = cap.read()
    index = 0
    for qrcode in decode(img):
        # decode QR code, crucial function
        myData = qrcode.data.decode("utf-8")  # QR code data
        print(myData)

        # check whether visitor's QR code info matches with enrollment data file
        if myData in myDataList:
            myOutput = "Enrolled"
            myColor = (0,255,0)
            index = myDataList.index(myData)
            if myData != lastData:
                logfile.write(myData + " " + time.ctime() + "\n")
            lastData = myData
            # display session info in output window
            print(sessionList[index])
        else:
            myOutput = "Not Enrolled"
            myColor = (0,0,255)

        # draw rectangle around QR code, put visitor's info on screen
        pts = np.array([qrcode.polygon], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = qrcode.rect
        cv2.putText(img, myOutput + " " + myData, (pts2[0], pts2[1]-50), cv2.FONT_HERSHEY_PLAIN, 1.8, myColor, 2)
        cv2.putText(img, sessionList[index], (pts2[0], pts2[1]-10), cv2.FONT_HERSHEY_PLAIN, 1.8, myColor, 2)

    cv2.imshow("Result", img)
    cv2.waitKey(1)

# close (save) log file of attendance
logfile.close()
