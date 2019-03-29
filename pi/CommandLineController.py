from Controllers.Controller import Controller
import readchar


class CommandLineController(Controller):
    def __init__(self,name="Command Line Controller", motorPowerPercent = 80):
        super().__init__(name)
        self.motorPowerPercent = motorPowerPercent
        self.updateThread = None

    def initialize(self):
        print("Starting Command Line Couch Controller...")
        print("Use WASD to control the motors")
        print("Press the spacebar to stop")
        print("----------------------------")

    def readAndUpdate(self):
        charIn = readchar.readchar()  # Will return b'[char] e.g: b'a' for a
        if charIn == b'w' or charIn == b'W':
            self.leftMotorPercent = self.motorPowerPercent
            self.rightMotorPercent = self.motorPowerPercent
        elif charIn == b's' or charIn == b'S':
            # left Motor backwards
            self.leftMotorPercent = -self.motorPowerPercent
            self.rightMotorPercent = -self.motorPowerPercent
        elif charIn == b'a' or charIn == b'A':
            self.leftMotorPercent = -self.motorPowerPercent
            self.rightMotorPercent = self.motorPowerPercent
        elif charIn == b'd' or charIn == b'D':
            self.leftMotorPercent = self.motorPowerPercent
            self.rightMotorPercent = -self.motorPowerPercent
        else:
            self.leftMotorPercent = 0
            self.rightMotorPercent = 0

        if charIn == b' ':
            # space stops the motors
            self.rightMotorPercent = 0
            self.leftMotorPercent = 0

