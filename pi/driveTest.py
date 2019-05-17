# Test main functions for the couch
# To run:
# pip3 install -r requirements.txt
# python3 driveTest.py

from Sabertooth import Sabertooth
from time import sleep

from Couches.testBenchCouch import testBenchCouch
#from CommandLineController import CommandLineController
from bluetoothController import BluetoothControl
from Controllers.LogitechGamepad import LogitechGamepad


def driveTestGamepad():
    controller = LogitechGamepad(maxSpeed = 50)         # maxSpeed [0, 100]
    couch = testBenchCouch(controller)
    couch.startDrivetrainControl()
    while True:
        sleep(1)


def driveTestBluetooth():
    controller = BluetoothControl()
    couch = testBenchCouch(controller)
    couch.startDrivetrainControl()
    #while 1:
    #    couch.startBluetoothDrivetrainControl()
    #    print(controller.getMotorPercents())
    #    print("-----------")
    #    sleep(0.2)


def driveTestSabertooth():
    mC = Sabertooth('/dev/ttyS0')
    mC.drive(1,80)



#driveTestSabertooth()
#driveTestBluetooth()
driveTestGamepad()
