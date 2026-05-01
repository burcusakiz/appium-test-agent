# TC-0008: Expected Failure (for screenshot testing)

App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: Low

Steps:
1. Launch the application
2. Enter username: testuser
3. Enter password: wrongpass
4. Tap the Login button

Expected:
Home screen is displayed with welcome message.

Automation: tests/android/login/test_TC008_expected_failure.py
