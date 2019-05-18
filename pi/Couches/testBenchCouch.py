from Couches.Couch import Couch
from Drivetrains.OneControllerDrivetrain import OneControllerDrivetrain
from Drivetrains.TankDrivetrain import TankDrivetrain
from threading import Thread

class testBenchCouch(Couch):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.initialize()
        self.drivetrainThread = None

        # One or two motor drivers
        #self.setDrivetrain(OneControllerDrivetrain('/dev/ttyS0'))       #one sabertooth (address 128)
        self.setDrivetrain(TankDrivetrain('/dev/ttyS0'))               #two sabertooth (address 128, 129)

    def startDrivetrainControl(self):
        # One Thread for reading controllers and updating motors
        self.drivetrainThread = Thread(target=self.readControllerUpdateMotors(), daemon=True)
        self.drivetrainThread.start()

        # Two Threads for reading controllers and updating motors
        # TODO issues with print statements from multiple threads
        #self.controller.startController()                              
        #self.drivetrainThread = Thread(target=self.updateMotors(), daemon=True)
        #self.drivetrainThread.start()

    
    #sets drivetrainThread to controller thread without any motor speed update      
    def startBluetoothDrivetrainControl(self):
        self.drivetrainThread = Thread(target=self.controller.readAndUpdate())
        self.drivetrainThread.start()

    def readControllerUpdateMotors(self):
        """
        Loop to run in a thread - updates controller and motors
        Not to be called from outside this class
        :return: none
        """
        while True:
            self.controller.readAndUpdate()
            motorSpeeds = self.controller.getMotorPercents()
            print("Motor Speeds: " + str(motorSpeeds))
            self.drivetrain.setSpeed(motorSpeeds)

    def updateMotors(self):
        """
        Loop to run in a thread - updates motors
        Not to be called from outside this class
        :return: none
        """
        while True:
            motorSpeeds = self.controller.getMotorPercents()
            print("Motor Speeds: " + str(motorSpeeds))
            self.drivetrain.setSpeed(motorSpeeds) 
