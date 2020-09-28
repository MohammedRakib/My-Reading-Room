package com.example.myreadingroomapp;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
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

public class ViewJoinedClassesActivity extends AppCompatActivity implements View.OnClickListener {
    public String auth_token;
    public TextView view_joined_classes_textView;
    public Button refresh, joinClassButton;
    public EditText classCodeEditText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_joined_classes);

        auth_token = getIntent().getStringExtra("AUTH_TOKEN");
        view_joined_classes_textView = findViewById(R.id.view_joined_class_text_viewID);
        view_joined_classes_textView.setMovementMethod(new ScrollingMovementMethod());

        refresh = findViewById(R.id.join_class_refreshButtonID);

        joinClassButton = findViewById(R.id.joinClassButtonID);
        classCodeEditText = findViewById(R.id.classCodeEditTextID);


        refresh.setOnClickListener(this);
        joinClassButton.setOnClickListener(this);

    }

    @Override
    public void onClick(View v) {
        if (R.id.join_class_refreshButtonID == v.getId()) {
            OkHttpClient client = new OkHttpClient();
            Request request = new Request.Builder()
                    .url("http://192.168.0.106:8000/api/home_classroom_view_joined/")
                    .method("GET", null)
                    .addHeader("Authorization", "Token " + auth_token)
                    .build();
            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    Toast.makeText(ViewJoinedClassesActivity.this, "API Call Failed", Toast.LENGTH_LONG).show();
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    if (response.isSuccessful()) {
                        final String myresponse = response.body().string();
                        ViewJoinedClassesActivity.this.runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Gson gson = new GsonBuilder().setPrettyPrinting().create();
                                JsonParser jp = new JsonParser();
                                JsonElement je = jp.parse(myresponse);
                                view_joined_classes_textView.setText(gson.toJson(je));
                            }
                        });
                    }
                }
            });
        }
        if (R.id.joinClassButtonID == v.getId()) {
//            Toast.makeText(this, "Join Class Button ID", Toast.LENGTH_SHORT).show();
            String classCode = classCodeEditText.getText().toString();

            OkHttpClient client = new OkHttpClient();
            MediaType mediaType = MediaType.parse("application/json");
            RequestBody body = RequestBody.create(mediaType, String.format("{\"classCode\": \"%s\"}", classCode));
            Request request = new Request.Builder()
                    .url("http://192.168.0.106:8000/api/get_classroom_id/")
                    .method("POST", body)
                    .addHeader("Content-Type", "application/json")
                    .build();
            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    Toast.makeText(ViewJoinedClassesActivity.this, "API Call Failed", Toast.LENGTH_LONG).show();
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    if (response.isSuccessful()) {
                        String myresponse = response.body().string();
                        myresponse = myresponse.replace("{\"token\": \"", "");
                        myresponse = myresponse.replace("\"}", "");
                        if (myresponse.equals("No class found with that class code")) {
                            ViewJoinedClassesActivity.this.runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    Toast.makeText(ViewJoinedClassesActivity.this, "No class found with that class code", Toast.LENGTH_SHORT).show();
                                }
                            });
                        } else {
                            final int class_pk = Integer.parseInt(myresponse);
                            ViewJoinedClassesActivity.this.runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    Toast.makeText(ViewJoinedClassesActivity.this, Integer.toString(class_pk), Toast.LENGTH_SHORT).show();
                                }
                            });
                            OkHttpClient client = new OkHttpClient();
                            MediaType mediaType = MediaType.parse("application/json");
                            RequestBody body = RequestBody.create(mediaType, "");
                            final Request request = new Request.Builder()
                                    .url(String.format("http://192.168.0.106:8000/api/classroom/%d/join/", class_pk))
                                    .method("PUT", body)
                                    .addHeader("Content-Type", "application/json")
                                    .addHeader("Authorization", "Token " + auth_token)
                                    .build();
                            client.newCall(request).enqueue(new Callback() {
                                @Override
                                public void onFailure(Call call, IOException e) {
                                    ViewJoinedClassesActivity.this.runOnUiThread(new Runnable() {
                                        @Override
                                        public void run() {
                                            Toast.makeText(ViewJoinedClassesActivity.this, "Join Class API Called Failed", Toast.LENGTH_SHORT).show();
                                        }
                                    });
                                }

                                @Override
                                public void onResponse(Call call, Response response) throws IOException {
                                    if (response.isSuccessful()) {
                                        String myresponse = response.body().string();
                                        myresponse = myresponse.replace("{\"detail\":\"", "");
                                        myresponse = myresponse.replace("\"}", "");
                                        final String finalMyresponse = myresponse;
                                        ViewJoinedClassesActivity.this.runOnUiThread(new Runnable() {
                                            @Override
                                            public void run() {
                                                Toast.makeText(ViewJoinedClassesActivity.this, finalMyresponse, Toast.LENGTH_LONG).show();
                                            }
                                        });
                                        if (finalMyresponse.equals("Not found.")) {
                                            ViewJoinedClassesActivity.this.runOnUiThread(new Runnable() {
                                                @Override
                                                public void run() {
                                                    Toast.makeText(ViewJoinedClassesActivity.this, "You are already joined in this class", Toast.LENGTH_LONG).show();
                                                }
                                            });
                                        } else {
                                            ViewJoinedClassesActivity.this.runOnUiThread(new Runnable() {
                                                @Override
                                                public void run() {
                                                    Toast.makeText(ViewJoinedClassesActivity.this, "Successfully joined in this class", Toast.LENGTH_LONG).show();
                                                }
                                            });
                                        }
                                    }
                                }
                            });
                        }
                    }
                }
            });

        }
    }
}