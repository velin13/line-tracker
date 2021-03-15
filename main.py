import cv2
#from Link import Link
from Frame import Frame
from Controller import Controller

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)

    # Check if succeeded to connect to the camera
    if capture.isOpened() == None:  
        cv2.CV_Assert("Cam open failed")

    controller = Controller()

    while(1):

        retVal, image = capture.read()
        if retVal:
            # Initialize filtered and processed Frame
            frame = Frame(image)
            turnAngle = controller.pid(frame.calculateVariation())

            cv2.imshow("Processed Frame", frame.processedFrame)
            
            #Link.transmit(turnAngle)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break
        
    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()