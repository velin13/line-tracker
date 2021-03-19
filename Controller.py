from Singleton import Singleton

@Singleton
class Controller:
    """ Proportional-Integral-Derivative (PID) Controller
    """
    def __init__(self):
        """ Inits Controller """

        self.Kp = .75
        self.Ki = .25 / 100
        self.Kd = .25 / 100

        self.lastError = 0
        self.sumError = 0
        self.turnAngle = 0

    def pid(self, currentError):
        """ Calculates Turn Angle 
        
        Args:
            currentError (int): Current variation from expected center point.
        
        Returns: 
            Returns calculated turn angle.
        """
        self.sumError = self.sumError + currentError
        self.turnAngle = (currentError * self.Kp) + (self.sumError * self.Ki) + ((currentError - self.lastError) * self.Kd)
        self.lastError = currentError

        # Sum Error should not exceed +/- 500
        if (self.sumError > 500):
            self.sumError = 500
        elif (self.sumError < -500):
            self.sumError = -500

        # Debug print statements
        # print("Current Error:", self.currentError)
        # print("Last Error:", self.lastError)
        # print("Sum Error:", self.sumError)
        # print("Turn Angle:", self.turnAngle)
        return self.turnAngle