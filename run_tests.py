#!/usr/bin/env python3
"""
Test Runner Script for Appium Test Agent
Executes all tests and generates HTML report using pytest and pytest-html
"""

import subprocess
import sys
import os
import argparse
from datetime import datetime


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Appium Test Agent - Execute tests and generate HTML report"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "-k", "--keywords",
        type=str,
        default="",
        help="Only run tests matching the given keyword expression"
    )
    parser.add_argument(
        "-m", "--markers",
        type=str,
        default="",
        help="Only run tests matching the given marker expression"
    )
    parser.add_argument(
        "-x", "--exitfirst",
        action="store_true",
        help="Exit instantly on first error or failed test"
    )
    parser.add_argument(
        "--app-path",
        type=str,
        default=None,
        help="Path to the Android APK file"
    )
    parser.add_argument(
        "--platform-version",
        type=str,
        default=None,
        help="Android platform version"
    )
    parser.add_argument(
        "--device-name",
        type=str,
        default=None,
        help="Device name for Appium"
    )
    parser.add_argument(
        "--report-name",
        type=str,
        default=None,
        help="Name of the output HTML report"
    )
    parser.add_argument(
        "--date-report",
        action="store_true",
        help="Create date-based report in reports/YYYY-MM-DD/report.html"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run tests in headless mode (no UI)"
    )
    return parser.parse_args()


def get_report_path(args):
    """Generate report path based on arguments"""
    if args.date_report:
        date_dir = datetime.now().strftime("%Y-%m-%d")
        report_dir = os.path.join("reports", date_dir)
        os.makedirs(report_dir, exist_ok=True)
        return os.path.join(report_dir, "report.html")

    if args.report_name:
        report_dir = os.path.join("reports")
        os.makedirs(report_dir, exist_ok=True)
        return os.path.join(report_dir, args.report_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"test_report_{timestamp}.html"
    return os.path.join("reports", report_name)


def get_appium_options(args):
    """Build Appium environment variables from arguments"""
    env_vars = {}

    if args.app_path:
        env_vars["APP_PATH"] = args.app_path
    if args.platform_version:
        env_vars["PLATFORM_VERSION"] = args.platform_version
    if args.device_name:
        env_vars["DEVICE_NAME"] = args.device_name

    return env_vars


def run_tests(args):
    """Run pytest with the specified arguments"""
    print("=" * 60)
    print("Appium Test Agent - Test Runner")
    print("=" * 60)
    print()

    # Get report path
    report_path = get_report_path(args)

    # Build pytest command
    cmd = ["pytest", "-v"]

    # Add markers if specified
    if args.markers:
        cmd.extend(["-m", args.markers])
    elif args.keywords:
        cmd.extend(["-k", args.keywords])

    # Add other options
    if args.verbose:
        cmd.append("-vv")
    if args.exitfirst:
        cmd.append("-x")

    # Add pytest-html options
    cmd.extend(["--html", report_path, "--self-contained-html", "--tb=short"])

    # Add test directory
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    cmd.append(test_dir)

    print("Pytest command:")
    print(" ".join(cmd))
    print()

    # Set environment variables
    env = os.environ.copy()
    env.update(get_appium_options(args))

    print(f"Test Report: {report_path}")
    print()

    # Run tests
    print("-" * 60)
    print("Running tests...")
    print("-" * 60)
    print()

    result = subprocess.run(cmd, env=env, cwd=os.path.dirname(os.path.abspath(__file__)))

    print()
    print("-" * 60)

    if result.returncode == 0:
        print("All tests passed!")
    else:
        print(f"Tests failed with exit code: {result.returncode}")

    print("-" * 60)
    print()

    # Print summary
    print("Summary:")
    print(f"  - Report: file://{os.path.abspath(report_path)}")
    print(f"  - Tests directory: {test_dir}")
    print()

    return result.returncode


def main():
    """Main entry point"""
    args = parse_args()
    exit_code = run_tests(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
