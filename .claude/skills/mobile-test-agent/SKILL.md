---
name: mobile-test-agent
description: Create human-readable mobile test scenarios, convert them into Android Appium pytest automation, run Android/API tests, analyze failures, and update reports for this repository.
---

# Mobile Test Agent

Use this Skill when the user asks to create mobile test scenarios, generate Appium automation from scenarios, run tests on an emulator/device, analyze failures, or fix failing mobile/API tests in this repository.

## Repository Contract

- Human-authored scenarios live under `test-scenarios/<suite-id>/TC-000X-name.md`.
- Executable automation lives under `tests/android`, `tests/api`, and shared Page Objects under `tests/page_objects`.
- Test output lives under `reports/YYYY-MM-DD/`.
- Supporting references for this Skill live under `references/`.
- Android app package defaults to `com.demo.loginapp`.
- Appium server defaults to `http://127.0.0.1:4723`.
- Mock API server defaults to `http://127.0.0.1:8080`.

## Scenario Authoring Workflow

1. Read existing scenarios in the target suite before creating a new one.
2. Pick the next unused `TC-000X` id.
3. Write the scenario as Markdown with this shape:

```markdown
# TC-000X: Scenario Title

App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: High

Steps:
1. Launch the application
2. Enter username: testuser
3. Enter password: password123
4. Tap the Login button

Expected:
Home screen is displayed. Welcome message contains "testuser".

Automation: tests/android/login/test_TC00X_name.py
```

4. Keep scenario text human-readable and independent from implementation details except the final `Automation` path.

## Automation Workflow

1. Read the scenario and matching Page Objects.
2. Reuse existing Page Object methods before adding new ones.
3. Create pytest tests under the `Automation` path declared in the scenario.
4. Use clear markers: `smoke`, `regression`, `login`, `android`, `api`, or `negative`.
5. Use Appium waits or Page Object helpers for UI synchronization. Avoid `time.sleep`.
6. Keep assertions tied to the scenario's expected result.
7. If a locator is missing, inspect Android XML layouts or existing Page Objects before inventing a locator.

## Execution Workflow

Use the narrowest command that proves the change:

```bash
python3 run_tests.py tests/android/login/test_TC00X_name.py
python3 run_tests.py --platform android -m smoke
python3 run_tests.py --platform api --html
```

If emulator/Appium/mock API are not running, report that clearly and use:

```bash
make appium
make mock
```

## Failure Analysis

1. Start with pytest output and the latest `reports/YYYY-MM-DD/report.html`.
2. Check failure screenshots under `reports/YYYY-MM-DD/screenshots/`.
3. Distinguish product bugs from automation bugs:
   - Product bug: app state or response violates the scenario expectation.
   - Automation bug: stale locator, missing wait, wrong test data, wrong fixture, or bad environment.
4. Fix automation only when the scenario expectation is still valid.
5. After a fix, rerun the smallest affected test first, then the related marker/suite if needed.

## Quality Bar

- New tests must be deterministic and independent.
- Page Objects should expose user-level actions and assertions, not raw locator usage in every test.
- Do not delete user-created scenarios or reports unless explicitly asked.
- Keep dashboard work separate unless the user specifically asks for dashboard maturity.
