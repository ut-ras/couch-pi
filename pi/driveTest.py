from Sabertooth import Sabertooth
from CommandLineController import CommandLineController
from time import sleep
from Couches.testBenchCouch import testBenchCouch
"""
mC = Sabertooth('/dev/ttyS0')
mC.drive(1,80)
"""
controller = CommandLineController()
couch = testBenchCouch(controller)
while 1:
    couch.readControllerUpdateMotors()
    print(couch.drivetrain.getMotorVals())
    print("-----------")
    sleep(0.2)