import cv2
import numpy as np
import math
import time
import serial

# Open the device at the ID 0
cap = cv2.VideoCapture(0)

PARTITION_NUM = 4

class PartialImageInfo:
    def __init__(self, contour, center):
        self.contourCtrX = contour[0]
        self.contourCtrY = contour[1]
        self.imageCtrX = center[0]
        self.imageCtrY = center[1]
    
class Error:
    Kp = .75
    Ki = .25
    Kd = .25
    lastError = 0
    sumError = 0

error = Error()

def _map(x, in_min, in_max, out_min, out_max):
    return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min

def pid(error, currError):
    error.Kp = error.Kp/1.0
    error.Ki = error.Ki/1000.0
    error.Kd = error.Kd/100.0

    error.sumError = error.sumError + currError
    turnAngle = (currError * error.Kp) + (error.sumError * error.Ki) + ((currError - error.lastError) * error.Kd)
    print("currErr:", currError)
    print(" last Err:", error.lastError)
    error.lastError = currError

    if (error.sumError > 500):
        error.sumError = 500
    elif (error.sumError < -500):
        error.sumError = 500
    print(" sumErr:", error.sumError)
    # TODO adjust the turn angle
    print(" turnAngle:", turnAngle)
    return turnAngle
# Check whether user selected camera is opened successfully.

if not (cap.isOpened()):
    print("Could not open video device")

def split(image, numPartitions):
    height, width = image.shape[:2]
    partitionSize = int(height / numPartitions)
    images = []
    points = []

    currentError = 0

    for i in range(numPartitions):
        startPartition = i * partitionSize
        partition = image[startPartition:startPartition+partitionSize, 0:width]
        info = process(partition)
        
        # Adjust coordinate relative to full image
        info.contourCtrY = info.contourCtrY + startPartition
        info.imageCtrY= info.imageCtrY + startPartition
        
        points.append(info)
        images.append(partition)
    
    fullImage = reconstructImage(images)
    
    top = points[0]
    bottom = points[PARTITION_NUM - 1]
    
    cv2.line(fullImage, (top.contourCtrX, top.contourCtrY), (bottom.imageCtrX, bottom.imageCtrY), (255, 0, 0), 2)
    currentError = (-1) * int(math.degrees(math.atan((top.contourCtrX - bottom.imageCtrX) / (top.contourCtrY- bottom.imageCtrY))))

    cv2.putText(fullImage, str(currentError), (100,100), cv2.FONT_HERSHEY_SIMPLEX, .75, (0,255,0), 2)
    cv2.imshow("preview", fullImage)

    return currentError

def process(image):
    height, width = image.shape[:2]
    ctrImage = (int(width/2), int(height/2))
    ctrContourX = 0
    ctrContourY = 0

    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray, (7, 7), 0)
    ret, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV);
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        # TODO M['m00'] = 0 fix division by 0

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        ctrContourX = cx
        ctrContourY = cy

        cv2.circle(image, (cx,cy), 4, (255,255,255), 2)
        cv2.drawContours(image, contours, -1, (0,255,0), 1)

    cv2.circle(image, ctrImage, 4, (0, 0, 255), 2)
    distance = int(ctrImage[0] - ctrContourX)
    
    cv2.putText(image, str(distance), ctrImage, cv2.FONT_HERSHEY_SIMPLEX, .75, (255,0,0), 2)

    return PartialImageInfo((ctrContourX, ctrContourY), ctrImage)

def reconstructImage(images):
    fullImage = images[0]

    for i in range(1, len(images)):
        fullImage = np.concatenate((fullImage, images[i]), axis=0)
 
    cv2.imshow("preview", fullImage)
    
    return fullImage

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    
    while(True):

        # Capture frame-by-frame
        ret, frame = cap.read()

        e = split(frame, PARTITION_NUM)
        turnAngle = pid(error, e)
        #turnAngle = _map(pid(error, e), -90, 90, 5, 10);
        
        print("mapped turn angle:", turnAngle);
        print("-------------------------------")
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
        ser.write(str.encode(str(round(turnAngle)+90)))
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break
        

# When everything done, release the capture

cap.release()

cv2.destroyAllWindows()
