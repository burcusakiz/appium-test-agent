package com.demo.loginapp;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class LoginActivity extends AppCompatActivity {

    private EditText editTextUsername;
    private EditText editTextPassword;
    private TextView textViewError;
    private Button loginButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        editTextUsername = findViewById(R.id.username_input);
        editTextPassword = findViewById(R.id.password_input);
        textViewError = findViewById(R.id.textViewError);
        loginButton = findViewById(R.id.login_button);

        loginButton.setOnClickListener(v -> performLogin());
    }

    private void performLogin() {
        String username = editTextUsername.getText().toString().trim();
        String password = editTextPassword.getText().toString().trim();

        // Clear previous error
        textViewError.setText("");

        // Validate empty fields
        if (username.isEmpty() || password.isEmpty()) {
            textViewError.setText("Please enter username and password");
            return;
        }

        // Validate credentials
        if (isValidCredentials(username, password)) {
            // Login successful - navigate to home screen
            Intent intent = new Intent(this, HomeActivity.class);
            intent.putExtra("username", username);
            startActivity(intent);
            finish();
        } else {
            // Login failed
            textViewError.setText("Invalid credentials");
            editTextPassword.setText("");
        }
    }

    private boolean isValidCredentials(String username, String password) {
        // Valid credentials: testuser / password123
        return "testuser".equals(username) && "password123".equals(password);
    }
}
