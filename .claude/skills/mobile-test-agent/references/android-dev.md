# Android Development Skill Guide

**Purpose**: Android native application development, testing, and debugging

**When to use**: When working with Android APK files, native UI elements, device automation, or Android-specific features

---

## Core Principles

### 1. Android Activity Lifecycle
```kotlin
// Activity lifecycle order:
// onCreate() → onStart() → onResume() → onPause() → onStop() → onDestroy()
// onResume() is when the activity is interactive

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
    // Initialize views, bind data
}

override fun onResume() {
    super.onResume()
    // Refresh data, restart animations
}
```

### 2. Android Component Types
| Component | Purpose | Lifecycle |
|-----------|---------|-----------|
| Activity | Single screen with UI | Full lifetime |
| Service | Background operations | Started/Bound |
| BroadcastReceiver | System/application events | Temporary |
| ContentProvider | Data sharing between apps | System-managed |

---

## UI Development Best Practices

### Layout XML Patterns
```xml
<!-- Use ConstraintLayout for complex layouts -->
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <TextView
        android:id="@+id/textViewTitle"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Title"
        android:textSize="18sp"
        android:textColor="@android:color/black"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="16dp"/>

    <EditText
        android:id="@+id/editTextInput"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:hint="Enter text"
        app:layout_constraintTop_toBottomOf="@id/textViewTitle"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_margin="16dp"/>

</androidx.constraintlayout.widget.ConstraintLayout>
```

### View Binding (Type-safe view access)
```kotlin
// In Activity
private lateinit var binding: ActivityMainBinding

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    binding = ActivityMainBinding.inflate(layoutInflater)
    setContentView(binding.root)
    
    // Access views directly
    binding.textViewTitle.text = "Hello"
    binding.buttonSubmit.setOnClickListener { onSubmitClick() }
}
```

---

## Security Best Practices

### 1. Data Storage
| Storage Type | Use Case | Secure? |
|-------------|----------|---------|
| SharedPreferences | Small key-value pairs | No (encrypt!) |
| Internal Storage | Private app data | Yes |
| External Storage | Public data | No |
| SQLite Database | Structured data | Yes (with encryption) |
| EncryptedSharedPreferences | Small sensitive data | Yes |
| Keystore | Cryptographic keys | Yes |

### 2. Secure Data Handling
```kotlin
// Use EncryptedSharedPreferences for sensitive data
val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "secret_prefs",
    MasterKey.Builder(context, MasterKey.Keys.AES256_GCM)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build(),
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

// Write encrypted data
encryptedPrefs.edit().putString("api_token", token).apply()
```

### 3. Network Security
```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Allow cleartext traffic only for localhost (debug) -->
    <debug-overrides>
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </debug-overrides>
    
    <!-- Default to secure connections -->
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
</network-security-config>
```

---

## Testing Best Practices

### 1. Unit Testing (JUnit 5)
```kotlin
@ExtendWith(MockitoExtension::class)
class LoginViewModelTest {
    
    @Mock
    private lateinit var repository: AuthRepository
    
    @InjectMocks
    private lateinit var viewModel: LoginViewModel
    
    @Test
    fun `login with valid credentials returns success`() = runTest {
        coEvery { repository.login("user", "pass") } returns true
        
        viewModel.login("user", "pass")
        
        assertTrue(viewModel.isLoggedIn.value!!)
    }
}
```

### 2. UI Testing (Espresso)
```kotlin
@Test
fun loginSuccessful() {
    // Input credentials
    onView(withId(R.id.editTextUsername))
        .perform(typeText("testuser"), closeSoftKeyboard())
    onView(withId(R.id.editTextPassword))
        .perform(typeText("password123"), closeSoftKeyboard())
    
    // Click login
    onView(withId(R.id.buttonLogin)).perform(click())
    
    // Verify navigation to home screen
    onView(withId(R.id.textViewWelcome))
        .check(matches(isDisplayed()))
        .check(matches(withText("Welcome, testuser")))
}
```

