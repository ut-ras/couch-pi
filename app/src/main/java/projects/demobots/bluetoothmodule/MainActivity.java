package projects.demobots.bluetoothmodule;

import android.annotation.SuppressLint;
import android.annotation.TargetApi;
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


public class MainActivity extends AppCompatActivity {
    private static BluetoothLeScanner sBleScanner;
    private static ScanCallback sScanCallback;
    private PrintWriter outputToPi;
    private BluetoothAdapter bluetoothAdapter;
    private InputStreamReader input;

    View decorView;
    
    TextView speedText;

    String MAC_adr = "B8:27:EB:2D:0F:98";

    //TODO: change button [and overall elements] names to be less ambiguous

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

    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        decorView = getWindow().getDecorView();
        int uiOptions = View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);

        setContentView(R.layout.activity_main);

        speedText = findViewById(R.id.textView2);

        setupDirectionalButtons();

        configureButton();
    }

    @TargetApi(Build.VERSION_CODES.KITKAT)
    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN)
    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            decorView.setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
        }
    }


    //creates button that tries to connect to desired device
    private void configureButton() {
        Button connectButton = findViewById(R.id.connectButton);

        Button sendString =  findViewById(R.id.testSendButton);

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
                                    //connect to insecure socket
                                    Method m = device.getClass().getMethod("createInsecureRfcommSocket", new Class[] {int.class});
                                    BluetoothSocket socket = (BluetoothSocket) m.invoke(device, 1);
                                    textView.setText("connected\n");
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

    private enum directionalButtons {
        FORWARD (R.id.forwardButton, R.drawable.ic_arrowup_w, R.drawable.ic_arrowup_bl,
                R.id.textView, "forward"),
        RIGHT (R.id.rightButton, R.drawable.ic_arrowright_w, R.drawable.ic_arrowright_bl,
                R.id.textView3, "right"),
        BACKWARD (R.id.backButton, R.drawable.ic_arrowdown_w, R.drawable.ic_arrowdown_bl,
                R.id.textView4, "backward"),
        LEFT (R.id.leftButton, R.drawable.ic_arrowleft_w, R.drawable.ic_arrowleft_bl,
                R.id.textView5, "left"),
        STOP (R.id.stopButton, R.drawable.ic_stop, R.drawable.ic_stop_pressed,
                R.id.textView6, "stop");

        private final int buttonID;
        private final int baseID;
        private final int pressedID;
        private final int textViewID;
        private final String name;

        directionalButtons(int buttonID, int baseID, int pressedID, int textViewID, String name) {
            this.buttonID = buttonID;
            this.baseID = baseID;
            this.pressedID = pressedID;
            this.textViewID = textViewID;
            this.name = name;
        }
    }

    @SuppressLint("ClickableViewAccessibility")
    private void setupDirectionalButtons() {
        for (final directionalButtons button : directionalButtons.values()) {
            final ImageButton imageButton = findViewById(button.buttonID);
            final TextView textView = findViewById(button.textViewID);
            imageButton.setOnTouchListener(new View.OnTouchListener() {
                @Override
                public boolean onTouch(View v, MotionEvent event) {
                    if (event.getAction() == MotionEvent.ACTION_DOWN) {
                        textView.setText(button.name + " on");
                        imageButton.setImageResource(button.pressedID);
                        //bluetoothSender.execute("on");
                        if (outputToPi != null) {
                            outputToPi.print(button.name + " on");
                            outputToPi.flush();
                        }
                    } else if (event.getAction() == MotionEvent.ACTION_UP) {
                        textView.setText(button.name + " off");
                        imageButton.setImageResource(button.baseID);
                        //bluetoothSender.execute("stop");
                        if (outputToPi != null) {
                            outputToPi.print(button.name + " off");
                            outputToPi.flush();
                        }
                    }
                    return true;
                }
            });
        }
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
}
