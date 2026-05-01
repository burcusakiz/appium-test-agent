# TC-0002: Wrong Password

App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: High

Steps:
1. Launch the application
2. Enter username: testuser
3. Enter password: wrongpass
4. Tap the Login button

Expected:
User remains on login screen. Error message is displayed.

Automation: tests/android/login/test_TC002_wrong_password.py
