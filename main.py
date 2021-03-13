import cv2

from Link import Link

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)

    while(1):

        retVal, image = caputre.read()
        if retVal:
            frame = Frame(image)
