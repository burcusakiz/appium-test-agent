#!/usr/bin/env python3
"""Project test runner for Appium/API automation."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Appium/API tests and write reports under reports/YYYY-MM-DD/."
    )
    parser.add_argument(
        "target",
        nargs="*",
        help="Optional pytest targets, for example tests/android/login/test_TC001_valid_login.py",
    )
    parser.add_argument(
        "--platform",
        choices=["all", "android", "api"],
        default=os.getenv("TEST_PLATFORM", "android"),
        help="Default test group when no explicit target is provided.",
    )
    parser.add_argument("-k", "--keyword", help="Pytest -k expression.")
    parser.add_argument("-m", "--mark", help="Pytest marker expression.")
    parser.add_argument(
        "--html",
        action="store_true",
        help="Also generate an HTML report for API-only runs.",
    )
    parser.add_argument(
        "--extra",
        nargs=argparse.REMAINDER,
        help="Arguments after --extra are passed directly to pytest.",
    )
    return parser.parse_args(argv)


def build_pytest_args(args: argparse.Namespace) -> list[str]:
    report_date = datetime.now().strftime("%Y-%m-%d")
    report_dir = ROOT_DIR / "reports" / report_date
    report_dir.mkdir(parents=True, exist_ok=True)

    pytest_args = ["pytest", "-v"]

    if args.target:
        pytest_args.extend(args.target)
    elif args.platform == "android":
        pytest_args.append("tests/android")
    elif args.platform == "api":
        pytest_args.append("tests/api")
    else:
        pytest_args.append("tests")

    if args.keyword:
        pytest_args.extend(["-k", args.keyword])

    if args.mark:
        pytest_args.extend(["-m", args.mark])

    should_write_html = args.platform != "api" or args.html or bool(args.target)
    if should_write_html:
        report_name = "api-report.html" if args.platform == "api" and not args.target else "report.html"
        pytest_args.extend(
            [
                f"--html={report_dir / report_name}",
                "--self-contained-html",
            ]
        )

    if args.extra:
        pytest_args.extend(args.extra)

    return pytest_args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    pytest_args = build_pytest_args(args)
    print("Running:", " ".join(pytest_args))
    return subprocess.call(pytest_args, cwd=ROOT_DIR)


if __name__ == "__main__":
    raise SystemExit(main())
