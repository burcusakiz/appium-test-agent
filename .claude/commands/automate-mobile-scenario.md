---
description: Convert an existing Markdown mobile scenario into Appium pytest automation.
---

# Automate Mobile Scenario

Use the `mobile-test-agent` Skill and, when useful, the `appium-automation-engineer` subagent.

Task:

1. Read the scenario path or id from `$ARGUMENTS`.
2. Read matching existing tests and Page Objects.
3. Implement the pytest automation under the scenario's `Automation:` path.
4. Add or adjust Page Object helpers only when needed.
5. Run the narrowest validation command that does not require unavailable infrastructure.

Return changed files, validation result, and any environment blocker.
