@Singleton
class Controller:
    """ Proportional-Integral-Derivative (PID) Controller
    """
    def __init__(self):
        """ Inits Controller """

        self.Kp = .75
        self.Ki = .25
        self.Kd = .25

        self.lastError = 0
        self.currentError = 0
        self.sumError = 0
        self.turnAngle = 0

    def pid(self, currentError):
        """ Calculates Turn Angle 
        
        Args:
            currentError (int): Current variation from expected center point.
        
        Returns: 
            Returns calculated turn angle.
        """
        self.sumError = self.sumError + self.currentError
        self.turnAngle = (self.currError * self.Kp) + (self.sumError * self.Ki) + ((self.currError - self.lastError) * self.Kd)
        self.lastError = self.currentError

        # Sum Error should not exceed +/- 500
        if (self.sumError > 500):
            self.sumError = 500
        elif (self.sumError < - 500):
            self.sumError = - 500

        # Debug print statements
        print("Current Error:", self.currError)
        print("Last Error:", self.lastError)
        print("Sum Error:", self.sumError)
        print("Turn Angle:", self.turnAngle)
        return turnAngle