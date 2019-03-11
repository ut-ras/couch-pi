

class Controller(object):
    """
    Parent class/Interface for all controller classes
    """
    def __init__(self,name="Generic Controller"):
        # name of Controller
        self.name = name
        self.leftMotorPercent = 0
        self.rightMotorPercent = 0

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