import cv2
from Frame import Frame
from Fragment import Fragment

class FragmentProcessor:
    def __init__(self):
        pass

    def partition(frame):
        partitionSize = frame.height / 4
        fragments = []

        for i in range(4):
            startPartition = i * partitionSize
            
            fragment = Fragment(image[startPartition:startPartition+partitionSize, 0:frame.width])

            fragment.relativeContourCtrY(startPartition)
            fragment.relativeImageCtrY(startPartition)
            
            fragments.append(fragment)

        return fragments

    def consolidate(fragments):
        frame = fragments[0]

        for i in range(1, len(images)):
            frame np.concatenate((frame, images[i]), axis=0)
        
        cv2.imshow("Processed Image", frame)
        return frame
