.PHONY: test test-android test-api mock appium clean start-servers stop-servers

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

# Start all servers (Appium + Mock API)
start-servers:
	@echo "Starting all servers..."
	make appium
	@sleep 2
	make mock
	@echo "All servers started"

# Stop all servers
stop-servers:
	@echo "Stopping servers..."
	@pkill -f "appium --port 4723" || true
	@pkill -f "python3 mock_api_server.py" || true
	@echo "All servers stopped"

# Clean generated files
clean:
	rm -rf reports/ .pytest_cache/ __pycache__/
	make stop-servers

# Full clean (including virtual environment)
full-clean:
	rm -rf reports/ .pytest_cache/ __pycache__/ venv/
	make stop-servers

# Run tests with server management
run:
	make start-servers
	@sleep 2
	python3 run_tests.py
	make stop-servers

# Run tests with coverage
coverage:
	pip install pytest-cov
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# Run specific test file
run-test:
	python3 run_tests.py -k "$(TEST)"

# Run tests in parallel (requires pytest-xdist)
parallel:
	pytest tests/ -n auto -v

# Generate HTML report only
report:
	pytest tests/ -v --html=reports/report.html --self-contained-html

# Start dashboard app
dashboard:
	./venv/bin/python dashboard-app/app.py

# Install dependencies
install:
	pip install -r requirements.txt

# Run all tests with verbose output
verbose-test:
	pytest tests/ -vv -s
