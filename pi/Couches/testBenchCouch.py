from Couches.Couch import Couch
from Drivetrains.OneControllerDrivetrain import OneControllerDrivetrain
from Drivetrains.TankDrivetrain import TankDrivetrain
from Drivetrains.TankDrivetrainAcceleration import TankDrivetrainAcceleration
from threading import Thread, Timer
from Drivers.Led import LedStrip
import Drivers.Led as Led

import sys
import time

class testBenchCouch(Couch):
    drivetrainThread = None
    drivetrainUpdateTime = 0.02
    lastT = 0

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.initialize()
        self.led = LedStrip()

        # One or two motor drivers
        #self.setDrivetrain(OneControllerDrivetrain('/dev/ttyS0'))       #one sabertooth (address 128)
        self.setDrivetrain(TankDrivetrainAcceleration('/dev/ttyS0', accelerationUpdateTime=self.drivetrainUpdateTime))               #two sabertooth (address 128, 129)

    def startDrivetrainControl(self, controller_thread=True):
        # One Thread for reading controllers and updating motors
        #self.drivetrainThread = Thread(target=self.readControllerUpdateMotors(), daemon=True)
        #self.drivetrainThread.start()

        # One thread, one periodic timer
        Timer(self.drivetrainUpdateTime, self.updateMotors).start()

        if controller_thread:
            self.controller.startController() 
        else:
            self.controller.updateLoop()

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
        startT = time.time()

        if self.controller.error:
            self.drivetrain.setSabertoothPercent((0, 0))
            Led.ledOut(Led.ledRed, True)
            Led.ledOut(Led.ledGreen, False)
            print("Controller Error, stopping couch")
            self.led.turnOff()
            sys.exit()
        else:
            motorSpeeds = self.controller.getMotorPercents()
            self.drivetrain.setSpeed(motorSpeeds) 
            self.drivetrain.accelerationUpdate()               # remove this if using accelerationTimer in TankDriveAcceleration
            print("Controller Speeds: " + str(motorSpeeds))
        
        diffT = time.time() - startT
        waitT = self.drivetrainUpdateTime - diffT
        errorT = self.drivetrainUpdateTime - (startT - self.lastT)
        self.lastT = startT
        #print("Wait: " + str(waitT) + ", Diff: " + str(diffT) + ", errorT: " + str(errorT))
        Timer(waitT, self.updateMotors).start()

    def toggleLedStrip(self, toggleOn):
        if toggleOn:
            self.led.turnOn()
            self.led.setMode('R')
        else:
            self.led.turnOff()
            
    def toggleLedOrange(self, toggleOn):
        if toggleOn:
            self.led.turnOn()
            self.led.setMode('L')
        else:
            self.led.turnOff()

