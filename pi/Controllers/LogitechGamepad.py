from Controllers.Controller import Controller


# See https://stackoverflow.com/questions/19203819/reading-joystick-values-with-python
# and https://theraspberryblonde.wordpress.com/2016/06/29/ps3-joystick-control-with-pygame/
# on how to use pygame to read joystick/gamepad inputs

class LogitechGamepad(Controller):
    def __init__(self,name="Logitech Gamepad"):
        Controller.__init__(name)

    def getStatus(self):
        pass

    def startController(self):
        """
        Starts a thread that continuously reads gamepad and updates Controller variables
        """
        pass
