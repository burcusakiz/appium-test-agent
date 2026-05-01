# Proje Mimarisi

## Genel Bakış

Appium Test Agent, mobil uygulama (Android) ve REST API testlerini otomatikleştiren bir BDD (Behavior-Driven Development) test framework'udur.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Test Layer                              │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │   Appium Tests  │    │   API Tests     │                    │
│  │  (UI - Android) │    │ (REST - Flask)  │                    │
│  └────────┬────────┘    └─────────────────┘                    │
│           │                                                     │
│  ┌────────▼────────┐                                            │
│  │   Page Objects  │                                            │
│  │   (POM Pattern) │                                            │
│  └────────┬────────┘                                            │
│           │                                                     │
│  ┌────────▼────────┐    ┌─────────────────┐                    │
│  │   Appium Driver │    │   Requests      │                    │
│  └────────┬────────┘    └─────────────────┘                    │
│           │                                                     │
│  ┌────────▼──────────────────────────────┐                     │
│  │         Test Runner (pytest)          │                     │
│  └────────────────┬──────────────────────┘                     │
│                   │                                             │
│         ┌─────────▼──────────┐                                  │
│         │   HTML Reports     │                                  │
│         └────────────────────┘                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Dizin Yapısı

```
docs/
├── ARCHITECTURE.md      ← Bu dosya - Mimarisi ve yapı
├── WORKFLOW.md          ← Test yazma ve çalıştırma workflow'u
└── CONFIGURATION.md     ← Konfigürasyon detayları

apps/                    ← APK dosyaları (runtime'da kullanılır)
mock_api_server.py       ← Flask tabanlı mock REST API
test-scenarios/          ← BDD senaryoları (human-readable)
tests/                   ← Test otomasyon kodları
├── android/            ← Android UI testleri
├── api/                ← REST API testleri
└── page_objects/       ← Page Object Model sınıfları
```

## Bileşenler

### 1. Mock API Server (`mock_api_server.py`)
- Flask tabanlı REST API simülasyonu
- Port: 8080
- Endpoints:
  - `POST /api/login` - Kullanıcı authentication
  - `GET /api/user` - Kullanıcı bilgileri
  - `POST /api/logout` - Oturum kapatma

### 2. Appium Driver
- Android uygulamalarını test etmek için Appium kullanır
- Port: 4723
- Uyumluluk: Appium Server 2.x

### 3. Page Object Model (POM)
- Kod tekrarını azaltır
- Okunabilirliği artırır
- Bakım kolaylığı sağlar

```python
# Örnek: Login Page Object
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
    
    def login(self, username, password):
        self._enter_username(username)
        self._enter_password(password)
        self._tap_login_button()
```

### 4. Test Runner (pytest)
- Test discovery ve çalıştırma
- HTML rapor üretimi
- Fixture yönetimi (`conftest.py`)

## Test Çalışma Akışı

```
1. Mock Server Başlatılır
   ↓
2. Appium Server Başlatılır
   ↓
3. Test Senaryosu Seçilir (test-scenarios/)
   ↓
4. Test Kodu Çalıştırılır (pytest)
   ↓
5. Sonuç Raporlanır (reports/YYYY-MM-DD/)
```

## Raporlama

Her test çalıştırmasından sonra otomatik olarak:
- HTML rapor: `reports/YYYY-MM-DD/report.html`
- Screenshot: `reports/YYYY-MM-DD/screenshots/`

## Teknolojiler

| Kategori | Tech |
|----------|------|
| Testing Framework | Pytest |
| Mobile Testing | Appium Python Client |
| API Testing | Requests |
| Web Framework (Mock) | Flask |
| Reporting | pytest-html |
