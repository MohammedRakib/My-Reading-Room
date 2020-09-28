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

public class SignUpActivity extends AppCompatActivity implements View.OnClickListener {
public EditText signUpUserNameEditText, signUpPassWordOneEditText, signUpPassWordTwoEditText;
public Button signUpActivitySignUpButton;
public TextView loginInsteadTextView, signUpErrorTextView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up);

        signUpUserNameEditText = findViewById(R.id.signUpActivityUserNameEditTextID);
        signUpPassWordOneEditText = findViewById(R.id.signUpActivityPassWordOneEditTextID);
        signUpPassWordTwoEditText = findViewById(R.id.signUpActivityPassWordTwoEditTextID);

        signUpActivitySignUpButton = findViewById(R.id.signUpActivitySignUpButtonID);

        loginInsteadTextView = findViewById(R.id.LoginInsteadTextViewID);
        signUpErrorTextView = findViewById(R.id.signUpErrorTextViewID);

        signUpActivitySignUpButton.setOnClickListener(this);
        loginInsteadTextView.setOnClickListener(this);


    }

    @Override
    public void onClick(View v) {
        if (R.id.signUpActivitySignUpButtonID==v.getId()){
            if(signUpPassWordOneEditText.getText().toString().equals(signUpPassWordTwoEditText.getText().toString())){
                String name = signUpUserNameEditText.getText().toString();
                String pass = signUpPassWordOneEditText.getText().toString();

                OkHttpClient client = new OkHttpClient();
                MediaType mediaType = MediaType.parse("application/json");
                RequestBody body = RequestBody.create(mediaType, String.format("{\"username\": \"%s\", \"password\":\"%s\"}", name, pass));

                Request request = new Request.Builder()
                        .url("http://192.168.0.106:8000/api/signup/")
                        .method("POST", body)
                        .addHeader("Content-Type", "application/json")
                        .build();
                client.newCall(request).enqueue(new Callback() {
                    @Override
                    public void onFailure(Call call, IOException e) {
                        SignUpActivity.this.runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                signUpErrorTextView.setText("API Call Failed");
                            }
                        });
                        Toast.makeText(SignUpActivity.this, "API Call Failed", Toast.LENGTH_LONG).show();
                    }

                    @Override
                    public void onResponse( Call call,  Response response) throws IOException {
                        if(response.isSuccessful()){
                            final String myresponse = response.body().string();

                            if (myresponse.equals("{\"error\": \"Username is already take!\"}")){
                                SignUpActivity.this.runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
                                        signUpErrorTextView.setText("Username is already taken");
                                    }
                                });
                            }
                            else{
                                Intent classRoomHomeActivityIntent = new Intent(getApplicationContext(), ClassRoomHomeActivity.class);
                                classRoomHomeActivityIntent.putExtra("AUTH_TOKEN", myresponse);
                                startActivity(classRoomHomeActivityIntent);
                            }
                        }
                    }
                });

            }
            else {
                signUpErrorTextView.setText("Password did not matched");
            }

        }
        if (R.id.LoginInsteadTextViewID==v.getId()){
            Intent loginIntent = new Intent(getApplicationContext(), MainActivity.class);
            startActivity(loginIntent);
        }
    }
}