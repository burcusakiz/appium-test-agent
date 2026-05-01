.PHONY: test test-android test-api mock appium clean

# Start mock API server
mock:
	python3 mock_api_server.py &

# Start Appium server
appium:
	appium --port 4723 --log-level error &

# Run all tests
test:
	python3 run_tests.py

# Run Android tests only
test-android:
	pytest tests/android/ -v --html=reports/$$(date +%Y-%m-%d)/report.html --self-contained-html

# Run API tests only
test-api:
	pytest tests/api/ -v

# Run smoke tests only
test-smoke:
	pytest -m smoke -v

# Clean generated files
clean:
	rm -rf reports/ .pytest_cache/ __pycache__/

# Start dashboard app
dashboard:
	./venv/bin/python dashboard-app/app.py
