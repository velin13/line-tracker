import cv2

class Fragment:
    """ A Fragment holds a partitioned segment of an image capture

    Attributes:
        rawFragment (np.ndarray): Partitioned raw image.
        processedFragment (np.ndarry): Partitioned processed image.

        height (int): Fragment height.
        width (int): Fragment width.

        contourCtrX (int): X-coordinate of expected (line) center point.
        contourCtrY (int): Y-coordinate of expected (line) center point.

        relativeContourCtrX (int): X-coordinate of expected (line) center point relative to full frame.
        relativeContourCtrY (int): Y-coordinate of expected (line) center point relative to full frame.
        
        imageCtrX (int): X-coordinate of fragment's center point.
        imageCtrY (int): Y-coordinate of fragments's center point.

        relativeImageCtrX (int): X-coordinate of fragment's center point relative to full frame.
        relativeImageCtrY (int): Y-coordinate of fragment's center point relative to full frame.
    """
    def __init__(self, image):
        """ Inits Fragment

        Args:
        image (np.ndarry): Raw and segmented image.
        """
        self.rawFragment = image
        self.processedFragment = image

        self.height = image[0]
        self.width = image[1]

        self.contourCtrX = 0
        self.contourCtrY = 0

        self.relativeContourCtrX = 0
        self.relativeContourCtrY = 0

        self.imageCtrX = image[1] / 2
        self.imageCtrY = image[0] / 2

        self.relativeImageCtrX = 0
        self.relativeImageCtrY = 0

        # Filter colors and extract edges from individual fragment
        process()

    def setRelativeImageCtrY(self, offset):
        """ Add relative offset to relativeImageCtrY
        
        Args:
        offset (int): Offset.
        """
        self.relativeImageCtrY = self.imageCtrY + offset

    def setRelativeImageCtrX(self, offset):
        """ Add relative offset to relativeImageCtrX
        
        Args:
        offset (int): Offset.
        """
        self.relativeImageCtrX = self.imageCtrX + offset

    def setRelativeContourCtrY(self, offset):
        """ Add relative offset to relativeContourCtrY
        
        Args:
        offset (int): Offset.
        """
        self.relativeContourCtrY = self.contourCtrY + offset

    def setRelativeContourCtrX(self, offset):
        """ Add relative offset to relativeContourCtrX
        
        Args:
        offset (int): Offset.
        """
        self.relativeContourCtrX = self.contourCtrX + offset

    def process(self):
        """ Apply blur, grayscale, and threshold to image to extract edges (line) """
        
        # Obtain all contours from blurred, grayscaled, and thresholded image
        imgray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(imgray, (7, 7), 0)
        ret, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # Extract edges from contours
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            # TODO M['m00'] = 0 fix division by 0

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            # Center of line
            self.contourCtrX = cx
            self.contourCtrY = cy

            # Draw white circle on line's center point
            cv2.circle(self.processedFragment, (cx,cy), 4, (255,255,255), 2)
            cv2.drawContours(self.processedFragment, contours, -1, (0,255,0), 1)

        # Draw red circle on fragment's center point
        cv2.circle(self.processedFragment, (self.imageCtrX, self.imageCtrY), 4, (0, 0, 255), 2)
        
        # Calculate distance between image and contour center point
        distance = self.imageCtrX - self.contourCtrX
        cv2.putText(self.processedFragment, str(distance), (self.imageCtrX, self.imageCtrY), cv2.FONT_HERSHEY_SIMPLEX, .75, (255,0,0), 2)