package projects.demobots.bluetoothmodule;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanFilter;
import android.bluetooth.le.ScanResult;
import android.bluetooth.le.ScanSettings;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.NetworkInterface;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.UUID;


public class MainActivity extends AppCompatActivity {
    private static BluetoothLeScanner sBleScanner;
    private static ScanCallback sScanCallback;
    private PrintWriter outputToPi;
    private BluetoothAdapter bluetoothAdapter;
    private InputStreamReader input;

    String t = "connected";

    //currently MAC_adr = Takuma's Laptop
    String MAC_adr = "B8:27:EB:2D:0F:98"; //TODO: change to raspberry pi MAC adr.

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    public static void searchBleDeviceByNames(final ScanCallback callback, String[] deviceNames) {
        //Log.e(TAG, "Searching for BLE device...");

        List<ScanFilter> filterList = new ArrayList<>();
        for (String name : deviceNames) {
            filterList.add(new ScanFilter.Builder().setDeviceName(name).build());
        }

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            if (sBleScanner == null) {
                sBleScanner = BluetoothAdapter.getDefaultAdapter().getBluetoothLeScanner();
            }
            if (sScanCallback == null) {
                sScanCallback = new ScanCallback(){
                    @Override
                    public void onScanResult(int callbackType, ScanResult result){
                        super.onScanResult(callbackType, result);
                    }
                };
            }

            if (sBleScanner != null) {
                sBleScanner.startScan(filterList, new ScanSettings.Builder().build(), sScanCallback);
            }
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        configureButton();
    }


    //creates button that tries to connect to desired device
    private void configureButton() {
        Button connectButton = findViewById(R.id.button);

        Button sendString =  findViewById(R.id.sendString);

        sendString.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                TextView textView = findViewById(R.id.status);
                textView.setText("tried to send stuff");
                outputToPi.print("E");
                outputToPi.flush();
            }
        });

        TextView myMac = findViewById(R.id.myMacAdd);
        try {
            myMac.setText("My MAC address: " + NetworkInterface.getNetworkInterfaces().toString());
        } catch (Exception e){
            myMac.setText("couldn't get my mac");
        }

        connectButton.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
            @Override
            public void onClick(View view) {
                BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
                System.out.println(bluetoothAdapter.isEnabled());
                if (bluetoothAdapter.isEnabled()) {
                    //get list of all paired devices
                    Set<BluetoothDevice> bondedDevices = bluetoothAdapter.getBondedDevices();
                    BluetoothLeScanner myScanner = bluetoothAdapter.getBluetoothLeScanner();
                    ScanCallback myCallback = new ScanCallback(){
                        @Override
                        public void onScanResult(int callbackType, ScanResult result){
                            super.onScanResult(callbackType, result);
                        }
                    };
                    String[] deviceNames = {"raspberrypi"};
                    searchBleDeviceByNames(myCallback, deviceNames);

                    TextView textView = findViewById(R.id.status);

                    if (bondedDevices.size() > 0) {
                        textView.setText("Number of devices: " + bondedDevices.size());
                        for (BluetoothDevice device : bondedDevices) {
                            //find correct MAC address for desired device
                            textView.append("\n" + "name = " + device.getName() + "address = " + device.getAddress());
                            if (device.getAddress().equals(MAC_adr)) {

                                try {
                                    //use this UUID instead of any dynamically generated one
                                    UUID MY_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
                                    //connect to insecure socket
                                    BluetoothSocket socket = device.createInsecureRfcommSocketToServiceRecord(MY_UUID);
                                    textView.setText("createInsecureRfcommSocketToServiceRecord\n");
                                    //attempt to connect to socket
                                    bluetoothAdapter.cancelDiscovery();
                                    socket.connect();
                                    //set out/inputSteam if socket connection successful
                                    textView.append("connect\n");
                                    outputToPi = new PrintWriter(socket.getOutputStream());
                                    textView.append("PrintWriter\n");
                                    input = new InputStreamReader(socket.getInputStream());
                                    textView.append("InputStreamReader\n");
                                } catch (IOException e) {
                                    //could not connect to socket
                                    textView.append(e.getMessage());
                                }
                                break;
                            }
                        }
                    }
                }
            }
        });
    }
}
