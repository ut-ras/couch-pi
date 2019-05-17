from Sabertooth import Sabertooth


# https://github.com/MomsFriendlyRobotCompany/pysabertooth


class TankDrivetrain(object):

    def __init__(self, port, baudrate=9600, timeout=0.1):
        Sabertooth.createSerial(port,baudrate,timeout)
        Sabertooth.open()
        self.sabertoothL = Sabertooth(address=128)
        self.sabertoothR = Sabertooth(address=129)
        self.sabertoothL.setBaudrate(baudrate)
        self.sabertoothR.setBaudrate(baudrate)

    def drive(self, speed):
        """
        Sets the speed of the left and right sabertooth drivers (both motors on each)
        :param speed: tuple (speedL, speedR)
        :return: nothing
        """
        print("Drivetrain: L=" + str(speed[0]) + ", R=" + str(speed[1]))
        self.sabertoothL.driveBoth(speed[0], speed[0])
        self.sabertoothR.driveBoth(speed[1], speed[1])

