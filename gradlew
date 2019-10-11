package projects.software_lab.hw1_461L_F19morning;

import androidx.appcompat.app.AppCompatActivity;

import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //ApiCall darkSkyCall = new ApiCall();
        //darkSkyCall.execute("https://api.darksky.net/forecast/5f98e132cb610d3537b7d3ae61556a96/29.6197,-95.6349");

        ApiCall googleCall = new ApiCall();
        googleCall.execute("https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyDzMnRXnEM07R6xemvNrPIscUCE6Vuo2Qc");
    }

    //Arthur driving
    private class ApiCall extends AsyncTask<String, Void, JSONObject> {

        @Override
        protected JSONObject doInBackground(String... strings) {
            String url = strings[0];

            URL urlObj;
            HttpURLConnection con;

            try {
                urlObj = new URL(url);
                con = (HttpURLConnection) urlObj.openConnection();

                con.setRequestMethod("GET");
                con.setRequestProperty("User-Agent", "Mozilla/5.0");

                BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                StringBuilder response = new StringBuilder();

                while ((inputLine = br.readLine()) != null)
                    response.append(inputLine);
                br.close();

                return new JSONObject(response.toString());

            } catch (Exception e) {
                e.printStackTrace();
            }

            return null;
        }

        @Override
        protected void onPostExecute(JSONObject jsonObject) {
            TextView textView = findViewById(R.id.placeholder);
            try {
                //textView.setText(jsonObject.get("latitude").toString());
                JSONArray myArray = jsonObject.getJSONArray("results");
                JSONObject myObject = myArray.getJSONObject(0);
                textView.setText(jsonObject.get("").toString());
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             