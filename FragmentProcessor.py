import cv2
import numpy as np
from Fragment import Fragment

class FragmentProcessor(object):
    """ Fragment Processor partitions and consolidates processed fragments """

    @staticmethod
    def partition(frame):
        """ Partition Frame into processed fragments 
        
        Args:
            frame (np.ndarry): Frame to partition.
        
        Returns: 
            A list of Fragments derived from Frame.
        """
        height, width = frame.shape[:2]
        partitionSize = height//4
        fragments = []

        for i in range(4):
            startPartition = i * partitionSize
            # Extract and color-process fragment
            fragment = Fragment(frame[startPartition:(startPartition + partitionSize), 0:width])

            # Set center points to be relative to full Frame
            fragment.setRelativeContourCtrX(0)
            fragment.setRelativeImageCtrX(0)
            fragment.setRelativeContourCtrY(startPartition)
            fragment.setRelativeImageCtrY(startPartition)

            fragments.append(fragment)

        return fragments

    @staticmethod
    def consolidate(fragments):
        """ Consolidate partitioned Fragments.
        
        Args:
            fragments (list[Fragment]): Fragments to consolidate.
        
        Returns: 
            A 2D array of consolidated fragments.
        """
        frame = fragments[0].processedFragment

        # Concatenate fragments into one Frame
        for i in range(1, len(fragments)):
            frame = np.concatenate((frame, fragments[i].processedFragment), axis=0)
            
        return frame
