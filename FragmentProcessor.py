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