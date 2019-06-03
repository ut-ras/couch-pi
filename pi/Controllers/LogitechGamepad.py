#!/usr/bin/python

# pip install evdev
# cat /dev/input/event0

from Controllers.Controller import Controller
from evdev import InputDevice, categorize, ecodes, KeyEvent
from threading import Thread, Timer
from select import select
import pprint
import serial
import time

# See https://stackoverflow.com/questions/19203819/reading-joystick-values-with-python
# and https://theraspberryblonde.wordpress.com/2016/06/29/ps3-joystick-control-with-pygame/
# on how to use pygame to read joystick/gamepad inputs

# Device event library evdev
# https://python-evdev.readthedocs.io/en/latest/tutorial.html

# Current Controls:
# Stop: let go of joystick and hold down either B, Left Bumper, or Right Bumper
# Left side speed: Left Joystick Y-Axis
# Right side speed: Right Joystick Y-Axis
# Rainbow LED: A
# Orange LED: X
# E-STOP is on Couch base, push in large red button

class LogitechGamepad(Controller):
    joystickMax = 255

    # Stop buttons
    stopFast = False
    isDownLeftBump = False
    isDownRightBump = False
    isDownB = False

    # Other buttons - thread is created to trigger the event, booleans are toggled each button press
    toggleA = False
    toggleX = False
    btnAEvent = None
    btnXEvent = None

    def __init__(self,name="Logitech Gamepad", maxSpeed=100):
        super().__init__(name, maxSpeed)
        try:
            self.gamepad = InputDevice('/dev/input/event0')
            print(self.gamepad)
            print(pprint.pformat(self.gamepad.capabilities(verbose=True))) #get input options
            self.error = False
        except (FileNotFoundError, serial.SerialException):
            self.gamepad = None
            self.error = True
            print("ERROR Gamepad is not plugged in")            

    def getStatus(self):
        pass

    # Starts a thread for updateLoop, which reads continuously in a loop
    def startController(self):
        """
        Starts a thread that continuously reads gamepad and updates Controller variables
        """
        self.updateThread = Thread(target=self.updateLoop(), daemon=True)
        self.updateThread.start()

    # Read continuously in a loop, does not exit
    def updateLoop(self):
        if self.gamepad is not None:
            try:
                for event in self.gamepad.read_loop():
                    self.handleEvent(event)
            except Exception as e:
                self.error = True
                print(e)
        else:
            print("ERROR Gamepad is not plugged in")

    # Read the input buffer until empty, exit when done
    def readAndUpdate(self):
        if self.gamepad is not None:
            try:
                r,w,x = select([self.gamepad], [], [])
                for event in self.gamepad.read():
                    self.handleEvent(event)
            except Exception as e:
                self.error = True
                print(e)
        else:
            print("ERROR Gamepad is not plugged in")
       
    # Handle a Controller event, helper function for updateLoop and readAndUpdate
    def handleEvent(self, event):
        if event.type == ecodes.EV_KEY:
            keyevent = categorize(event)
            #print(keyevent.event)
            print("KEY | " + str(keyevent.keycode))

            #Buttons with KeyEvent
            if keyevent.keystate == KeyEvent.key_down:
                if keyevent.keycode == 'BTN_THUMB':
                    self.toggleA = not self.toggleA
                    if self.btnAEvent is not None:
                        Thread(target=self.btnAEvent, name='Btn A Thread', args=(self.toggleA,)).start()
                if keyevent.keycode[0] == 'BTN_JOYSTICK':
                    self.toggleX = not self.toggleX
                    if self.btnXEvent is not None:
                        Thread(target=self.btnXEvent, name='Btn X Thread', args=(self.toggleX,)).start()
                elif keyevent.keycode == 'BTN_THUMB2':
                    self.isDownB = True
                elif keyevent.keycode == 'BTN_BASE':
                    self.isDownLeftBump = True
                elif keyevent.keycode == 'BTN_BASE2':
                    self.isDownRightBump = True
                    
            if keyevent.keystate == KeyEvent.key_up:
                if keyevent.keycode == 'BTN_BASE':
                    self.isDownLeftBump = False
                elif keyevent.keycode == 'BTN_BASE2':
                    self.isDownRightBump = False
                elif keyevent.keycode == 'BTN_THUMB2':
                    self.isDownB = False

        elif event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            #print(absevent.event)
            print("ABS | " + str(absevent.event.code) + " " + str(absevent.event.value))

            # AbsEvent code values
            #ABS_Y / 1 / Left Y
            #ABS_X / 0 / Left X
            #ABS_RZ / 5 / Right Y
            #ABS_Z / 2 / Right X
            
            if self.stopFast:
                self.leftMotorPercent = 0
                self.rightMotorPercent = 0
            else:
                if absevent.event.code == ecodes.ABS_Y:
                    #Left Y
                    self.leftMotorPercent = (self.maxSpeed - (2 * self.maxSpeed * absevent.event.value / self.joystickMax))
                elif absevent.event.code == ecodes.ABS_RZ:
                    #Right Y
                    self.rightMotorPercent = (self.maxSpeed - (2 * self.maxSpeed * absevent.event.value / self.joystickMax))

        # Stop Buttons
        if self.isDownLeftBump or self.isDownRightBump or self.isDownB:
            self.leftMotorPercent = 0
            self.rightMotorPercent = 0
            self.stopFast = True
        else:
            self.stopFast = False