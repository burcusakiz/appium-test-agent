# TC-0005: Empty Password

App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: Medium

Steps:
1. Launch the application
2. Enter username: testuser
3. Leave password empty
4. Tap the Login button

Expected:
User remains on login screen. Error message is displayed.

Automation: tests/android/login/test_TC005_empty_password.py
