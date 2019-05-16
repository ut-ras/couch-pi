# To run:
# pip3 install -r requirements.txt
# python3 driveTest.py

from Sabertooth import Sabertooth
from time import sleep

from Couches.testBenchCouch import testBenchCouch
from Couches.testBenchCouchGamepad import testBenchCouchGamepad

#from CommandLineController import CommandLineController
from bluetoothController import BluetoothControl
from Controllers.LogitechGamepad import LogitechGamepad

def driveTest3():
    controller = LogitechGamepad()
    couch = testBenchCouchGamepad(controller)
    couch.startDrivetrainControl()

    while True:
        sleep(1)

def driveTest1():
    controller = BluetoothControl()
    couch = testBenchCouch(controller)
    while 1:
        couch.startBluetoothDrivetrainControl()
        print(controller.getMotorPercents())
        print("-----------")
        sleep(0.2)


def driveTest2():
    mC = Sabertooth('/dev/ttyS0')
    mC.drive(1,80)



#driveTest1()
#driveTest2()
driveTest3()
