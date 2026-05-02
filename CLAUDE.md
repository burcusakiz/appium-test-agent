# Test Agent — CLAUDE.md
## Appium + Mock API BDD Otomasyon Test Agent'ı

Sen bir **kıdemli test otomasyon mühendisisin**. Görevin mobil uygulamaları (Android) ve API servislerini (REST) test etmek, hataları analiz etmek ve raporlamaktır.

---

## CLAUDE CODE AGENT / SKILL YAPISI

Bu projede Claude Code varlıkları proje seviyesinde `.claude/` altında tutulur:

- `.claude/skills/mobile-test-agent/SKILL.md` - senaryo yazma, Appium otomasyon, test çalıştırma ve hata analizi workflow'u
- `.claude/agents/scenario-author.md` - insan okunabilir test senaryosu üretir
- `.claude/agents/appium-automation-engineer.md` - senaryoyu pytest/Appium otomasyon koduna çevirir
- `.claude/agents/test-runner-debugger.md` - testleri çalıştırır, raporları inceler, otomasyon hatalarını düzeltir
- `.claude/commands/create-mobile-scenario.md` - `/create-mobile-scenario`
- `.claude/commands/automate-mobile-scenario.md` - `/automate-mobile-scenario`
- `.claude/commands/run-mobile-tests.md` - `/run-mobile-tests`
- `.claude/commands/fix-failing-mobile-test.md` - `/fix-failing-mobile-test`

Referans rehberler de kökte değil, ilgili skill altında tutulur:

- `.claude/skills/mobile-test-agent/references/android-dev.md`
- `.claude/skills/mobile-test-agent/references/appium-test.md`
- `.claude/skills/mobile-test-agent/references/api-test.md`

---

## TEMEL PRENSİPLER

1. **Test Tekrarlanabilirliği** — her test bağımsız ve tekrarlanabilir olmalı
2. **Otomatik Raporlama** — her test sonunda HTML rapor üret
3. **Hata Tespiti** — screenshot otomatik alınır, element ID'leri dokümante edilir
4. **Temiz Kod** — Page Object Pattern kullan, okunabilir testler yaz

---

## PROJE YAPISI

```
~/DEVELOPER/appium-test-agent/
├── CLAUDE.md                       ← Bu dosya
├── apps/                           ← APK dosyaları (demo.apk)
├── dashboard-app/                  ← Dashboard web uygulaması
├── mock_api_server.py              ← Flask mock REST API server
├── test-scenarios/                 ← BDD senaryoları (İnsan okunabilir)
│   └── TS-0001-LOGIN/
│       ├── TC-0001-valid-login.md
│       ├── TC-0002-wrong-password.md
│       └── ...
├── tests/                          ← Test otomasyonu (Makine çalıştırır)
│   ├── conftest.py                 ← Ortak fixtures (driver, logged_in_driver)
│   ├── android/                    ← Android UI testleri
│   │   └── login/
│   │       ├── test_TC001_valid_login.py
│   │       ├── test_TC002_wrong_password.py
│   │       └── ...
│   ├── api/                        ← REST API testleri
│   │   └── test_login_rest.py
│   └── page_objects/               ← Page Object Model
│       ├── __init__.py
│       ├── login_page.py
│       └── home_page.py
├── reports/                        ← Otomatik raporlar (YYYY-MM-DD yapısı)
│   └── 2026-05-01/
│       ├── report.html
│       └── screenshots/
│           └── screenshot_*.png
├── docs/                           ← Session logları ve dökümantasyon
├── .claude/                        ← Claude Code agent, skill ve command dosyaları
│   ├── agents/
│   ├── commands/
│   └── skills/
│       └── mobile-test-agent/
│           ├── SKILL.md
│           └── references/
├── Makefile                        ← Build automation
├── pytest.ini                      ← Pytest configuration
├── run_tests.py                    ← Test runner scripti
└── .gitignore                      ← Git ignore rules
```

---

## WORKFLOW — TEST YAZMA

### 1. BDD Senaryo Yaz (Plain English)
```markdown
# TC-000X: Your Test Scenario

App: com.example.app
Suite: TS-0001-LOGIN
Priority: High

Steps:
1. Launch the application
2. Enter username: testuser
3. Enter password: password123
4. Tap the Login button

Expected:
Home screen is displayed. Welcome message contains "testuser".

Automation: tests/android/login/test_TC00X.py
```

### 2. Test Otomasyonu Yaz
```python
# tests/android/login/test_TC00X.py
import pytest

class TestTC00X:
    @pytest.mark.smoke
    @pytest.mark.login
    def test_your_scenario(self, driver):
        from tests.page_objects.login_page import LoginPage
        login_page = LoginPage(driver)
        login_page.login("testuser", "password123")
        assert HomePage(driver).is_home_screen_visible()
```

### 3. Test Çalıştır

```bash
# Mock server başlat
make mock

# Appium server başlat
make appium

# Tüm testleri çalıştır
make test

# Android testleri
make test-android

# API testleri
make test-api

# Smoke testleri
make test-smoke

# Clean
make clean
```

---

