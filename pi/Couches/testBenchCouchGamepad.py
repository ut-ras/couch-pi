from Couches.Couch import Couch
from Drivetrains.OneControllerDrivetrain import OneControllerDrivetrain
from threading import Thread

class testBenchCouchGamepad(Couch):
    def __init__(self, controller):
        super().__init__()
        #self.setDrivetrain(OneControllerDrivetrain('/dev/ttyS0'))
        self.controller = controller
        self.controller.initialize()
        self.drivetrainThread = None

    def startDrivetrainControl(self):
        self.setDrivetrain(OneControllerDrivetrain('/dev/ttyS0'))
        #self.controller.startController()          #TODO issues with print statements from multiple threads
        self.drivetrainThread = Thread(target=self.readControllerUpdateMotors(), daemon=True)
        self.drivetrainThread.start()

    def readControllerUpdateMotors(self):
        """
        Loop to run in a thread
        Not to be called from outside this class
        :return: none
        """
        while True:
            self.controller.readAndUpdate()
            motorSpeeds = self.controller.getMotorPercents()
            print("Motor Speeds: " + str(motorSpeeds))
            self.drivetrain.setSpeed(motorSpeeds)
