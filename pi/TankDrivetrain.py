import Sabertooth

#https://github.com/MomsFriendlyRobotCompany/pysabertooth
class TankDrivetrain:
    def __init__(self, left_sabertooth_port, right_sabertooth_port):
        sabertoothL = Sabertooth(left_sabertooth_port)

