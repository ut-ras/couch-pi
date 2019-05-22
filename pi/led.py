import RPi.GPIO as GPIO
import board
import neopixel
import time

#https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage

ledGreen = 17
ledBlue = 27
ledRed = 22

pixels = None
num_pixels = 300
ORDER = neopixel.GRB


# DEBUG LEDS

def ledInit(pin):  
    global pixels  
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

def ledOut(pin, output):
    GPIO.output(pin, output)


# NEOPIXEL LED STRIP

def ledStripInit():
    global pixels
    pixels = neopixel.NeoPixel(board.D18, num_pixels, pixel_order=ORDER)

def ledStripFill(colors):
    global pixels
    pixels.fill(colors)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)
 
 
def rainbow_cycle(wait):
    global pixels
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)
 
