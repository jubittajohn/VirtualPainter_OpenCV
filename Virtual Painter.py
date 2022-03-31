#Virtual Painter
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 580)
cap.set(10, 175)

myColors = [[89,82,101,137,255,255],  #blue - hsv min and max values
            [47,45,62,83,255,255],  #green
            [0,124,167,10,182,255], #orange
            [146,131,103,179,255,255]] #red
myColorVals = [[213,240,12],    #blue - bgr code
               [32,92,4],       #green
               [9,91,232],       #orange
               [5,5,250]]       #red
myPoints = [] # x,y,colorId

def findColor(img, myColors, myColorVals):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []

    for color in myColors:
        lower = np.array(myColors[count][0:3])
        upper = np.array(myColors[count][3:6])
        mask = cv2.inRange(imgHsv, lower, upper)

        x, y = getContours(mask)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count += 1
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0

    for cnt in contours:
        area = cv2.contourArea(cnt)  #Finding area of the contours one by one

        if area> 300:             #Giving threshold for area to avoid noise
            #cv2.drawContours(imgResult, cnt, -1, (0,0,200), 3)
            peri = cv2.arcLength(cnt, True)  #To find the perimeter
            approx = cv2.approxPolyDP(cnt, 0.02*peri,True)  #to return the corner points
            x,y, w, h = cv2.boundingRect(approx)   # to define the dimensions of the bounding rectangle
    return x+w//2,y

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 9  , myColorVals[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()

    newPoints = findColor(img, myColors, myColorVals)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorVals)

    cv2.imshow("Video", imgResult)
    if cv2.waitKey(30) & 0xFF ==ord('q'):
        break