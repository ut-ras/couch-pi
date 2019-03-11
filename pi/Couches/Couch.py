class Couch:
    def __init__(self):
        self.drivetrain = None

    def setDrivetrain(self, drivetrain):
        self.drivetrain = drivetrain

    def startDrivetrainControl(self):
        """
        Starts a thread which continuously reads controller and sends commands to motors
        :return:
        """
        pass
