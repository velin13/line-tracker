PARTITION_NUM = 4

import cv2
import math
from Fragment import Fragment
from FragmentProcessor import FragmentProcessor

class Frame:
    def __init__(self, image):

        if (image.shape[0] != 1280 and image.shape[1] != 720):
            raise Exception(image.shape[0] + "x" + image.shape[1] + " is not 1280x720")

        self.height = image.shape[0]
        self.width = image.shape[1]
        
        self.image = image

        self.fragments = FragmentProcessor.partition(image)
        self.processedFrame = FragmentProcessor.consolidate(self.fragments)

    def calculateVariation(self):
        # Tentative/Placeholder algorithm

        # Obtain top-most and bottom-most center points
        top = self.fragments[0]
        bottom = self.fragments[PARTITION_NUM - 1]
    
        # Draw line between expected center point (top) and skewed point (bottom)
        cv2.line(self.processedFrame, (top.relativeContourCtrX, top.relativeContourCtrY), (bottom.relativeImageCtrX, bottom.relativeImageCtrY), (255, 0, 0), 2)
        
        # Calculate variation (distance away from center)
        currentError = (-1) * int(math.degrees(math.atan((top.relativeContourCtrX - bottom.relativeImageCtrX) / (top.relativeContourCtrY- bottom.relativeImageCtrY))))
        return currentError