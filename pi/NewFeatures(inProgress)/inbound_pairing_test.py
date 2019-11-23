bashCommand = "bluetoothctl"
import subprocess
process = subprocess.Popen(['bluetoothctl'],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
process.stdin.write('discoverable on')
