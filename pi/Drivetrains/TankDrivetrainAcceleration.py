from Drivers.Sabertooth import Sabertooth
import serial
from threading import Thread, Timer
import time

# https://github.com/MomsFriendlyRobotCompany/pysabertooth

# Wiring
# Connect Pi GPIO14 / UART_TX -> Sabertooth S1 pin on both drivers
# Connect Pi Gnd -> Sabertooth Gnd (the one near S1) on both drivers

class TankDrivetrainAcceleration(object):
    leftMotorPercent = 0
    rightMotorPercent = 0
    leftMotorSetpoint = 0
    rightMotorSetpoint = 0

    stopDeceleration = 120          #percent per second - fast stop acceleration/deceleration
    stopThresh = 6                  #trigger fast stop when both setpoints under this value
    
    acceleration = 20               #percent per second - general acceleration/deceleration

    def __init__(self, port, baudrate=9600, timeout=0, accelerationUpdateTime=0.05):
        try:
            Sabertooth.createSerial(port,baudrate,timeout)
            Sabertooth.open()
            self.sabertoothL = Sabertooth(address=128)
            self.sabertoothR = Sabertooth(address=129)
            self.sabertoothL.setBaudrate(baudrate)
            self.sabertoothR.setBaudrate(baudrate)
            self.error = False

            #Timer(self.accelerationUpdateTime, self.accelerationTimer).start()     # add this if using accelerationTimer
        except (FileNotFoundError, serial.SerialException, Exception):
            print("ERROR Sabertooth Driver could not find UART /dev/ttyS0")
            self.sabertoothL = None
            self.sabertoothR = None
            self.error = True

        self.accelerationUpdateTime = accelerationUpdateTime

    def setSpeed(self, speed):
        self.leftMotorSetpoint = speed[0]
        self.rightMotorSetpoint = speed[1]

    def getMotorPercents(self):
        return (self.leftMotorPercent, self.rightMotorPercent)
    
    def setSabertoothPercent(self, speed):
        """
        Sets the speed of the left and right sabertooth drivers (both motors on each)
        :param speed: tuple (speedL, speedR)
        :return: nothing
        """
        try:
            if self.sabertoothL is not None and self.sabertoothR is not None:
                #print("Drivetrain: L=" + str(speed[0]) + ", R=" + str(speed[1]))
                self.sabertoothL.driveBoth(speed[0], speed[0])
                self.sabertoothR.driveBoth(speed[1], speed[1])
            else:
                print("ERROR Sabertooth Driver not initialized")
        except Exception as e:
            print("ERROR Sabertooth Driver exception, check connection")
            print(e)

    def accelerationUpdate(self):
        leftDiff = self.leftMotorSetpoint - self.leftMotorPercent
        rightDiff = self.rightMotorSetpoint - self.rightMotorPercent

        leftInc = rightInc = 0
        if abs(self.leftMotorSetpoint) < self.stopThresh and abs(self.rightMotorSetpoint) < self.stopThresh:
            leftInc = self.stopDeceleration * self.accelerationUpdateTime 
            rightInc = self.stopDeceleration * self.accelerationUpdateTime           
        else:
            leftInc = self.acceleration * self.accelerationUpdateTime
            rightInc = self.acceleration * self.accelerationUpdateTime   
            
        self.leftMotorPercent += min(leftInc, abs(leftDiff)) * (1 if leftDiff > 0 else -1)  
        self.rightMotorPercent += min(rightInc, abs(rightDiff)) * (1 if rightDiff > 0 else -1)  

        # set motors
        #sbStartT = time.time()
        self.setSabertoothPercent((self.leftMotorPercent, self.rightMotorPercent))
        #sbT = time.time() - sbStartT        # the serial flush() command was taking >0.1 seconds, causing some bottleneck and delay, so I removed it from Sabertooth.py
        #print("serialTime: " + str(sbT))
        print("Motor Speeds: " + str(self.getMotorPercents()))
    
    # Background timer that gradually brings the MotorPercent values closer to the MotorSetpoint values
    # Initialize this with Timer(self.accelerationUpdateTime, self.accelerationTimer).start()
    # testBenchCouch currently calls accelerationUpdate in the updateMotors Timer when it changes the setpoint
    def accelerationTimer(self):
        startT = time.time()

        self.accelerationUpdate()

        #calculate sleep time and reset timer
        waitT = self.accelerationUpdateTime - abs(time.time() - startT)
        #print("Wait: " + str(waitT))
        Timer(waitT, self.accelerationTimer).start()