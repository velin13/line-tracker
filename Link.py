import serial
from Singleton import Singleton

@Singleton
class Link(object):
    """ Link performs initial setup to Arduino and Camera. """
    def __init__(self):
        """ Initializes Link """
        self.serial = None

    def connect(self):
        """ Connects to Arduino """
        self.serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.serial.flush()

    def transmit(self, package):
        """ Sends information to Arduino """
        self.serial.write(str.encode(str(round(package) + 90)))

    def receive(self):
        """ Retrieves information from Arduino """
        return self.serial.readline().decode('utf-8').rstrip()