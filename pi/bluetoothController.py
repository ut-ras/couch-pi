from Controllers.Controller import Controller
import bluetooth
from ast import literal_eval
from Drivetrains.TankDrivetrain import TankDrivetrain


class BluetoothControl(Controller):
    def __init__(self,name="Bluetooth Controller", motorPowerPercent = 0):
        super().__init__(name)
        self.motorPowerPercent = motorPowerPercent
        self.updateThread = None
        self.drivetrain = TankDrivetrain('/dev/ttyS0')
        

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
        returns data type of received data
        """
        try:
            return type(literal_eval(input_data))
        except (ValueError, SyntaxError):
            # A string, so return str
            return str
    
    def handleRightOn(self):
        #do stuff
        self.drivetrain.drive(self.motorPowerPercent, -self.motorPowerPercent)
        print("right on handled")
        return
    
    def handleRightOff(self):
        #do stuff
        self.drivetrain.drive(0, 0)
        print("right off handled")
        return
    
    def handleLeftOn(self):
        #do stuff
        self.drivetrain.drive(self.motorPowerPercent, -self.motorPowerPercent)
        print("left on handled")
        return
    
    def handleLeftOff(self):
        #do stuff
        self.drivetrain.drive(0, 0)
        print("left off handled")
        return
     
    def handleForwardOn(self):
        #do stuff
        self.drivetrain.drive(self.motorPowerPercent, self.motorPowerPercent)
        print("forward on handled")
        return
    
    def handleForwardOff(self):
        #do stuff
        self.drivetrain.drive(0, 0)
        print("forward off handled")
        return
    
    def handleBackwardOn(self):
        #do stuff
        self.drivetrain.drive(-self.motorPowerPercent, -self.motorPowerPercent)
        print("backward on handled")
        return
    
    def handleBackwardOff(self):
        #do stuff
        self.drivetrain.drive(0, 0)
        print("backward off handled")
        return
    
    def handleStop(self):
        #do stuff
        self.drivetrain.drive(0, 0)
        print("stop handled")
        return
    
    def handleSpeed(self,speed):
        self.motorPowerPercent = speed
        print("speed changed to %d", speed)
        return
    
    def handleTest(self):
        print("testing")
        return
    
    handler = {
            #all data has letter "b" before string and '' around sent string 
            "Stop": handleStop,
            "Forward On": handleForwardOn,
            "Forward Off": handleForwardOff,
            "Left On": handleLeftOn,
            "Left Off": handleLeftOff,
            "Right On": handleRightOn,
            "Right Off": handleRightOff,
            "Backward On": handleBackwardOn,
            "Backward Off": handleBackwardOff
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
    
    def receiveAndHandleMessages(self):
      
      while(1): 
          data = self.client_sock.recv(1024)
          print ("received [%s]" % data)
          self.handle_input(data)
    
      self.client_sock.close()
      self.server_sock.close()
      


    def readAndUpdate(self):
        data = self.client_sock.recv(1024)
        print ("received [%s]" % data)
        self.handle_input(data)

