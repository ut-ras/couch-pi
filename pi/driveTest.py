# Test main functions for the couch
# To run:
# sudo apt-get install python3-pip
# sudo pip3 install -r requirements.txt
# sudo python3 driveTest.py

# To python fie in background at startup with log files:
# sudo vim /etc/rc.local
#       sudo python3 /home/pi/couch-pi/pi/driveTest.py > /home/pi/couch-pi/pi/logs/log.$(date "+%Y.%m.%d-%H.%M.%S").txt 2>&1 &
#       exit 0

# Enable UART
# add "enable_uart=1" to /boot/config.txt

from Sabertooth import Sabertooth
from time import sleep
import sys
import RPi.GPIO as GPIO

from Couches.testBenchCouch import testBenchCouch
#from CommandLineController import CommandLineController
from bluetoothController import BluetoothControl
from Controllers.LogitechGamepad import LogitechGamepad
from Drivetrains.OneControllerDrivetrain import OneControllerDrivetrain


def driveTestGamepad():
    ledInit(17)
    #ledInit(27)
    #ledInit(22)
    ledOut(17, True)

    controller = LogitechGamepad(maxSpeed = 30)         # maxSpeed [0, 100]
    couch = testBenchCouch(controller)

    if couch.drivetrain.error or controller.error:
        sys.exit()
        
    couch.startDrivetrainControl()
    while True:
        ledOut(17, True)
        sleep(1)
        ledOut(17, False)
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



def ledInit(pin):    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

def ledOut(pin, output):
    GPIO.output(pin, output)



#driveTestSabertooth()
#driveTestBluetooth()
driveTestGamepad()
