package com.example.py_charmer;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class ExecutableService extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        Toast.makeText(context, "Hi I am Executed", Toast.LENGTH_SHORT).show();
    }
}
