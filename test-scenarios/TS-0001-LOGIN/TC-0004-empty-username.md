# TC-0004: Empty Username

App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: Medium

Steps:
1. Launch the application
2. Enter password: password123
3. Leave username empty
4. Tap the Login button

Expected:
User remains on login screen. Error message is displayed.

Automation: tests/android/login/test_TC004_empty_username.py
