# Test Workflow ve Kullanım Kılavuzu

## Hızlı Başlangıç

### Gerekli Servislerin Başlatılması

```bash
# Terminal 1: Mock API server
make mock

# Terminal 2: Appium server
make appium
```

### Test Çalıştırma

```bash
# Tüm testleri çalıştır
make test

# Android testleri
make test-android

# API testleri
make test-api

# Smoke testleri
make test-smoke

# Belirli bir test dosyası
pytest tests/android/login/test_TC001_valid_login.py -v
```

## Test Yazma Process

### Adım 1: BDD Senaryosu Oluştur

`test-scenarios/TS-0001-LOGIN/` klasöründe yeni bir dosya oluştur:

```markdown
# TC-000X: Yeni Test Senaryosu

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

Automation: tests/android/login/test_TC00X.py
```

### Adım 2: Test Kodu Yaz

`tests/android/login/` klasöründe Python testi oluştur:

```python
import pytest

class TestTC00X:
    @pytest.mark.smoke
    @pytest.mark.login
    def test_scenario(self, driver):
        from tests.page_objects.login_page import LoginPage
        login_page = LoginPage(driver)
        login_page.login("testuser", "password123")
        assert HomePage(driver).is_home_screen_visible()
```

### Adım 3: Çalıştır ve Raporu İncele

```bash
make test-android
# Rapor: reports/$(date +%Y-%m-%d)/report.html
```

## Makefile Komutları

| Komut | Açıklama |
|-------|----------|
| `make mock` | Mock API server'ı başlat (port 8080) |
| `make appium` | Appium server'ı başlat (port 4723) |
| `make test` | Tüm testleri çalıştır |
| `make test-android` | Sadece Android testlerini çalıştır |
| `make test-api` | Sadece API testlerini çalıştır |
| `make test-smoke` | Smoke testleri çalıştır |
| `make clean` | Cache ve report klasörlerini temizle |
| `make report` | En son raporu aç |

## Test Çaplama

### Test Tag'leri

```python
@pytest.mark.smoke      # Kritik testler
@pytest.mark.login      # Kategori: Login
@pytest.mark.regression # Kategori: Regression
@pytest.mark.android    # Platform: Android
@pytest.mark.api        # Platform: API
```

### Tag ile Çalıştırma

```bash
# Sadece smoke testleri
pytest -m smoke

# Login kategorisi
pytest -m login

# Android testleri + smoke
pytest -m "android and smoke"
```

## Hata Ayıklama

### Appium Bağlantı Sorunu

```bash
# Port kontrolü
lsof -i :4723

# Appium restart
pkill -f appium
appium --port 4723 --log-level error
```

### Mock Server Sorunu

```bash
# Port kontrolü
lsof -i :8080

# Server restart
pkill -f "mock_api_server.py"
python3 mock_api_server.py
```

### Element Bulunamadı

```python
# Hata anında sayfa kaynağını yazdır
print(driver.page_source)

# Screenshot al
driver.save_screenshot("reports/current/error.png")
```

## CI/CD Entegrasyonu

```bash
# Test çalıştır
pytest tests/ -v --html=reports/report.html --self-contained-html

# Exit code kontrolü (pytest dönüş kodu)
echo $?  # 0 = success, 1 = failure
```
