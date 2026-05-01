# Appium Test Agent

A complete Appium test framework for Android mobile application testing with Python, pytest, and SoapUI mock API.

## Project Structure

```
appium-test-agent/
├── app/                           # Android app source
│   ├── src/main/
│   │   ├── AndroidManifest.xml
│   │   ├── res/                   # Resources
│   │   └── java/                  # Java source (optional)
│   └── build.gradle
├── tests/                         # Python test files
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── page_objects/              # Page Object Model
│   │   ├── __init__.py
│   │   ├── login_page.py
│   │   └── home_page.py
│   ├── test_login_valid.py        # Valid login tests
│   ├── test_login_invalid.py      # Invalid login tests
│   └── test_navigation.py         # Navigation tests
├── reports/                       # Test reports output
├── screenshots/                   # Test screenshots
├── soapui/                        # SoapUI mock API
│   ├── LoginService-soapui-project.xml
│   └── start-mock-api.sh
├── config/                        # Configuration files
│   └── test_config.json
├── run_tests.py                   # Test runner script
├── pytest.ini                     # Pytest configuration
├── appium_config.json             # Appium configuration
├── requirements.txt               # Python dependencies
├── start-all.sh                   # Start all services
├── start-appium.sh                # Start Appium server
├── start-emulator.sh              # Start Android emulator
├── mock_api_server.py             # Python mock API server
└── README.md
```

## Prerequisites

- Python 3.8+
- Node.js and npm (for Appium)
- Android SDK (for emulator)
- Appium Server

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Appium:
```bash
npm install -g appium
```

3. Install Android SDK and create an AVD

## Quick Start

Run the `start-all.sh` script to start all services:
```bash
chmod +x start-all.sh
./start-all.sh
```

Or start services individually:
```bash
# Start emulator
./start-emulator.sh

# Start mock API
python3 mock_api_server.py

# Start Appium
./start-appium.sh
```

## Running Tests

### Run all tests:
```bash
python run_tests.py
```

### Run with markers:
```bash
python run_tests.py -m smoke
python run_tests.py -m login
```

### Run with keywords:
```bash
python run_tests.py -k "valid and login"
```

### Generate HTML report:
Reports are automatically generated in the `reports/` directory.

## Test Scenarios

### 1. Login with Valid Credentials
- Verify successful login redirects to home screen
- Verify welcome message is displayed correctly
- Verify status indicator shows connected

### 2. Login with Invalid Credentials
- Verify error message is displayed for invalid username
- Verify error message is displayed for invalid password
- Verify empty credentials are rejected

### 3. Navigation
- Verify navigation from login to home screen
- Verify navigation from home to login after logout
- Verify input is preserved on login error

## Mock API

The mock API is available at `http://127.0.0.1:8080/api/login`

### Login Endpoint
- **POST** `/api/login`
- **Valid credentials**: `{"username": "testuser", "password": "password123"}`
- **Response**: JSON with success status and user data

## Configuration

Edit `appium_config.json` to customize:
- Appium server settings
- Android/iOS capabilities
- Test timeouts
- Mock API settings

Edit `config/test_config.json` to customize:
- Test data
- Expected results
- Timeouts

## Report Generation

Tests automatically generate HTML reports using `pytest-html`. The report includes:
- Test results summary
- Detailed test results with timestamps
- Screenshots on failure
- Environment information

## License

MIT License
# appium-test-agent
