package com.example.py_charmer;

import android.content.Context;
import android.content.Intent;

public class AlarmHandler {
    private Context context;

    public AlarmHandler(Context context) {
        this.context = context;
    }

    //This will activate the alarm
    public void setAlarmManager(){
        Intent intent = new Intent(context, ExecutableService.class);

    }
    //This will cancel the alarm
    public void cancelAlarmManager(){

    }
}
