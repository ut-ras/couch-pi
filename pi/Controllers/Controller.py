

class Controller(object):
    """
    Parent class/Interface for all controller classes
    MotorPercent range: [-100, 100]     negative = reverse
    maxSpeed range: [0, 100]
    """
    def __init__(self,name="Generic Controller", maxSpeed=100):
        # name of Controller
        self.name = name
        self.leftMotorPercent = 0       
        self.rightMotorPercent = 0

        self.setMaxSpeed(maxSpeed)

    def setMaxSpeed(self, maxSpeed):
        if maxSpeed > 100:
            maxSpeed = 100
        elif maxSpeed < 0:
            maxSpeed = 0
        self.maxSpeed = maxSpeed

    def initialize(self):
        """
        Should connect to USB/Bluetooth or open ports
        """
        pass

    def startController(self):
        """
        Starts a thread that continuously updates Controller variables
        """
        pass

    def readAndUpdate(self):
        """
        Read in values and update self.leftMotorPercent and self.rightMotorPercent and other variables
        Should not loop
        """

    def getMotorPercents(self):
        """
        Returns a tuple containing left and right motor percents
        :return: (leftMotorPercent, rightMotorPercent)
        """
        return (self.leftMotorPercent, self.rightMotorPercent)