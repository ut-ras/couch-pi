from Controllers.Controller import Controller
import bluetooth
from ast import literal_eval
from Drivetrains.TankDrivetrain import TankDrivetrain
from threading import Thread


class BluetoothControl(Controller):
    """
    To use this class, 
    
    After creating a BluetoothControl instance,
    1. Call "initialize"
    2. Call "readAndUpdate"
    
    Then program will continuously wait for a device to connect
    and input commands using bluetooth
    """
    
    def __init__(self,name="Bluetooth Controller", motorPowerPercent = 30):
        super().__init__(name)
        self.error = False
        self.motorPowerPercent = motorPowerPercent
        self.updateThread = None
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
        self.leftMotorPercent = +self.motorPowerPercent
        self.rightMotorPercent = -self.motorPowerPercent
        print("right on handled")
        return
    
    def handleRightOff(self):
        self.leftMotorPercent = 0
        self.rightMotorPercent = 0
        print("right off handled")
        return
    
    def handleLeftOn(self):
        self.leftMotorPercent = -self.motorPowerPercent
        self.rightMotorPercent = +self.motorPowerPercent
        print("left on handled")
        return
    
    def handleLeftOff(self):
        self.leftMotorPercent = 0
        self.rightMotorPercent = 0
        print("left off handled")
        return
     
    def handleForwardOn(self):
        self.leftMotorPercent = self.motorPowerPercent
        self.rightMotorPercent = self.motorPowerPercent
        print("forward on handled")
        return
    
    def handleForwardOff(self):
        self.leftMotorPercent = 0
        self.rightMotorPercent = 0
        print("forward off handled")
        return
    
    def handleBackwardOn(self):
        self.leftMotorPercent -= self.motorPowerPercent
        self.rightMotorPercent -= self.motorPowerPercent
        print("backward on handled")
        return
    
    def handleBackwardOff(self):
        self.leftMotorPercent = 0
        self.rightMotorPercent = 0
        print("backward off handled")
        return
    
    def handleStop(self):
        self.isStopped = True
        self.leftMotorPercent = 0
        self.rightMotorPercent = 0
        print("stop handled")
        return
    
    def handleStopOff(self):
        print("stop released")
        return
    
    def handleSpeed(self,speed):
        #self.motorPowerPercent = speed
        print("speed changed to %d.....but speed change is not yet implemented.", speed)
        return
     
    def handle_input(self,argument):
        
        myType = self.get_type(argument)
        if(myType == type("1")):
            argument = str(argument)[2:-1]
            print(argument)
            # Get the function from handler dictionary
            #func = self.handler.get(str(argument), "Invalid command")
            if(argument == "stop on"):
                self.handleStop()
            elif(argument == "stop off"):
                self.handleStopOff()
            elif(argument == "forward on"):
                self.handleForwardOn()
            elif(argument == "forward off"):
                self.handleForwardOff()
            elif(argument == "left on"):
                self.handleLeftOn()
            elif(argument == "left off"):
                self.handleLeftOff()
            elif(argument == "right on"):
                self.handleRightOn()
            elif(argument == "right off"):
                self.handleRightOff()
            elif(argument == "backward on"):
                self.handleBackwardOn()
            elif(argument == "backward off"):
                self.handleBackwardOff()
            else:
                print("invalid command")
        elif(myType == type(1)):
            self.handleSpeed(int(argument))
        elif(myType == type(1.0)):
            print("handled the following:")
            print(argument)
        else:
            print("handled the following:")
            print(argument)
    
    def startController(self):
        """
        Starts a thread that continuously reads gamepad and updates Controller variables
        """
        self.updateThread = Thread(target=self.readAndUpdate(), daemon=True)
        self.updateThread.start()
    
    
    def readAndUpdate(self):
      """
      Reads controls from bluetooth and sets speed on motors.
      """
      while(1): 
          try:
              data = self.client_sock.recv(1024)
              print ("received [%s]" % data)
              self.handle_input(data)
          except:
              self.leftMotorPercent = 0
              self.rightMotorPercent = 0
    
      self.client_sock.close()
      self.server_sock.close()

