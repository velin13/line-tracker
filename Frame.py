from Fragment import Fragment

class Frame:
    def __init__(self, image):

        if (image.shape[0] != 1280 and image.shape[1] != 720):
            raise Exception(image.shape[0] + "x" + image.shape[1] + " is not 1280x720")

        self.height = image.shape[0]
        self.width = image.shape[1]
        
        self.image = image
        self.ProcessedFrame = None

        self.fragment = None


    def calculateVariation():
        pass    
        