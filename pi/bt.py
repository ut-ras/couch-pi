# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html

import bluetooth

def handleRight():
    #do stuff
    print("right handled")
    return
 
def handleLeft():
    #do stuff
    print("left handled")
    return
 
def handleForward():
    #do stuff
    print("forward handled")
    return

def handleBack():
    #do stuff
    print("back handled")
    return

def handleStop():
    #do stuff
    print("stop handled")
    return
 
handler = {
        #all data has letter "b" before string and '' around sent string 
        "'b'right": handleRight,
        "'b'left": handleLeft,
        "'b'forward": handleForward,
        "'b'back": handleBack,
        "'b'stop'": handleStop
}
 
 
def handle_input(argument):
    # Get the function from handler dictionary
    func = handler.get(argument, "nothing")
    # Execute the function
    return func()

def receiveMessages():
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
  port = 1
  server_sock.bind(("",port))
  server_sock.listen(1)
  
  client_sock,address = server_sock.accept()
  print ("Accepted connection from " + str(address))
  while(1): 
      data = client_sock.recv(1024)
      print ("received [%s]" % data)
      
      handle_input(str(data))
      
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
