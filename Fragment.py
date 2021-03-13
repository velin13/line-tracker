import cv2

class Fragment:
    def __init__(self, image):
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


        process()

    def setRelativeImageCtrY(offset):
        self.relativeImageCtrY = self.imageCtrY + offset

    def setRelativeImageCtrX(offset):
        self.relativeImageCtrX = self.imageCtrX + offset

     def setRelativeContourCtrY(offset):
        self.relativeContourCtrY = self.contourCtrY + offset

    def setRelativeContourCtrX(offset):
        self.relativeContourCtrX = self.contourCtrX + offset

    def process():
        imgray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(imgray, (7, 7), 0)
        ret, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            # TODO M['m00'] = 0 fix division by 0

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            self.contourCtrX = cx
            self.contourCtrY = cy

            cv2.circle(self.processedFragment, (cx,cy), 4, (255,255,255), 2)
            cv2.drawContours(self.processedFragment, contours, -1, (0,255,0), 1)

        cv2.circle(self.processedFragment, (self.width, self.height), 4, (0, 0, 255), 2)
        distance = self.imageCtrX - self.contourCtrX
    
        cv2.putText(self.processedFragment, str(distance), (self.imageCtrX, self.imageCtrY), cv2.FONT_HERSHEY_SIMPLEX, .75, (255,0,0), 2)