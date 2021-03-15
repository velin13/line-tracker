import cv2
import numpy as np
from Frame import Frame
from Fragment import Fragment

@Singleton
class FragmentProcessor:
    def __init__(self):
        pass

    def partition(self, frame: np.ndarray) -> list[Fragment]:
        partitionSize = frame.height / 4
        fragments = []

        for i in range(4):
            startPartition = i * partitionSize
            
            # Extract and color-process fragment
            fragment = Fragment(frame[startPartition:startPartition + partitionSize, 0:frame.width])

            # Set center points to be relative to full Frame
            fragment.setRelativeContourCtrX(0)
            fragment.setRelativeImageCtrX(0)
            fragment.setRelativeContourCtrY(startPartition)
            fragment.setRelativeImageCtrY(startPartition)

            fragments.append(fragment)

        return fragments

    def consolidate(self, fragments: Fragment) -> np.ndarry:
        frame = fragments[0].processedFragment

        # Concatenate fragments into one Frame
        for i in range(1, len(fragments)):
            frame = np.concatenate((frame, fragments[i]), axis=0)
        
        cv2.imshow("Processed Image", frame)
        return frame
