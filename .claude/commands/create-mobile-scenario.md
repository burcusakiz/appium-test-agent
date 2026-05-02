---
description: Create a human-readable mobile test scenario in test-scenarios using the repository scenario format.
---

# Create Mobile Scenario

Use the `mobile-test-agent` Skill and, when useful, the `scenario-author` subagent.

Task:

1. Interpret the user's requested scenario from `$ARGUMENTS`.
2. Read existing files under `test-scenarios/` to identify the suite and next `TC-000X` id.
3. Create or update one Markdown scenario using the repository format.
4. Include an `Automation:` path for the future pytest file.
5. Do not write automation code unless the user explicitly requested it.

Return the scenario path and any assumption that affects expected behavior.
