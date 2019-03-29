from Sabertooth import Sabertooth


# https://github.com/MomsFriendlyRobotCompany/pysabertooth


class TankDrivetrain(object):

    def __init__(self, port, baudrate=9600, address=128, timeout=0.1):
        Sabertooth.createSerial(port,baudrate,timeout)
        Sabertooth.open()
        self.sabertoothL = Sabertooth(address=128)
        self.sabertoothR = Sabertooth(address=129)
        self.sabertoothL.setBaudrate(baudrate)
        self.sabertoothR.setBaudrate(baudrate)

    def drive(self,speedL, speedR):
        self.sabertoothL.driveBoth(speedL)
        self.sabertoothR.driveBoth(speedR)

