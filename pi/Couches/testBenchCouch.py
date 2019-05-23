from Couches.Couch import Couch
from Drivetrains.OneControllerDrivetrain import OneControllerDrivetrain
from Drivetrains.TankDrivetrain import TankDrivetrain
from threading import Thread, Timer
from Couches.Led import LedStrip

class testBenchCouch(Couch):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.initialize()
        self.drivetrainThread = None
        self.drivetrainUpdateTime = 0.01
        self.led = LedStrip()

        # One or two motor drivers
        #self.setDrivetrain(OneControllerDrivetrain('/dev/ttyS0'))       #one sabertooth (address 128)
        self.setDrivetrain(TankDrivetrain('/dev/ttyS0'))               #two sabertooth (address 128, 129)

    def startDrivetrainControl(self):
        # One Thread for reading controllers and updating motors
        #self.drivetrainThread = Thread(target=self.readControllerUpdateMotors(), daemon=True)
        #self.drivetrainThread.start()

        # Two Threads for reading controllers and updating motors
        # TODO issues with print statements from multiple threads, not sure if working
        #self.controller.startController()                              
        #self.drivetrainThread = Thread(target=self.updateMotors(), daemon=True)
        #self.drivetrainThread.start()

        # One thread, one periodic timer
        Timer(self.drivetrainUpdateTime, self.updateMotors).start()
        self.controller.startController() 

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
        Run in timer - updates motors
        Not to be called from outside this class
        :return: none
        """
        if self.controller.error:
            self.drivetrain.setSpeed((0, 0))
            print("Controller Error, stopping couch")
        else:
            motorSpeeds = self.controller.getMotorPercents()
            self.drivetrain.setSpeed(motorSpeeds) 
            print("Motor Speeds: " + str(motorSpeeds))
        
        Timer(self.drivetrainUpdateTime, self.updateMotors).start()

    def toggleLedStrip(self, toggleOn):
        if toggleOn:
            self.led.rainbow_cycle(0.01)
        else:
            self.led.fill((0,0,0))
            

