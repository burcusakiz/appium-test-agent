"""
Test Agent Dashboard - Flask Web Server
Appium Test Automation Dashboard with Live Emulator View
"""

import os
import re
import subprocess
import threading
import time
from datetime import datetime
from flask import Flask, render_template, jsonify, Response, request
import json
import base64

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
test_passed = 0
test_failed = 0


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
    """Main dashboard page - Live Stream"""
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


def load_tests_from_scenarios():
    """Load tests from test-scenarios directory"""
    scenarios_dir = os.path.join(os.path.dirname(__file__), '..', 'test-scenarios')
    tests = []

    if not os.path.exists(scenarios_dir):
        return tests

    # Find all TC-*.md files
    for root, dirs, files in os.walk(scenarios_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract TC ID and name from first line
                    first_line = content.strip().split('\n')[0].strip()
                    match = re.match(r'^# (TC-\d+):\s*(.+)$', first_line)
                    if match:
                        tc_id = match.group(1)
                        tc_name = match.group(2).strip()

                        # Find automation path from content
                        path_match = re.search(r'Automation:\s*(.+)', content)
                        test_path = path_match.group(1).strip() if path_match else ''

                        tests.append({
                            'id': tc_id,
                            'name': tc_name,
                            'path': test_path,
                            'scenario_path': os.path.relpath(filepath, os.path.dirname(__file__))
                        })
                except Exception as e:
                    print(f"Error reading {file}: {e}")

    return tests


@app.route('/api/debug')
def debug_tests():
    """Debug endpoint to see what files are found and their first lines"""
    scenarios_dir = os.path.join(os.path.dirname(__file__), '..', 'test-scenarios')
    project_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    debug_info = {
        'scenarios_dir': scenarios_dir,
        'project_dir': project_dir,
        'dir_exists': os.path.exists(scenarios_dir),
        'files': []
    }

    if os.path.exists(scenarios_dir):
        for root, dirs, files in os.walk(scenarios_dir):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        first_line = content.split('\n')[0].strip() if content else ''
                        # Find automation path from content
                        path_match = re.search(r'Automation:\s*(.+)', content)
                        test_path = path_match.group(1).strip() if path_match else ''

                        # Check if test file exists
                        abs_test_path = os.path.join(project_dir, test_path) if test_path else ''
                        file_exists = os.path.exists(abs_test_path) if test_path else False

                        debug_info['files'].append({
                            'path': filepath,
                            'filename': file,
                            'first_line': first_line,
                            'first_line_repr': repr(first_line),
                            'automation_path': test_path,
                            'absolute_test_path': abs_test_path,
                            'test_file_exists': file_exists
                        })
                    except Exception as e:
                        debug_info['files'].append({
                            'path': filepath,
                            'filename': file,
                            'error': str(e)
                        })

    tests = load_tests_from_scenarios()
    debug_info['parsed_tests'] = tests
    debug_info['test_count'] = len(tests)

    return jsonify(debug_info)


@app.route('/api/tests')
def get_tests():
    """Get list of available tests from scenarios"""
    tests = load_tests_from_scenarios()
    # Add test count to response
    return jsonify({'tests': tests, 'count': len(tests)})


@app.route('/api/run-test', methods=['POST'])
def run_test():
    """Run only the selected tests, one by one with fresh app state each time."""
    global test_running, last_test_log, test_passed, test_failed

    data = request.get_json()
    test_ids = data.get('tests', [])

    # DEBUG: Log selected test IDs
    last_test_log += f"<span style='color:#58a6ff'>[DEBUG] Backend received test IDs: {test_ids}</span><br>\n"

    if test_running:
        return jsonify({'error': 'Test already running'}), 400

    if not test_ids:
        return jsonify({'error': 'No tests selected'}), 400

    # Map selected TC IDs → absolute file paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.normpath(os.path.join(base_dir, '..'))

    all_scenarios = load_tests_from_scenarios()
    id_to_path = {s['id']: s['path'] for s in all_scenarios}

    test_files = []
    missing = []
    for tid in test_ids:
        rel = id_to_path.get(tid)
        if rel:
            abs_path = os.path.join(project_dir, rel)
            if os.path.exists(abs_path):
                test_files.append((tid, abs_path))
            else:
                missing.append(f"{tid} → {rel} (dosya bulunamadı)")
        else:
            missing.append(f"{tid} (senaryo bulunamadı)")

    if not test_files:
        return jsonify({'error': 'Seçilen testler için dosya bulunamadı: ' + ', '.join(missing)}), 400

    # Add debug info to log
    last_test_log += f"<span style='color:#58a6ff'>[DEBUG] Seçilen test IDs: {test_ids}</span><br>\n"
    last_test_log += f"<span style='color:#58a6ff'>[DEBUG] Toplam test dosyası: {len(test_files)}</span><br>\n"

    test_running = True
    last_test_log = ""
    test_passed = 0
    test_failed = 0

    def run_tests():
        global last_test_log, test_running, test_passed, test_failed

        if missing:
            for m in missing:
                last_test_log += f"<span style='color:#ff7b72'>UYARI: {m}</span><br>\n"

        last_test_log += f"[{datetime.now().strftime('%H:%M:%S')}] <span style='color:#58a6ff'>[DEBUG] Çalıştırılacak test sayısı: {len(test_files)}</span><br>\n"

        for tid, filepath in test_files:
            last_test_log += f"<br>[{datetime.now().strftime('%H:%M:%S')}] ▶ <span style='color:#58a6ff'>[DEBUG] Çalıştırılıyor: {tid} ({filepath})</span><br>\n"
            try:
                result = subprocess.run(
                    ['pytest', filepath, '-v', '--tb=short', '--color=no'],
                    capture_output=True,
                    text=True,
                    timeout=300,
                    cwd=project_dir
                )
                output = (result.stdout + result.stderr).replace('\n', '<br>')

                tc_passed = result.stdout.count(' PASSED')
                tc_failed = result.stdout.count(' FAILED') + result.stdout.count(' ERROR')
                test_passed += tc_passed
                test_failed += tc_failed

                # Add clear step results
                last_test_log += f"<br><div style='margin: 8px 0; padding: 8px; background: #0d0d16; border-radius: 4px; border-left: 3px solid #198754;'>"
                last_test_log += f"<span class='step-pass'>PASS: {tid} - {tc_passed} test geçti</span>"
                last_test_log += f"</div><br>"

                if result.returncode != 0 and tc_failed > 0:
                    last_test_log += f"<div style='margin: 8px 0; padding: 8px; background: #0d0d16; border-radius: 4px; border-left: 3px solid #dc3545;'>"
                    last_test_log += f"<span class='step-fail'>FAIL: {tid} - {tc_failed} test başarısız</span>"
                    last_test_log += f"</div><br>"

                last_test_log += f"<div style='margin: 4px 0; padding: 4px; background: #161625; border-radius: 4px;'>{output}</div><br>"

            except subprocess.TimeoutExpired:
                test_failed += 1
                last_test_log += f"<span style='color:#ff7b72'>✗ {tid} TIMEOUT</span><br>\n"
            except Exception as e:
                test_failed += 1
                last_test_log += f"<span style='color:#ff7b72'>✗ {tid} ERROR: {str(e)}</span><br>\n"

        last_test_log += f"<br><span style='color:#198754'>{'='*44}</span><br>\n"
        last_test_log += f"<span style='color:#198754'>TAMAMLANDI: {test_passed} geçti, {test_failed} başarısız</span><br>\n"
        last_test_log += f"<span style='color:#198754'>{'='*44}</span><br>\n"

        test_running = False

    threading.Thread(target=run_tests, daemon=True).start()
    return jsonify({'status': 'started', 'tests': test_ids})


@app.route('/api/log')
def get_log():
    """Get test log"""
    return jsonify({'log': last_test_log, 'running': test_running, 'passed': test_passed, 'failed': test_failed})


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


# Live stream thread and state
live_stream_active = False
live_stream_thread = None


def generate_live_screenshots():
    """Generate live screenshots in base64 for SSE stream"""
    global live_stream_active
    while live_stream_active:
        try:
            # Capture screenshot via adb
            result = subprocess.run(
                ['adb', 'shell', 'screencap', '-p'],
                capture_output=True,
                timeout=3
            )
            if result.returncode == 0:
                # Convert PNG data to base64
                image_data = result.stdout
                base64_image = base64.b64encode(image_data).decode('utf-8')
                yield f"data:image/png;base64,{base64_image}\n\n"
            else:
                yield f"data:error\n\n"
        except Exception as e:
            yield f"data:error:{str(e)}\n\n"
        time.sleep(0.5)  # 2 FPS - duzgun performans ve bandwidth


@app.route('/api/emulator/live')
def emulator_live_stream():
    """Live emulator screen stream via SSE"""
    global live_stream_active, live_stream_thread

    def event_stream():
        global live_stream_active
        live_stream_active = True

        try:
            while live_stream_active:
                try:
                    # Capture screenshot via adb
                    result = subprocess.run(
                        ['adb', 'shell', 'screencap', '-p'],
                        capture_output=True,
                        timeout=3
                    )
                    if result.returncode == 0:
                        # Convert PNG data to base64
                        image_data = result.stdout
                        base64_image = base64.b64encode(image_data).decode('utf-8')
                        yield f"data:image/png;base64,{base64_image}\n\n"
                    else:
                        yield f"data:error\n\n"
                except Exception as e:
                    yield f"data:error:{str(e)}\n\n"

                time.sleep(0.5)  # 2 FPS
        finally:
            live_stream_active = False

    return Response(event_stream(), mimetype='text/event-stream')


@app.route('/api/emulator/live/start', methods=['POST'])
def start_live_stream():
    """Start live stream"""
    global live_stream_active
    live_stream_active = True
    return jsonify({'status': 'started'})


@app.route('/api/emulator/live/stop', methods=['POST'])
def stop_live_stream():
    """Stop live stream"""
    global live_stream_active
    live_stream_active = False
    return jsonify({'status': 'stopped'})


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
