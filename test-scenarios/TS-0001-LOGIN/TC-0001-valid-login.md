# TC-0001: Valid Login

App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: High

Steps:
1. Launch the application
2. Enter username: testuser
3. Enter password: password123
4. Tap the Login button

Expected:
Home screen is displayed. Welcome message contains "testuser". Logout button is visible.

Automation: tests/android/login/test_TC001_valid_login.py
