from Couches.Couch import Couch
from Drivetrains.OneControllerDrivetrain import OneControllerDrivetrain
from threading import Thread

class testBenchCouch(Couch):
    def __init__(self, controller):
        super().__init__()
        #self.setDrivetrain(OneControllerDrivetrain('/dev/ttyS0'))
        self.controller = controller
        self.controller.initialize()
        self.drivetrainThread = None

    def startDrivetrainControl(self):
        self.setDrivetrain(OneControllerDrivetrain('/dev/ttyS0'))
        self.drivetrainThread = Thread(target=self.readControllerUpdateMotors())
        self.drivetrainThread.start()
        
    def readControllerUpdateMotors(self):
        """
        Loop to run in a thread
        Not to be called from outside this class
        :return: none
        """
        while True:
            self.controller.readAndUpdate()
            self.drivetrain.setSpeed(self.controller.getMotorPercents())

    def startBluetoothDrivetrainControl(self):
        self.drivetrainThread = Thread(target=self.readBluetoothUpdateMotors())
        self.drivetrainThread.start()
        
    def readBluetoothUpdateMotors(self):
        """
        Loop to run in a thread
        Not to be called from outside this class
        :return: none
        """
        self.controller.readAndUpdate()
    
    