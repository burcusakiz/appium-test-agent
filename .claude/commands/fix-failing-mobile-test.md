---
description: Diagnose and fix failing Appium/API tests while preserving scenario intent.
---

# Fix Failing Mobile Test

Use the `mobile-test-agent` Skill and, when useful, the `test-runner-debugger` subagent.

Task:

1. Run or inspect the failing target from `$ARGUMENTS`.
2. Read the relevant scenario, test file, Page Object, and latest report/screenshot.
3. Classify the failure as environment, product behavior, or automation code.
4. Fix automation code only when the scenario expectation remains valid.
5. Rerun the smallest affected test.

Return the root cause, changed files, and validation result.
