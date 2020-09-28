package com.example.myreadingroomapp;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.text.Editable;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class ViewClassOrCreateClassActivity extends AppCompatActivity implements View.OnClickListener {
    public String auth_token;
    public TextView view_create_class_text_view;
    public Button refresh, createClassButton;
    public EditText className, classSection;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_class_or_create_class);

        auth_token = getIntent().getStringExtra("AUTH_TOKEN");

        view_create_class_text_view = findViewById(R.id.view_create_class_text_viewID);
        view_create_class_text_view.setMovementMethod(new ScrollingMovementMethod());

        className = findViewById(R.id.class_name_EditTextID);
        classSection = findViewById(R.id.class_section_EditTextID);
        createClassButton = findViewById(R.id.create_class_buttonID);

        refresh = findViewById(R.id.refreshButtonID);
        createClassButton.setOnClickListener(this);

        refresh.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {

        if (R.id.refreshButtonID == v.getId()) {
            OkHttpClient client = new OkHttpClient();
            Request request = new Request.Builder()
                    .url("http://192.168.0.106:8000/api/home_classroom_create/")
                    .method("GET", null)
                    .addHeader("Authorization", "Token " + auth_token)
                    .build();
            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    Toast.makeText(ViewClassOrCreateClassActivity.this, "API Call Failed", Toast.LENGTH_LONG).show();
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    if (response.isSuccessful()) {
                        final String myresponse = response.body().string();
                        ViewClassOrCreateClassActivity.this.runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Gson gson = new GsonBuilder().setPrettyPrinting().create();
                                JsonParser jp = new JsonParser();
                                JsonElement je = jp.parse(myresponse);
                                view_create_class_text_view.setText(gson.toJson(je));
                            }
                        });
                    }
                }
            });
        }
        if (R.id.create_class_buttonID == v.getId()) {
            String name = className.getText().toString();
            String sec = classSection.getText().toString();

            if (!name.isEmpty() && !sec.isEmpty()) {
                OkHttpClient client = new OkHttpClient();

                MediaType mediaType = MediaType.parse("application/json");

                RequestBody body = RequestBody.create(mediaType, String.format("{\"name\": \"%s\", \"section\":\"%s\"}", name, sec));

                final Request request = new Request.Builder()
                        .url("http://192.168.0.106:8000/api/home_classroom_create/")
                        .method("POST", body)
                        .addHeader("Content-Type", "application/json")
                        .addHeader("Authorization", "Token " + auth_token)
                        .build();

                client.newCall(request).enqueue(new Callback() {
                    @Override
                    public void onFailure(Call call, IOException e) {
                        ViewClassOrCreateClassActivity.this.runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(ViewClassOrCreateClassActivity.this, "Create Class API called Failed", Toast.LENGTH_LONG).show();
                            }
                        });
                    }

                    @Override
                    public void onResponse(Call call, final Response response) throws IOException {
                        if (response.isSuccessful()) {
                            final String myresponse = response.body().string();
                            ViewClassOrCreateClassActivity.this.runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    Toast.makeText(ViewClassOrCreateClassActivity.this, myresponse, Toast.LENGTH_LONG).show();
                                }
                            });
                        }
                    }
                });
            } else {
                ViewClassOrCreateClassActivity.this.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(ViewClassOrCreateClassActivity.this, "Class Name or Section Cant be Empty!", Toast.LENGTH_LONG).show();
                    }
                });
            }
        }
    }
}