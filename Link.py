import serial

from Singleton import Singleton

@Singleton
class Link(object):
    def __init__(self):
        self.serial = None

    def connect(self):
        self.serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.serial.flush()

    def transmit(self, package):
        self.serial.write(str.encode(round(package) + 90))

    def receive(self):
        return self.serial.readline().decode('utf-8').rstrip()