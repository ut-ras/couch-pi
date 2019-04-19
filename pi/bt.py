# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html

import bluetooth
from ast import literal_eval


def get_type(input_data):
    """
    returns data type of received data
    """
    try:
        return type(literal_eval(input_data))
    except (ValueError, SyntaxError):
        # A string, so return str
        return str

def handleRightOn():
    #do stuff
    print("right on handled")
    return

def handleRightOff():
    #do stuff
    print("right off handled")
    return

def handleLeftOn():
    #do stuff
    print("left on handled")
    return

def handleLeftOff():
    #do stuff
    print("left off handled")
    return
 
def handleForwardOn():
    #do stuff
    print("forward on handled")
    return

def handleForwardOff():
    #do stuff
    print("forward off handled")
    return

def handleBackwardOn():
    #do stuff
    print("backward on handled")
    return

def handleBackwardOff():
    #do stuff
    print("backward off handled")
    return

def handleStop():
    #do stuff
    print("stop handled")
    return

def handleSpeed(speed):
    #do stuff
    print("speed changed to %d", speed)
    return

def handleTest():
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
 
 
def handle_input(argument):
    
    myType = get_type(argument)
    if(myType == type("1")):
        print(argument)
        # Get the function from handler dictionary
        func = handler.get(str(argument), "Invalid command")
    elif(myType == type(1)):
        handleSpeed(int(argument))
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

def receiveMessages():
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  port = 1
  server_sock.bind(("",port))
  server_sock.listen(1)
  print("Waiting for bluetooth connection . . .") 
  client_sock,address = server_sock.accept()
  print ("Accepted connection from " + str(address))
  while(1): 
      data = client_sock.recv(1024)
      print ("received [%s]" % data)
      handle_input(data)

  client_sock.close()
  server_sock.close()
  
def sendMessageTo(targetBluetoothMacAddress):
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send("hello!!")
  sock.close()
  
def lookUpNearbyBluetoothDevices():
  nearby_devices = bluetooth.discover_devices()
  for bdaddr in nearby_devices:
    print (str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")

def testSwitchStatement(argument):
    handle_input(str(argument))
    
    
#lookUpNearbyBluetoothDevices()
receiveMessages()
