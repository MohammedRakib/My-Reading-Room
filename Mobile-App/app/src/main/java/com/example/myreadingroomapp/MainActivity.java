package com.example.myreadingroomapp;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
public TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = findViewById(R.id.TextViewID);

        OkHttpClient client = new OkHttpClient().newBuilder()
                .build();
        MediaType mediaType = MediaType.parse("application/json");

        RequestBody body = RequestBody.create(mediaType, "{\"username\": \"srs\", \"password\":\"12345678\"}");

        Request request = new Request.Builder()
                .url("http://127.0.0.1:8000/api/login/")
                .method("POST", body)
                .addHeader("Content-Type", "application/json")
                .build();

        try {
            final Response response = client.newCall(request).execute();
            MainActivity.this.runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    textView.setText(response.body().toString());
                }
            });
        }
        catch (Exception e){
            textView.setText(e.toString());
        }

    }
}