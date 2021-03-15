import cv2
from Link import Link
from Frame import Frame
from Controller import Controller

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)

    while(1):

        retVal, image = capture.read()
        if retVal:
            # Initialize filtered and processed Frame
            frame = Frame(image)
            turnAngle = Controller.pid(frame.calculateVariation())
            Link.transmit(turnAngle)
