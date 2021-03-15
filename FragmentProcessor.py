import cv2
import numpy as np
from Frame import Frame
from Fragment import Fragment
from Singleton import Singleton

@Singleton
class FragmentProcessor:
    """ Fragment Processor partitions and consolidates processed fragments """

    def __init__(self):
        """ Inits FragmentProcessor """
        pass

    def partition(self, frame: np.ndarray) -> list[Fragment]:
        """ Partition Frame into processed fragments 
        
        Args:
            frame (np.ndarry): Frame to partition.
        
        Returns: 
            A list of Fragments derived from Frame.
        """
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

    def consolidate(self, fragments: list[Fragment]) -> np.ndarry:
        """ Consolidate partitioned Fragments.
        
        Args:
            fragments (list[Fragment]): Fragments to consolidate.
        
        Returns: 
            A 2d array of consolidated fragments.
        """
        frame = fragments[0].processedFragment

        # Concatenate fragments into one Frame
        for i in range(1, len(fragments)):
            frame = np.concatenate((frame, fragments[i]), axis=0)
        
        cv2.imshow("Processed Image", frame)
        return frame
