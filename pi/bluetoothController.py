from Controllers.Controller import Controller
import bluetooth
from ast import literal_eval
from Drivetrains.TankDrivetrain import TankDrivetrain


class BluetoothControl(Controller):
    """
    To use this class, 
    
    After creating a BluetoothControl instance,
    1. Call "initialize"
    2. Call "readAndUpdate"
    
    Then program will continuously wait for a device to connect
    and input commands using bluetooth
    """
    
    def __init__(self,name="Bluetooth Controller", motorPowerPercent = 50):
        super().__init__(name)
        self.motorPowerPercent = motorPowerPercent
        self.updateThread = None
        self.drivetrain = TankDrivetrain('/dev/ttyS0')
        self.isStopped = False
        

    def initialize(self):
        print("Starting Bluetooth Controller...")
        self.server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1
        self.server_sock.bind(("",port))
        self.server_sock.listen(1)
        print("Waiting for bluetooth connection . . .") 
        self.client_sock,self.address = self.server_sock.accept()
        print ("Accepted connection from " + str(self.address))
        
    def get_type(self,input_data):
        """
        returns data type of input_data
        """
        try:
            return type(literal_eval(input_data))
        except (ValueError, SyntaxError):
            # A string, so return str
            return str
    
    def handleRightOn(self):
        self.leftMotorPercent += self.motorPowerPercent/2
        self.rightMotorPercent -= self.motorPowerPercent/2
        if self.isStopped:
            return
        self.drivetrain.drive(self.leftMotorPercent, self.rightMotorPercent)
        print("right on handled")
        return
    
    def handleRightOff(self):
        self.leftMotorPercent -= self.motorPowerPercent/2
        self.rightMotorPercent += self.motorPowerPercent/2
        if self.isStopped:
            return
        self.drivetrain.drive(self.leftMotorPercent, self.rightMotorPercent)
        print("right off handled")
        return
    
    def handleLeftOn(self):
        self.leftMotorPercent -= self.motorPowerPercent/2
        self.rightMotorPercent += self.motorPowerPercent/2
        if self.isStopped:
            return
        self.drivetrain.drive(self.leftMotorPercent, self.rightMotorPercent)
        print("left on handled")
        return
    
    def handleLeftOff(self):
        self.leftMotorPercent += self.motorPowerPercent/2
        self.rightMotorPercent -= self.motorPowerPercent/2
        if self.isStopped:
            return
        self.drivetrain.drive(self.leftMotorPercent, self.rightMotorPercent)
        print("left off handled")
        return
     
    def handleForwardOn(self):
        self.leftMotorPercent += self.motorPowerPercent
        self.rightMotorPercent += self.motorPowerPercent
        if self.isStopped:
            return
        self.drivetrain.drive(self.leftMotorPercent, self.rightMotorPercent)
        print("forward on handled")
        return
    
    def handleForwardOff(self):
        self.leftMotorPercent -= self.motorPowerPercent
        self.rightMotorPercent -= self.motorPowerPercent
        if self.isStopped:
            return
        self.drivetrain.drive(self.leftMotorPercent, self.rightMotorPercent)
        print("forward off handled")
        return
    
    def handleBackwardOn(self):
        self.leftMotorPercent -= self.motorPowerPercent
        self.rightMotorPercent -= self.motorPowerPercent
        if self.isStopped:
            return
        self.drivetrain.drive(self.leftMotorPercent, self.rightMotorPercent)
        print("backward on handled")
        return
    
    def handleBackwardOff(self):
        self.leftMotorPercent += self.motorPowerPercent
        self.rightMotorPercent += self.motorPowerPercent
        if self.isStopped:
            return
        self.drivetrain.drive(self.leftMotorPercent, self.rightMotorPercent)
        print("backward off handled")
        return
    
    def handleStop(self):
        self.isStopped = True
        self.drivetrain.drive(0, 0)
        print("stop handled")
        return
    
    def handleStopOff(self):
        self.isStopped = False
        self.drivetrain.drive(self.leftMotorPercent, self.rightMotorPercent)
        print("stop released")
        return
    
    def handleSpeed(self,speed):
        #self.motorPowerPercent = speed
        print("speed changed to %d.....but speed change is not yet implemented.", speed)
        return
    
    handler = {
            "stop on": handleStop,
            "stop off": handleStopOff,
            "forward on": handleForwardOn,
            "forward off": handleForwardOff,
            "left on": handleLeftOn,
            "left off": handleLeftOff,
            "right on": handleRightOn,
            "right off": handleRightOff,
            "backward on": handleBackwardOn,
            "backward off": handleBackwardOff
    }
     
     
    def handle_input(self,argument):
        
        myType = self.get_type(argument)
        if(myType == type("1")):
            print(argument)
            # Get the function from handler dictionary
            func = self.handler.get(str(argument), "Invalid command")
        elif(myType == type(1)):
            self.handleSpeed(int(argument))
        elif(myType == type(1.0)):
            print("handled the following:")
            print(argument)
        else:
            print("handled the following:")
            print(argument)
        # Execute the function
        if(func == "Invalid command"):
            print("Invalid command")
            return
        return func()
    
    def readAndUpdate(self):
      """
      Reads controls from bluetooth and sets speed on motors.
      """
      while(1): 
          data = self.client_sock.recv(1024)
          print ("received [%s]" % data)
          self.handle_input(data)
    
      self.client_sock.close()
      self.server_sock.close()

