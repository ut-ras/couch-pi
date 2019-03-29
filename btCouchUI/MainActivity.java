package projects.demobots.bluetoothcouchui;

import android.annotation.SuppressLint;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    TextView forwardText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        forwardText = findViewById(R.id.textView);
        setupForwardButton();
    }

    @SuppressLint("ClickableViewAccessibility")
    private void setupForwardButton() {
        final ImageButton forwardButton = findViewById(R.id.imageButton5);
        forwardButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN)
                    forwardText.setText("Forward On");
                else if (event.getAction() == MotionEvent.ACTION_UP)
                    forwardText.setText("Forward Off");
                return true;
            }
        });
    }
}
