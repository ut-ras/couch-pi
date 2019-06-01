from Drivers.Sabertooth import Sabertooth
import serial

# https://github.com/MomsFriendlyRobotCompany/pysabertooth

# Wiring
# Connect Pi GPIO14 / UART_TX -> Sabertooth S1 pin on both drivers
# Connect Pi Gnd -> Sabertooth Gnd (the one near S1) on both drivers

class TankDrivetrain(object):

    def __init__(self, port, baudrate=9600, timeout=0.1):
        try:
            Sabertooth.createSerial(port,baudrate,timeout)
            Sabertooth.open()
            self.sabertoothL = Sabertooth(address=128)
            self.sabertoothR = Sabertooth(address=129)
            self.sabertoothL.setBaudrate(baudrate)
            self.sabertoothR.setBaudrate(baudrate)
            self.error = False
        except (FileNotFoundError, serial.SerialException):
            print("ERROR Sabertooth Driver could not find UART /dev/ttyS0")
            self.sabertoothL = None
            self.sabertoothR = None
            self.error = True

    def setSpeed(self, speed):
        """
        Sets the speed of the left and right sabertooth drivers (both motors on each)
        :param speed: tuple (speedL, speedR)
        :return: nothing
        """
        if self.sabertoothL is not None and self.sabertoothR is not None:
            #print("Drivetrain: L=" + str(speed[0]) + ", R=" + str(speed[1]))
            self.sabertoothL.driveBoth(speed[0], speed[0])
            self.sabertoothR.driveBoth(speed[1], speed[1])
        else:
            print("ERROR Sabertooth Driver could not find UART /dev/ttyS0")

