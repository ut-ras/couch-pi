from Sabertooth import Sabertooth
from CommandLineController import CommandLineController
from time import sleep
from Couches.testBenchCouch import testBenchCouch
from bluetoothController import BluetoothControl
"""
mC = Sabertooth('/dev/ttyS0')
mC.drive(1,80)
"""
controller = BluetoothControl()
couch = testBenchCouch(controller)
while 1:
    couch.readBluetoothUpdateMotors()
    #print(couch.drivetrain.getMotorVals())
    print("-----------")
    sleep(0.2)