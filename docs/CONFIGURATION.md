# Konfigürasyon ve Ayarlar

## Proje Konfigürasyonu

### pytest.ini

Test framework ayarları:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    smoke: smoke test
    login: login test
    regression: regression test
```

### Mock API Server Ayarları

`mock_api_server.py` - Flask sunucusu için ayarlar:

```python
HOST = '0.0.0.0'
PORT = 8080
DEBUG = False
```

**Endpoints:**
- `POST /api/login` - Kullanıcı girişi
- `GET /api/user` - Kullanıcı bilgileri
- `POST /api/logout` - Oturum kapatma

### Dashboard App Ayarları

`dashboard-app/app.py` - Dashboard web sunucusu:

```python
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False
```

**API Endpoints:**
- `GET /` - Dashboard ana sayfa
- `GET /api/status` - Sistem durumu
- `GET /api/tests` - Mevcut test listesi
- `POST /api/run-test` - Test çalıştır
- `GET /api/log` - Test logları
- `GET /api/emulator/screenshot` - Emülatör ekran görüntüsü
- `GET /api/reports/latest` - En son rapor

## Servis Portları

| Servis | Port | Açıklama |
|--------|------|----------|
| Mock API Server | 8080 | REST API simülasyonu |
| Appium Server | 4723 | Mobil UI testleri |
| Dashboard App | 5000 | Web dashboard |

## Environment Variables

```bash
# Optional: Dashboard port
export PORT=5000

# Optional: Mock API port
export MOCK_API_PORT=8080

# Optional: Appium port
export APPIUM_PORT=4723
```

## Test Configuration

### Test Data

Test verileri hardcoded değildir. Test senaryoları `test-scenarios/` klasöründe plain English yazılır.

### Test Execution

```python
# conftest.py - Ortak fixture'lar
@pytest.fixture
def driver():
    """Appium driver fixture"""
    driver = webdriver.Remote(
        command_executor='http://localhost:4723',
        desired_capabilities=DESIRED_CAPABILITIES
    )
    yield driver
    driver.quit()
```

## Rapor Ayarları

### Rapor Konumu

```
reports/
└── YYYY-MM-DD/           ← Tarih klasörü
    ├── report.html       ← HTML rapor
    └── screenshots/      ← Ekran görüntüleri
        ├── screenshot_*.png
        └── emulator_live.png
```

### Screenshot Naming

```
screenshot_{test_name}_{YYYYMMDD_HHMMSS}.png
```

Örnek: `screenshot_test_valid_login_20260501_143025.png`

## CI/CD için Ayarlar

```yaml
# .github/workflows/test.yml (örnek)
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v --html=reports/report.html
```
