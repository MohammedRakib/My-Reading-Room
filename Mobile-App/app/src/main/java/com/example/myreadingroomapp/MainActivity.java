package com.example.myreadingroomapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    public EditText usernameEditText, passwordEditText;
    public Button loginButton;
    public TextView textView, singUpTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        usernameEditText = findViewById(R.id.login_username_editTextID);
        passwordEditText = findViewById(R.id.login_password_editTextID);
        loginButton = findViewById(R.id.login_buttonID);
        textView = findViewById(R.id.textViewID);
        singUpTextView = findViewById(R.id.signUpTextViewID);

        loginButton.setOnClickListener(this);
        singUpTextView.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        if (R.id.login_buttonID == v.getId()) {
            String username = usernameEditText.getText().toString();
            String password = passwordEditText.getText().toString();

            OkHttpClient client = new OkHttpClient();
            MediaType mediaType = MediaType.parse("application/json");

            RequestBody body = RequestBody.create(mediaType, String.format("{\"username\": \"%s\", \"password\":\"%s\"}", username, password));


            Request request = new Request.Builder()
                    .url("http://192.168.0.106:8000/api/login/")
                    .method("POST", body)
                    .addHeader("Content-Type", "application/json")
                    .build();
            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    MainActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            textView.setText("API Call Failed");
                        }
                    });
//                    Toast.makeText(MainActivity.this, "API Call Failed", Toast.LENGTH_LONG).show();
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {

                    if (response.isSuccessful()) {
//                        final String myresponse = response.body().string();
//
//                        MainActivity.this.runOnUiThread(new Runnable() {
//                            @Override
//                            public void run() {
//                                textView.setText(myresponse);
//                            }
//                        });
                        final String myresponse = response.body().string();

                        if (myresponse.equals("{\"token\": \"Could not login, Please check username and password\"}")) {
                            MainActivity.this.runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    textView.setText("Could not login, Please check username and password");
                                }
                            });
                        } else {
                            Intent classRoomHomeActivityIntent = new Intent(getApplicationContext(), ClassRoomHomeActivity.class);
                            classRoomHomeActivityIntent.putExtra("AUTH_TOKEN", myresponse);
                            startActivity(classRoomHomeActivityIntent);
                        }
                    }
                }
            });

        }
        if (R.id.signUpTextViewID==v.getId()){
            Intent signUpActivity = new Intent(getApplicationContext(), SignUpActivity.class);
            startActivity(signUpActivity);
        }
    }
}