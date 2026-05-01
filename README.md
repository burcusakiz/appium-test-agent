# Appium Test Agent

Mobil uygulama (Android) ve REST API testlerini otomatikleştiren BDD (Behavior-Driven Development) test framework'ü.

## Özellikler

- **Appium Integration** - Android UI testleri
- **REST API Testing** - Flask mock API ile testler
- **Page Object Model** - Temiz, Bakımı Kolay Kod
- **BDD Senaryoları** - Human-readable test senaryoları
- **Otomatik Raporlama** - HTML raporlar ve screenshot'lar
- **Dashboard** - Web tabanlı test kontrol paneli

## Proje Yapısı

```
appium-test-agent/
├── dashboard-app/              # Dashboard web uygulaması
├── docs/                       # Dokümantasyon
│   ├── ARCHITECTURE.md        # Mimarisi ve yapı
│   ├── WORKFLOW.md            # Test workflow
│   └── CONFIGURATION.md       # Konfigürasyon
├── mock_api_server.py          # Flask mock REST API
├── test-scenarios/             # BDD senaryoları
│   └── TS-0001-LOGIN/
├── tests/                      # Test otomasyonu
│   ├── android/               # Android UI testleri
│   ├── api/                   # REST API testleri
│   └── page_objects/          # Page Object Model
├── apps/                       # APK dosyaları (runtime)
├── reports/                    # Otomatik raporlar
├── skills/                     # Specialized skill guides
├── Makefile                    # Build automation
├── pytest.ini                  # Pytest configuration
├── run_tests.py                # Test runner script
└── requirements.txt            # Python dependencies
```

## Hızlı Başlangıç

### 1. Bağımlılıkları Kur

```bash
pip install -r requirements.txt
```

### 2. Servisleri Başlat

```bash
# Terminal 1: Mock API server
make mock

# Terminal 2: Appium server
make appium

# Terminal 3: Dashboard (isteğe bağlı)
cd dashboard-app && python app.py
```

### 3. Test Çalıştır

```bash
# Tüm testleri çalıştır
make test

# Android testleri
make test-android

# API testleri
make test-api

# Smoke testleri
make test-smoke
```

## Dokümantasyon

- [Mimarisi ve Yapı](docs/ARCHITECTURE.md) - Proje mimarisi ve bileşenler
- [Test Workflow](docs/WORKFLOW.md) - Test yazma ve çalıştırma
- [Konfigürasyon](docs/CONFIGURATION.md) - Ayarlar ve konfigürasyon

## Teknolojiler

| Kategori | Tech |
|----------|------|
| Testing Framework | Pytest |
| Mobile Testing | Appium Python Client |
| API Testing | Requests |
| Web Framework | Flask |
| Reporting | pytest-html |

## Gereksinimler

- Python 3.10+
- Appium Server 2.x
- Android SDK (emülatör veya cihaz)
- Flask

## Lisans

MIT
