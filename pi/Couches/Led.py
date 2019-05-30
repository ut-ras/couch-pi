import RPi.GPIO as GPIO
import board
import neopixel
import time
from threading import Thread, Event
import colorsys

# Debug LEDS - for the main program
ledGreen = 17
ledBlue = 27
ledRed = 22

def ledInit(pin):  
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

def ledOut(pin, output):
    GPIO.output(pin, output)


# Wrapper for the NeoPixel object - for examples and custom functions
# https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
class LedStrip():
    pixels = None           # NeoPixel object
    pixelThread = None      # cycle thread
    pixelCycleSleep = 0.001
    num_pixels = 108        # number of LEDs on the strip        108 = 30 + 30 + 24 + 24
    ORDER = neopixel.GRB    # order of colors on the strip
    
    # Colors
    burntorange = (191, 30, 0)      #should be (191, 87, 0) but the green makes it look yellow
    burntorange_hue = 9 / 255
    rainbow_shift = 20

    # Modes:
    # 'R' = Rainbow, 'L' = Longhorn
    mode = 'R'                  

    # NEOPIXEL LED STRIP

    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, self.num_pixels, pixel_order=self.ORDER)
        self.on = Event()
        self.pixelThread = Thread(target=self.pixelCycle, name='NeoPixel', daemon=True)
        self.turnOff()
        self.pixelThread.start()


    def pixelCycle(self):
        count = 0
        try:
            while True:
                self.on.wait()
                for i in reversed(range(self.num_pixels)):
                    self.on.wait()
                    color = (0, 0, 0)
                    if self.mode == 'R':
                        # rainbow next pixel
                        color = self.rainbowCycle(i, count)
                    elif self.mode == 'L':
                        # longhorn next pixel
                        color = self.longhornCycle(i, count)
                    self.pixels[i] = color
                    time.sleep(self.pixelCycleSleep)
                    #print("Pixel: i=" + str(i) + ", cnt=" + str(count) + "color=" + str(color))
                self.pixels.show()
                count += 1
        except Exception as e:
            print(e)

    def turnOff(self):
        self.fill((0, 0, 0))
        self.brightness(0)
        self.on.clear()

    def turnOn(self):
        self.brightness(50)
        self.on.set()

    def setMode(self, mode):
        self.mode = mode

    # colors: tuple
    def fill(self, colors):
        self.pixels.fill(colors)

    # b: float [0, 1]
    def brightness(self, b):
        self.pixels.brightness = b

    #burnt orange
    def longhornCycle(self, i, c):
        # uses HSV and adjusts the saturation to rotate between orange and white
        # first half of strip length will go from while -> orange
        # second half of strip length will go from orange -> white
        # sat_range determines the range of saturation values [(1 - sat_range), 1]
        strip_len = 16
        sat_range = 0.2
        i = (i + c * (strip_len / 2))   #shift based on c
        sat = ((i % int(strip_len / 2)) / int(strip_len / 2)) * sat_range
        if (i % strip_len) >= int(strip_len / 2):
            sat += (1 - sat_range)
        else:
            sat = 1 - sat
        print(sat)
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(self.burntorange_hue, sat, 1))

    def longhornCycleStripes2(self, i , c):
        strip_len = self.num_pixels / 2
        if (i + c * int(0.5 * strip_len)) % strip_len > int(0.85 * strip_len):
            return (255, 255, 255)
        else:
            return self.burntorange

    def longhornCycleStripes(self, i, c):
        strip_len = 40
        if (i + c * int(0.5 * strip_len)) % strip_len > int(0.5 * strip_len):
            return (255, 255, 255)
        else:
            return self.burntorange

    def longhornCycleWorm(self, i, c):
        strip_len = 20
        if (i + c * strip_len) % self.num_pixels > self.num_pixels - strip_len:
            return (255, 255, 255)
        else:
            return self.burntorange

    def rainbowCycle(self, i, c):
        pixel_index = (i * 256 // self.num_pixels) + (c * self.rainbow_shift % 256)
        #print("pixel_index=" + str(pixel_index))
        return self.colorWheel(pixel_index & 255)
    
    def colorWheel(self, pos):
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
        return (r, g, b) if self.ORDER == neopixel.RGB or self.ORDER == neopixel.GRB else (r, g, b, 0)