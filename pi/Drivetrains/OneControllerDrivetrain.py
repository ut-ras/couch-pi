from Sabertooth import Sabertooth


# https://github.com/MomsFriendlyRobotCompany/pysabertooth


class OneControllerDrivetrain(object):

    def __init__(self, port, baudrate=9600, address=128, timeout=0.1):
        Sabertooth.createSerial(port,baudrate,timeout)
        Sabertooth.open()
        self.sabertooth = Sabertooth(address=128)
        self.sabertooth.setBaudrate(baudrate)

    def setSpeed(self,speed):
        """
        Sets the speed of the left and right motors
        :param speed: tuple (speedL, speedR)
        :return: nothing
        """
        self.sabertooth.driveBoth(speed[0], speed[1])
