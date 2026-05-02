---
description: Run Android Appium/API pytest tests and produce reports under reports/YYYY-MM-DD.
---

# Run Mobile Tests

Use the `mobile-test-agent` Skill and, when useful, the `test-runner-debugger` subagent.

Task:

1. Interpret `$ARGUMENTS` as a pytest target, marker, or platform.
2. Prefer `python3 run_tests.py` commands so reports are written consistently.
3. If no target is provided, run Android tests with `python3 run_tests.py --platform android`.
4. Inspect failures and report the exact failing tests.
5. Mention the generated report path.

Do not start or stop unrelated processes.
