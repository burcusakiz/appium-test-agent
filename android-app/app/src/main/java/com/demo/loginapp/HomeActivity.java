package com.demo.loginapp;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class HomeActivity extends AppCompatActivity {

    private TextView textViewWelcome;
    private Button logoutButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        textViewWelcome = findViewById(R.id.textViewWelcome);
        logoutButton = findViewById(R.id.buttonLogout);

        // Get username from intent
        Intent intent = getIntent();
        String username = intent.getStringExtra("username");

        // Display welcome message
        if (username != null && !username.isEmpty()) {
            textViewWelcome.setText("Welcome " + username + "!");
        }

        logoutButton.setOnClickListener(v -> logout());
    }

    private void logout() {
        // Navigate back to login screen
        Intent intent = new Intent(this, LoginActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(intent);
        finish();
    }
}
