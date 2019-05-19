import RPi.GPIO as GPIO

ledGreen = 17
ledBlue = 27
ledRed = 22

def ledInit(pin):    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

def ledOut(pin, output):
    GPIO.output(pin, output)


