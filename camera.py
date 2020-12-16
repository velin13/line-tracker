import cv2
import numpy as np
import math
# Open the device at the ID 0
cap = cv2.VideoCapture(0)

PARTITION_NUM = 4

Kp = 0
Ki = 0
Kd = 0
lastError = 0
sumError = 0

def pid(currError):
    sumError = sumError + currError
    turnAngle = (currError * Kp) + (sumError * Ki) + ((currError - lastError) * Kd)
    lastError = currError

    if (sumError > 500):
        sumError = 500
    else if (sumError < -500):
        sumError = 500

    # TODO adjust the turn angle
    print(turnAngle)
# Check whether user selected camera is opened successfully.

if not (cap.isOpened()):
    print("Could not open video device")

def split(image, numPartitions):
    height, width = image.shape[:2]
    partitionSize = int(height / numPartitions)
    images = []

    currentError = 0

    for i in range(numPartitions):
        startPartition = i * partitionSize
        partition = image[startPartition:startPartition+partitionSize, 0:width]
        e = process(partition)
        currentError = currentError + e
        images.append(partition)
    
    reconstructImage(images)
       
    return float(currentError)/PARTITION_NUM

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

    return distance

def reconstructImage(images):
    fullImage = images[0]

    for i in range(1, len(images)):
        fullImage = np.concatenate((fullImage, images[i]), axis=0)
 
    cv2.imshow("preview", fullImage)

while(True):

    # Capture frame-by-frame
    ret, frame = cap.read()

    error = split(frame, PARTITION_NUM)
    pid(error)

    #Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture

cap.release()

cv2.destroyAllWindows()
