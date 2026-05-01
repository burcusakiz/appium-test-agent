# LoginApp Android App

## Package
`com.demo.loginapp`

## Valid Credentials
- Username: `testuser`
- Password: `password123`

## Element IDs
| Element | ID |
|---------|-----|
| Title | `textViewTitle` |
| Username Input | `username_input` |
| Password Input | `password_input` |
| Login Button | `login_button` |
| Error Message | `textViewError` |
| Welcome Text | `textViewWelcome` |
| Logout Button | `buttonLogout` |

## Build Instructions

### Using Android Studio
1. Open Android Studio
2. Select "Open an existing project"
3. Navigate to this directory and click "Open"
4. Wait for Gradle sync to complete
5. Build → Build Bundle(s) / APK(s) → Build APK(s)

### Using Gradle (CLI)
```bash
# Build debug APK
./gradlew assembleDebug

# Build release APK
./gradlew assembleRelease

# Install to connected device
./gradlew installDebug

# Run tests
./gradlew test
```

### Output
- Debug APK: `app/build/outputs/apk/debug/app-debug.apk`
- Release APK: `app/build/outputs/apk/release/app-release.apk`

## Deploy to Device
```bash
# Using ADB
adb install app/build/outputs/apk/debug/app-debug.apk

# Uninstall
adb uninstall com.demo.loginapp
```

## Activity Structure
- **LoginActivity**: Login screen with username/password fields
- **HomeActivity**: Welcome screen with logout functionality
