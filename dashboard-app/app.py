"""
Test Agent Dashboard - Flask Web Server
Appium Test Automation Dashboard with Live Emulator View
"""

import os
import subprocess
import threading
import time
from datetime import datetime
from flask import Flask, render_template, jsonify, Response, request
import json

# Setup template and static folders relative to app.py location
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Configuration
REPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports', datetime.now().strftime('%Y-%m-%d'))
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, 'screenshots')
EMULATOR_SCREENSHOT_PATH = os.path.join(SCREENSHOTS_DIR, 'emulator_live.png')

# Ensure directories exist
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Global state for test runs
test_results = []
test_running = False
last_test_log = ""


def capture_emulator_screenshot():
    """Capture current emulator screen"""
    try:
        screenshot_path = os.path.join(SCREENSHOTS_DIR, 'emulator_live.png')
        result = subprocess.run(
            ['adb', 'shell', 'screencap', '-p', '/sdcard/screenshot.png'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            result = subprocess.run(
                ['adb', 'pull', '/sdcard/screenshot.png', screenshot_path],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return screenshot_path
    except Exception as e:
        print(f"Screenshot error: {e}")
    return None


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/status')
def api_status():
    """Check system status"""
    appium_running = subprocess.run(['lsof', '-i', ':4723'], capture_output=True).returncode == 0
    mock_api_running = subprocess.run(['lsof', '-i', ':8080'], capture_output=True).returncode == 0
    emulator_connected = subprocess.run(['adb', 'devices'], capture_output=True).returncode == 0

    # Capture live screenshot
    screenshot_path = capture_emulator_screenshot()

    return jsonify({
        'appium': 'running' if appium_running else 'stopped',
        'mock_api': 'running' if mock_api_running else 'stopped',
        'emulator': 'connected' if emulator_connected else 'disconnected',
        'screenshot': os.path.basename(screenshot_path) if screenshot_path else None,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/tests')
def get_tests():
    """Get list of available tests"""
    tests = [
        {'id': 'TC-001', 'name': 'Valid Login', 'path': 'tests/android/login/test_TC001_valid_login.py'},
        {'id': 'TC-002', 'name': 'Wrong Password', 'path': 'tests/android/login/test_TC002_wrong_password.py'},
        {'id': 'TC-003', 'name': 'Empty Credentials', 'path': 'tests/android/login/test_TC003_empty_credentials.py'},
        {'id': 'TC-004', 'name': 'Empty Username', 'path': 'tests/android/login/test_TC004_empty_username.py'},
        {'id': 'TC-005', 'name': 'Empty Password', 'path': 'tests/android/login/test_TC005_empty_password.py'},
        {'id': 'TC-006', 'name': 'UI Elements', 'path': 'tests/android/login/test_TC006_ui_elements.py'},
        {'id': 'TC-007', 'name': 'All Elements', 'path': 'tests/android/login/test_TC007_all_elements.py'},
        {'id': 'TC-008', 'name': 'Expected Failure', 'path': 'tests/android/login/test_TC008_expected_failure.py'},
        {'id': 'TC-009', 'name': 'API Login', 'path': 'tests/api/test_login_rest.py'},
    ]
    return jsonify(tests)


@app.route('/api/run-test', methods=['POST'])
def run_test():
    """Run selected tests"""
    global test_running, last_test_log

    data = request.get_json()
    test_paths = data.get('tests', [])

    if not test_paths:
        return jsonify({'error': 'No tests specified'}), 400

    if test_running:
        return jsonify({'error': 'Test already running'}), 400

    test_running = True
    last_test_log = ""

    # Start test in background thread
    def run_tests():
        global last_test_log

        for test_path in test_paths:
            full_path = os.path.join(os.path.dirname(__file__), '..', test_path)

            # Check if file exists
            if not os.path.exists(full_path):
                last_test_log += f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: Test not found: {test_path}<br>\n\n"
                continue

            last_test_log += f"[{datetime.now().strftime('%H:%M:%S')}] Starting: {test_path}<br>\n"

            try:
                result = subprocess.run(
                    ['pytest', full_path, '-v', '--tb=short'],
                    capture_output=True,
                    text=True,
                    timeout=300
                )

                output = result.stdout + result.stderr

                if result.returncode == 0:
                    last_test_log += f"[{datetime.now().strftime('%H:%M:%S')}] <span style='color:#58a6ff'>PASS</span>: {test_path}<br>\n"
                    last_test_log += output.replace('\n', '<br>') + "<br>\n"
                else:
                    last_test_log += f"[{datetime.now().strftime('%H:%M:%S')}] <span style='color:#f85149'>FAIL</span>: {test_path}<br>\n"
                    last_test_log += output.replace('\n', '<br>') + "<br>\n"
            except subprocess.TimeoutExpired:
                last_test_log += f"[{datetime.now().strftime('%H:%M:%S')}] <span style='color:#ff7b72'>ERROR</span>: {test_path} timeout<br>\n\n"
            except Exception as e:
                last_test_log += f"[{datetime.now().strftime('%H:%M:%S')}] <span style='color:#ff7b72'>ERROR</span>: {test_path} - {str(e)}<br>\n\n"

        last_test_log += f"<br><span style='color:#198754'>============================================</span><br>\n"
        last_test_log += f"<span style='color:#198754'>ALL TESTS COMPLETED</span><br>\n"
        last_test_log += f"<span style='color:#198754'>============================================</span><br>\n"

        test_running = False

    thread = threading.Thread(target=run_tests, daemon=True)
    thread.start()

    return jsonify({'status': 'started', 'tests': test_paths})


@app.route('/api/log')
def get_log():
    """Get test log"""
    return jsonify({'log': last_test_log, 'running': test_running})


@app.route('/api/emulator/screenshot')
def emulator_screenshot():
    """Get latest emulator screenshot"""
    capture_emulator_screenshot()

    # Read and return image
    try:
        with open(EMULATOR_SCREENSHOT_PATH, 'rb') as f:
            image_data = f.read()
        return Response(image_data, mimetype='image/png')
    except FileNotFoundError:
        return jsonify({'error': 'No screenshot available'}), 404


@app.route('/api/reports/list')
def list_reports():
    """List all available reports"""
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')

    if not os.path.exists(reports_dir):
        return jsonify({'error': 'No reports directory'}), 404

    # Get all date directories with their report info
    report_list = []
    dates = sorted([d for d in os.listdir(reports_dir) if os.path.isdir(os.path.join(reports_dir, d))], reverse=True)

    for date in dates:
        report_path = os.path.join(reports_dir, date, 'report.html')
        if os.path.exists(report_path):
            # Get file size
            size = os.path.getsize(report_path)
            # Get file modification time
            mtime = os.path.getmtime(report_path)

            # Parse report to get test counts (simple HTML parsing)
            try:
                with open(report_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    passed = content.count("style='color:#198754'")
                    failed = content.count("style='color:#f85149'")
            except:
                passed = 0
                failed = 0

            report_list.append({
                'date': date,
                'path': f'reports/{date}/report.html',
                'size': size,
                'modified': datetime.fromtimestamp(mtime).isoformat(),
                'passed': passed,
                'failed': failed
            })

    return jsonify({'reports': report_list, 'count': len(report_list)})


@app.route('/api/reports/latest')
def latest_report():
    """Get latest report information"""
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')

    if not os.path.exists(reports_dir):
        return jsonify({'error': 'No reports directory'}), 404

    # Get latest date directory
    dates = sorted([d for d in os.listdir(reports_dir) if os.path.isdir(os.path.join(reports_dir, d))], reverse=True)

    if not dates:
        return jsonify({'error': 'No reports found'}), 404

    latest_date = dates[0]
    report_path = os.path.join(reports_dir, latest_date, 'report.html')

    if os.path.exists(report_path):
        return jsonify({
            'date': latest_date,
            'path': f'reports/{latest_date}/report.html',
            'exists': True
        })

    return jsonify({'error': 'Report not found'}), 404


@app.route('/api/reports/<report_date>/html')
def get_report_html(report_date):
    """Get HTML content of a specific report"""
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    report_path = os.path.join(reports_dir, report_date, 'report.html')

    if not os.path.exists(report_path):
        return jsonify({'error': 'Report not found'}), 404

    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return jsonify({
            'date': report_date,
            'html': html_content,
            'exists': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reports/<report_date>')
def view_report(report_date):
    """Serve report HTML directly"""
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    report_path = os.path.join(reports_dir, report_date, 'report.html')

    if not os.path.exists(report_path):
        return "Report not found", 404

    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading report: {str(e)}", 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