### 3. Instrumented Test Setup
```kotlin
@AndroidEntryPoint
class BaseTest {
    @Rule
    @JvmField
    var activityRule = activityScenarioRule<MainActivity>()
}

@RunWith(AndroidJUnit4::class)
class LoginInstrumentedTest : BaseTest() {
    @Test
    fun testUserCanLogin() {
        // Your test code
    }
}
```

---

## Appium Integration

### Finding Elements (Priority Order)
```python
# Appium element location priority:
# 1. accessibility_id (most reliable)
# 2. id (using resource-id)
# 3. xpath (use sparingly - slower)

# Android examples:
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "login_button")
driver.find_element(AppiumBy.ID, "com.app:id/login_button")
driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='Login']")
```

### Expected Conditions
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)

# Wait for element to be present
element = wait.until(EC.presence_of_element_located((AppiumBy.ID, "element_id")))

# Wait for element to be clickable
button = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "button_id")))

# Wait for element to be visible
title = wait.until(EC.visibility_of_element_located((AppiumBy.ID, "title_id")))
```

### Common Android Capabilities
```python
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "14.0"
options.device_name = "emulator-5554"
options.app_package = "com.example.app"
options.app_activity = "com.example.app.MainActivity"
options.no_reset = False  # Set True to keep app state
options.auto_grant_permissions = True
options.new_command_timeout = 300
options.automation_name = "UiAutomator2"
```

---

## Performance Optimization

### 1. Layout Performance
- Use `ConstraintLayout` over nested layouts
- Avoid `include` with `merge` for complex layouts
- Use `ViewStub` for optional UI elements
- Use `merge` tags to reduce view hierarchy depth

### 2. Memory Management
```kotlin
// Use WeakReference for callbacks
class MyCallback(weakActivity: Activity) : Callback {
    private val activityRef = WeakReference(weakActivity)
    
    override fun onClick(v: View?) {
        val activity = activityRef.get()
        if (activity != null && !activity.isFinishing) {
            // Safe to use activity
        }
    }
}

// Recycle bitmaps
bitmap.recycle()
bitmap = null
```

### 3. Threading
```kotlin
// Use Coroutines for background work
class MyRepository(private val ioDispatcher: CoroutineDispatcher) {
    suspend fun loadData(): List<Data> = withContext(ioDispatcher) {
        // Background work here
        api.loadData()
    }
}

// In ViewModel
viewModelScope.launch {
    val data = repository.loadData()
    _data.value = data
}
```

---

## Debugging Commands

```bash
# View logcat
adb logcat -s AndroidRuntime:E

# View layout hierarchy
adb shell dumpsys window | grep -E "mCurrentFocus|mFocusedApp"

# Take screenshot
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png

# Record screen
adb shell screenrecord /sdcard/demo.mp4
adb pull /sdcard/demo.mp4

# Get app info
adb shell dumpsys package com.example.app | grep -E "package|version"

# Clear app data
adb shell pm clear com.example.app

# Install app
adb install -r app-release.apk

# Uninstall app
adb uninstall com.example.app
```

---

## Production Checklist

- [ ] Use ProGuard/R8 for code obfuscation
- [ ] Enable Firebase Crashlytics
- [ ] Configure proper signing keys
- [ ] Set up App Center or Firebase App Distribution
- [ ] Enable data protection in AndroidManifest
- [ ] Test on multiple screen sizes
- [ ] Verify dark theme support
- [ ] Check battery optimization handling
- [ ] Test on Android 10+ (scoped storage)
- [ ] Verify backup settings

---

## References

- [Android Developer Docs](https://developer.android.com/guide)
- [Material Design](https://m3.material.io/)
- [Appium Docs](https://appium.io/docs/)
- [Espresso Cheat Sheet](https://android.googlesource.com/platform/frameworks/testing/+/androidx-test-master/espresso/cheat_sheet/EspressoCheatSheet.md)
