# TC-0003: Empty Credentials

App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: High

Steps:
1. Launch the application
2. Leave username empty
3. Leave password empty
4. Tap the Login button

Expected:
User remains on login screen. Error message is displayed.

Automation: tests/android/login/test_TC003_empty_credentials.py
