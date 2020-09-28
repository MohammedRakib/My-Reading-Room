package com.example.myreadingroomapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class ClassRoomHomeActivity extends AppCompatActivity implements View.OnClickListener {
    public TextView textView;
    public Button createViewClassButton, viewJoinedClasses;
    public String auth_token;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_class_room_home);

        auth_token = getIntent().getStringExtra("AUTH_TOKEN");
        auth_token = auth_token.replace("{\"token\": \"","");
        auth_token = auth_token.replace("\"}","");
        Toast.makeText(this, auth_token, Toast.LENGTH_LONG).show();

        createViewClassButton = findViewById(R.id.create_or_view_created_class);
        viewJoinedClasses = findViewById(R.id.view_joined_class);

        createViewClassButton.setOnClickListener(this);
        viewJoinedClasses.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        if(R.id.create_or_view_created_class==v.getId()){
            Intent intent = new Intent(getApplicationContext(), ViewClassOrCreateClassActivity.class);
            intent.putExtra("AUTH_TOKEN", auth_token);
            startActivity(intent);
        }
        if (R.id.view_joined_class==v.getId()){
            Intent intent = new Intent(getApplicationContext(), ViewJoinedClassesActivity.class);
            intent.putExtra("AUTH_TOKEN", auth_token);
            startActivity(intent);
        }

    }
}