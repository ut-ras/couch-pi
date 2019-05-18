# Test main functions for the couch
# To run:
# sudo apt-get install python3-pip
# sudo pip3 install -r requirements.txt
# sudo python3 driveTest.py

# To run at startup
# sudo vim /etc/rc.local
#       sudo python3 /home/pi/couch-pi/pi/driveTest.py &
#       exit 0

from Sabertooth import Sabertooth
from time import sleep

from Couches.testBenchCouch import testBenchCouch
#from CommandLineController import CommandLineController
from bluetoothController import BluetoothControl
from Controllers.LogitechGamepad import LogitechGamepad
from Drivetrains.OneControllerDrivetrain import OneControllerDrivetrain


def driveTestGamepad():
    controller = LogitechGamepad(maxSpeed = 30)         # maxSpeed [0, 100]
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
    #mC = Sabertooth('/dev/ttyS0')
    #mC.drive(1,80)
    d = OneControllerDrivetrain('/dev/ttyS0')
    d.setSpeed((50, 50))
    while True:
        d.setSpeed((50, 50))
        sleep(1)


#driveTestSabertooth()
#driveTestBluetooth()
driveTestGamepad()
