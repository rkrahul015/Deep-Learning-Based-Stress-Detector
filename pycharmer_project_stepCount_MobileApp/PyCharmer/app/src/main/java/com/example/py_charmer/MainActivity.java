package com.example.py_charmer;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.content.pm.PackageManager;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity implements SensorEventListener {
    private TextView textViewStepCounter, textViewStepDetector, idRand;
    private SensorManager sensorManager;


    //URL where our data will be sent and collected
    public static final String url = "https://fastapi.surdebmalya11.repl.co/dummy_steps_count";

    private Button rstBtn;
    private Sensor mStepCounter, mStepDetector;
    private boolean isCounterSensorPresent, isDetectorSensorPresent;
    int stepCount = 0, stepDetect = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //For no taskbar
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getSupportActionBar().hide();
        setContentView(R.layout.activity_main);

        idRand = findViewById(R.id.idRand);

        //Permission for Walking Data collection
        //Walking Data
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.ACTIVITY_RECOGNITION) == PackageManager.PERMISSION_DENIED) { //ask for permission
            requestPermissions(new String[]{android.Manifest.permission.ACTIVITY_RECOGNITION}, 0);
        }
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        //Attaching the components with the variables
        textViewStepCounter = findViewById(R.id.textViewStepCounter);
        textViewStepDetector = findViewById(R.id.textViewStepDetector);
        rstBtn = findViewById(R.id.rstBtn);

        //For Sensors
        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);

        //Reading of the Walking Data
        if (sensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER) != null) {
            mStepCounter = sensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER);
            isCounterSensorPresent = true;
        } else {
            textViewStepCounter.setText("Counter Sensor is not Present");
            isCounterSensorPresent = false;
        }

        //For More Accurate reading of the sensor
        if (sensorManager.getDefaultSensor(Sensor.TYPE_STEP_DETECTOR) != null) {
            mStepDetector = sensorManager.getDefaultSensor(Sensor.TYPE_STEP_DETECTOR);
            isDetectorSensorPresent = true;
        } else {
            textViewStepDetector.setText("Detector Sensor is not Present");
            isDetectorSensorPresent = false;
        }

        //All Actions after clicking the button....
        rstBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                 {
                     dataa();
                     new Handler().postDelayed(new Runnable() {
                         @Override
                         public void run() {
                             rstBtn.performClick();
                         }
                     }, 5000);
            }
            }
        });

    }
    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        if(sensorEvent.sensor == mStepCounter){
            stepCount =(int) sensorEvent.values[0];
            textViewStepCounter.setText(String.valueOf(stepCount));
        }else if(sensorEvent.sensor == mStepDetector){
            stepDetect =(int) (stepDetect+sensorEvent.values[0]);
            textViewStepDetector.setText(String.valueOf(stepDetect));
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    @Override
    protected  void onResume(){
        super.onResume();
        if(sensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER)!=null)
            sensorManager.registerListener(this, mStepCounter, SensorManager.SENSOR_DELAY_NORMAL);

        if(sensorManager.getDefaultSensor(Sensor.TYPE_STEP_DETECTOR)!=null)
            sensorManager.registerListener(this, mStepDetector, SensorManager.SENSOR_DELAY_NORMAL);
    }

    @Override
    protected  void onPause(){
        super.onPause();
        if(sensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER)!=null)
            sensorManager.unregisterListener(this, mStepCounter);

        if(sensorManager.getDefaultSensor(Sensor.TYPE_STEP_DETECTOR)!=null)
            sensorManager.unregisterListener(this, mStepDetector);

    }

    public void dataa(){
        try {
            RequestQueue requestQueue = Volley.newRequestQueue(MainActivity.this);
            String URL = url;
            JSONObject jsonBody = new JSONObject();
            jsonBody.put("stepsCount", textViewStepDetector.getText().toString());
            jsonBody.put("accessToken", idRand.getText().toString());
            final String mRequestBody = jsonBody.toString();

            StringRequest stringRequest = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
                @Override
                public void onResponse(String response) {
                    Log.i("LOG_VOLLEY", response);
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    Log.e("LOG_VOLLEY", error.toString());
                }
            }) {
                @Override
                public String getBodyContentType() {
                    return "application/json; charset=utf-8";
                }

                @Override
                public byte[] getBody() throws AuthFailureError {
                    try {
                        return mRequestBody == null ? null : mRequestBody.getBytes("utf-8");
                    } catch (UnsupportedEncodingException uee) {
                        VolleyLog.wtf("Unsupported Encoding while trying to get the bytes of %s using %s", mRequestBody, "utf-8");
                        return null;
                    }
                }

                @Override
                protected Response<String> parseNetworkResponse(NetworkResponse response) {
                    String responseString = "";
                    if (response != null) {

                        responseString = String.valueOf(response.statusCode);

                    }
                    return Response.success(responseString, HttpHeaderParser.parseCacheHeaders(response));
                }
            };

            requestQueue.add(stringRequest);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

}