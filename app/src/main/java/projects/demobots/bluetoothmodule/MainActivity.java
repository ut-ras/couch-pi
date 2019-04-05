package projects.demobots.bluetoothmodule;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanFilter;
import android.bluetooth.le.ScanResult;
import android.bluetooth.le.ScanSettings;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.SeekBar;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
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

    private BluetoothSender bluetoothSender;

    TextView forwardText;
    TextView speedText;

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

        forwardText = findViewById(R.id.textView);
        speedText = findViewById(R.id.textView2);

        setupForwardButton();
        setupSpeedSlider();

        bluetoothSender = new BluetoothSender();

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
                outputToPi.print("Hello");
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
                                    //UUID MY_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
                                    //connect to insecure socket
                                    Method m = device.getClass().getMethod("createInsecureRfcommSocket", new Class[] {int.class});
                                    BluetoothSocket socket = (BluetoothSocket) m.invoke(device, 1);
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
                                } catch (IOException | NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
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

    @SuppressLint("ClickableViewAccessibility")
    private void setupForwardButton() {
        final ImageButton forwardButton = findViewById(R.id.imageButton5);
        forwardButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    forwardText.setText("Forward On");
                    //bluetoothSender.execute("forward");
                    outputToPi.print("Forward On");
                    outputToPi.flush();
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    forwardText.setText("Forward Off");
                    //bluetoothSender.execute("stop");
                    outputToPi.print("Forward Off");
                    outputToPi.flush();
                }
                return true;
            }
        });
    }

    private void setupSpeedSlider() {
        final SeekBar speedSlider = findViewById(R.id.seekBar);
        speedSlider.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                speedText.setText(String.valueOf(progress));
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });
    }

    //TODO: remove, no use for this class anymore
    @SuppressLint("StaticFieldLeak")
    private class BluetoothSender extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... strings) {
            return strings[0];
        }

        @Override
        protected void onPostExecute(String string) {
            outputToPi.print(string);
            outputToPi.flush();
        }
    }
}
