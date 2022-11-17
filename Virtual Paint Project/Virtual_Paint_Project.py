import cv2
import numpy as np
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)             #setting height
cap.set(4,frameHeight)              #setting width
cap.set(10,150)             #setting brightness

myColors = [[0,13,235,255,255,255],   #red
            [56,93,51,255,55,127],  #green
            [0,179,223,245,255,255]]  #blue    #Adding colours here
myColorValues = [[0,0,255],
                 [0,255,0],
                 [255,255,51]]
myPoints = []  ##[x,y, colorId]



def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    #cvtColor is used to convert an image from one color space to another.
                                            #here HSV stands for Hue, Saturation and Val
    count=0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)  #Defining the boundaries for showing mask
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        #cv2.imshow(str(color[2]),mask)
    return newPoints

def getContours(img):       #Contours means outlining something.
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)   #RETR_EXTERNAL only retrieves extreme outer layers.
    x,y,w,h = 0,0,0,0
    for cnt in contours:                             #CHAIN_APPROX_NONE stores all contour points.
        area = cv2.contourArea(cnt)
        if area>500:
            # cv2.drawContours(imgResult,cnt,-1, (255,0,0),3)
            peri = cv2.arcLength(cnt,True)  #calculating curve length eventually helping in detecting corner shapes
            # print(peri), and arcLength is length of circumference of circle.
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)  #used to perform an approximation of a shape of a contour. x
            x, y, w, h=cv2.boundingRect(approx)
    return x+w//2,y #Representing top point of colour

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)
while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
