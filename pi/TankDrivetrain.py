from Sabertooth import Sabertooth
from LogitechGamepad import LogitechGamepad

#https://github.com/MomsFriendlyRobotCompany/pysabertooth
class TankDrivetrain:
    def __init__(self, left_sabertooth_port, right_sabertooth_port, wired_controller, bluetooth_controller=None):
        sabertoothL = Sabertooth(left_sabertooth_port)
        sabertoothR = Sabertooth(right_sabertooth_port)
        wired_controller = LogitechGamepad("Wired Gamepad")



