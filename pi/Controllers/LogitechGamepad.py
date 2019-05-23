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

class LogitechGamepad(Controller):
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
        finally:
            self.joystickMax = 255
            self.leftMotorSetpoint = 0          #percent
            self.rightMotorSetpoint = 0         #percent
            self.stopDecelerationTime = 0.4     #seconds - for stop, decelerate from maxSpeed to 0 in this amount of time
            self.acceleration = 30              #percent per second - general acceleration/deceleration
            self.accelerationUpdateTime = 0.1   #seconds
            self.toggleA = False
            self.btnAEvent = None
            Timer(self.accelerationUpdateTime, self.accelerationTimer).start()
            

    def getStatus(self):
        pass

    def accelerationTimer(self):
        startT = time.time()
        leftDiff = self.leftMotorSetpoint - self.leftMotorPercent
        rightDiff = self.rightMotorSetpoint - self.rightMotorPercent
        leftInc = 0
        rightInc = 0

        if abs(self.leftMotorSetpoint) < 3:
            leftInc = self.maxSpeed / (self.stopDecelerationTime / self.accelerationUpdateTime)  
        else:
            leftInc = self.acceleration * self.accelerationUpdateTime 
            
        if abs(self.rightMotorSetpoint) < 3:
            rightInc = self.maxSpeed / (self.stopDecelerationTime / self.accelerationUpdateTime)          
        else:
            rightInc = self.acceleration * self.accelerationUpdateTime   
            
        self.leftMotorPercent += min(leftInc, abs(leftDiff)) * (1 if leftDiff > 0 else -1)  
        self.rightMotorPercent += min(rightInc, abs(rightDiff)) * (1 if rightDiff > 0 else -1)  
        waitT = self.accelerationUpdateTime - (time.time() - startT)
        #print("Wait: " + str(waitT))
        Timer(waitT, self.accelerationTimer).start()

    def startController(self):
        """
        Starts a thread that continuously reads gamepad and updates Controller variables
        """
        self.updateThread = Thread(target=self.updateLoop(), daemon=True)
        self.updateThread.start()

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

    def readAndUpdate(self):
        if self.gamepad is not None:
            r,w,x = select([self.gamepad], [], [])
            for event in self.gamepad.read():
                self.handleEvent(event)
        else:
            print("ERROR Gamepad is not plugged in")

    def handleEvent(self, event):
        if event.type == ecodes.EV_KEY:
            keyevent = categorize(event)
            print(keyevent.event)
            print(keyevent.keycode)

            #Buttons with KeyEvent
            if keyevent.keystate == KeyEvent.key_down:
                if keyevent.keycode == 'BTN_THUMB':
                    self.toggleA = not self.toggleA
                    if self.btnAEvent is not None:
                        Thread(target=self.btnAEvent, name='Btn A Thread', args=(self.toggleA,)).start()
            
        elif event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            print(absevent.event)
            print(absevent.event.value)

            # AbsEvent code values
            #ABS_Y / 1 / Left Y
            #ABS_X / 0 / Left X
            #ABS_RZ / 5 / Right Y
            #ABS_Z / 2 / Right X

            if absevent.event.code == ecodes.ABS_Y:
                #Left Y
                #self.leftMotorPercent = (self.maxSpeed - (2 * self.maxSpeed * absevent.event.value / self.joystickMax))
                self.leftMotorSetpoint = (self.maxSpeed - (2 * self.maxSpeed * absevent.event.value / self.joystickMax))
            elif absevent.event.code == ecodes.ABS_RZ:
                #Right Y
                #self.rightMotorPercent = (self.maxSpeed - (2 * self.maxSpeed * absevent.event.value / self.joystickMax))
                self.rightMotorSetpoint = (self.maxSpeed - (2 * self.maxSpeed * absevent.event.value / self.joystickMax))
                
