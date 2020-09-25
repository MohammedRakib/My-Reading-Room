package com.example.myreadingroomapp;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
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

        OkHttpClient client = new OkHttpClient();
        MediaType mediaType = MediaType.parse("application/json");

        RequestBody body = RequestBody.create(mediaType, "{\"username\": \"srs\", \"password\":\"12345678\"}");

        Request request = new Request.Builder()
                .url("http://192.168.0.107:8000/api/login/")
                .method("POST", body)
                .addHeader("Content-Type", "application/json")
                .build();

//        try {
//            final Response response = client.newCall(request).execute();
//            MainActivity.this.runOnUiThread(new Runnable() {
//                @Override
//                public void run() {
//                    textView.setText(response.body().toString());
//                }
//            });
//        }
//        catch (Exception e){
//            textView.setText(e.toString());
//        }

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                textView.setText(e.toString());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if(response.isSuccessful()){
                    final String myresponse = response.body().string();
                    MainActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            textView.setText(myresponse);
                        }
                    });
                }
            }
        });

    }
}