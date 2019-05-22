import RPi.GPIO as GPIO
import board
import neopixel

ledGreen = 17
ledBlue = 27
ledRed = 22

pixels = None
numPixels = 300
ORDER = neopixel.GRB

def ledInit(pin):  
    global pixels  
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

def ledOut(pin, output):
    GPIO.output(pin, output)


def ledStripInit():
    global pixels
    pixels = neopixel.NeoPixel(board.D18, numPixels, pixel_order=ORDER)

def ledStripFill(colors):
    global pixels
    pixels.fill(colors)