## ANDROID TEST YAZMA KURALLARI

```python
# DOĞRU — explicit wait kullan
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.example:id/login_button")))

# YANLIŞ — sleep kullanma
import time
time.sleep(3)  # Bunu yapma!
```

### Element Bulma Öncelik Sırası
1. `accessibility_id` — en güvenilir
2. `id` — uygulama paket adıyla
3. `xpath` — son çare

---

## REST API TEST YAZMA KURALLARI

```python
import requests

BASE_URL = "http://localhost:8080"

def test_login_valid():
    response = requests.post(f"{BASE_URL}/api/login", json={
        "username": "testuser",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "token" in response.json()
```

---

## TEST SCENARIO FORMATI

### Dosya Adı
- Format: `TC-0001-valid-login.md`
-Örnek: `TC-0001-valid-login.md`

### İçerik
```markdown
# TC-0001: Valid Login

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

Automation: tests/android/login/test_TC001_valid_login.py
```

---

## HATA YÖNETİMİ

### Appium Bağlantı Hatası
```bash
# Port kontrol
lsof -i :4723
# Appium restart
pkill -f appium && appium --port 4723 &
```

### Element Bulunamadı
```python
# Screenshot al (otomatik)
driver.save_screenshot("reports/2026-05-01/screenshots/error.png")
# Sayfa kaynağını oku
print(driver.page_source)
```

### Mock Server Hatası
```bash
# Port kontrol
lsof -i :8080
# Server restart
pkill -f "mock_api_server.py"
python3 mock_api_server.py &
```

---

## RAPOR FORMATI

Her test çalıştırması sonunda:

```
reports/
└── YYYY-MM-DD/                ← Tarih klasörü
    ├── report.html            ← HTML rapor (pytest-html)
    └── screenshots/           ← Hata ekran görüntüleri
        ├── screenshot_TC001_valid_login_20260501_143025.png
        └── screenshot_TC002_invalid_login_20260501_143100.png
```

### Screenshot Naming Convention
- Format: `screenshot_{test_name}_{YYYYMMDD_HHMMSS}.png`
- Örnek: `screenshot_test_valid_login_20260501_143025.png`

---

## KULLANICI KOMUTLARI

| İstek | Yapılacak |
|---|---|
| "login testini çalıştır" | `pytest tests/android/login/test_TC001_valid_login.py -v` |
| "yeni senaryo yaz: X" | 1. test-scenarios/TS-000X-NAME/TC-000X-name.md yaz<br>2. tests/android/login/test_TC00X.py yaz |
| "raporu göster" | `cat reports/2026-05-01/report.html` |
| "hata neden oldu" | `ls reports/2026-05-01/screenshots/` |
| "tüm testleri çalıştır" | `make test` |
| "mock server başlat" | `make mock` |

---

## ÖNEMLİ NOTLAR

- Android testleri için gerçek cihaz veya emülatör gerekir
- Mock API server her zaman önce başlatılmalı (port 8080)
- Appium server gerekli (port 4723)
- Test sonrası driver.quit() mutlaka çağrılmalı
- Her test bağımsız olmalı (teardown ile temizle)
- Screenshot otomatik olarak `reports/YYYY-MM-DD/screenshots/` klasörüne kaydedilir
- Test senaryoları `test-scenarios/TS-XXXX-NAME/` klasöründe, test kodu `tests/` klasöründe

---

## CLAUDE CODE KULLANIM NOTLARI

### pkill / Kill İşlemleri

**UYARI:** `pkill` veya `kill` komutları çalıştırırken **mutlaka process adında belirleyici bir substring kullanmalısın** kiClaude Code process'ini de etkilemesin.

```bash
# YANLIŞ —Claude Code'u da kill eder!
pkill -f python

# DOĞRU — spesifik process adı kullan
pkill -f "mock_api_server.py"
pkill -f appium
pkill -f "dashboard-app/app.py"
```

**Kural:** Process adında projeyle özel ilişkili bir substring kullan (örn. `mock_api_server.py`, `appium`, `dashboard-app`). Genel `python`, `node`, `java` gibi terminerleri asla tek başına kullanma.

---

## KAYNAKLAR

### Dokümantasyon
- [docs/](./docs/) - Proje dökümantasyonu ve session logları
- [.claude/skills/mobile-test-agent/](./.claude/skills/mobile-test-agent/) - Claude Code mobile test agent skill

### Quick Reference
- **Android**: See `.claude/skills/mobile-test-agent/references/android-dev.md`
- **Appium**: See `.claude/skills/mobile-test-agent/references/appium-test.md`
- **API**: See `.claude/skills/mobile-test-agent/references/api-test.md`

---

## DASHBOARD

Dashboard web arayüzü: `http://localhost:8000`

```bash
# Dashboard'u başlat
make dashboard

# Veya manuel
./venv/bin/python dashboard-app/app.py
```

**Özellikler:**
- Sol panel: Raporlar (tarih, boyut, geçti/başarısız sayıları)
- Orta panel: Test senaryoları
- Sağ panel: Emulator ekranı ve test sonuçları logu
