

class Controller:
    """
    Parent class/Interface for all controller classes
    """
    def __init__(self,name="Generic Controller"):
        # name of Controller
        self.name = name

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
