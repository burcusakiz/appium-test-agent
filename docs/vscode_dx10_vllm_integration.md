# VS Code + Claude Code + DX10 vLLM Entegrasyon Kılavuzu

Bu doküman MacBook üzerinde çalışan VS Code / Claude Code ortamının, DX10 üzerindeki Docker vLLM servisinde çalışan Qwen3-Coder-Next modeline bağlanmasını ve bu projedeki Claude Code Skill, Agent ve Command workflow'larının nasıl kullanılacağını anlatır.

## Hedef

Amaç şu akışı kurmaktır:

1. İnsan önce test senaryosunu Claude Code'a yazdırır.
2. Claude Code bu senaryoyu Appium pytest otomasyon koduna çevirir.
3. Testler Android emulator veya cihaz üzerinde çalıştırılır.
4. Sonuçlar `reports/YYYY-MM-DD/` altında üretilir.
5. Hata varsa Claude Code test raporu, screenshot ve kodu analiz ederek otomasyon hatasını düzeltir.

Bu projede Claude Code varlıkları proje içinde tutulur:

```text
.claude/
├── agents/
│   ├── appium-automation-engineer.md
│   ├── scenario-author.md
│   └── test-runner-debugger.md
├── commands/
│   ├── automate-mobile-scenario.md
│   ├── create-mobile-scenario.md
│   ├── fix-failing-mobile-test.md
│   └── run-mobile-tests.md
└── skills/
    └── mobile-test-agent/
        ├── SKILL.md
        └── references/
```

## Mimari

```text
MacBook
├── VS Code
│   ├── Claude Code Extension
│   │   └── ANTHROPIC_BASE_URL=http://192.168.1.21:8000
│   └── Continue Extension
│       └── apiBase=http://192.168.1.21:8000/v1
└── Terminal
    └── claude-gx10 alias
        └── claude CLI

DX10
└── Docker
    └── vllm/vllm-openai:cu130-nightly
        └── Qwen3-Coder-Next FP8
            └── served-model-name=claude-sonnet-4-6
```

Önemli fark:

- Continue, OpenAI uyumlu `/v1` endpoint kullanır.
- Claude Code için `ANTHROPIC_BASE_URL` değeri `http://192.168.1.21:8000` olarak verilir; `/v1` eklenmez.

## DX10 vLLM Servisini Çalıştırma

Mevcut komut çalışır durumdaysa model bağlantısı açısından doğru. Ancak LAN içinde endpoint'in korumasız kalmaması için `--api-key local-key` eklenmesi önerilir. MacBook tarafında zaten `ANTHROPIC_API_KEY=local-key` ve Continue tarafında `apiKey: local-key` kullanıldığı için bu değişiklik ayarlarla uyumludur.

Önerilen güncel komut:

```bash
docker run -d \
  --name vllm-coder-next \
  --restart unless-stopped \
  --runtime=nvidia \
  --gpus all \
  --ipc=host \
  -e HF_HUB_DISABLE_XET=1 \
  -v ~/models/qwen3-coder-next-fp8:/model \
  -p 0.0.0.0:8000:8000 \
  vllm/vllm-openai:cu130-nightly \
  --model /model \
  --served-model-name claude-sonnet-4-6 \
  --api-key local-key \
  --gpu-memory-utilization 0.80 \
  --max-model-len 131072 \
  --max-num-batched-tokens 65536 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --enable-prefix-caching \
  --language-model-only
```

`--served-model-name claude-sonnet-4-6` değeri bilinçli olarak Anthropic model adı gibi seçilmiştir. Claude Code MacBook tarafında Sonnet model alias'ını çağırır; DX10 tarafında vLLM bu adı local Qwen modeline map eder.

## Mevcut Container'ı Güncelleme

Docker container oluşturulduktan sonra run komutu değiştirilemez. `--api-key local-key` eklemek için container'ı yeniden oluşturmak gerekir:

```bash
docker stop vllm-coder-next
docker rm vllm-coder-next
```

Sonra yukarıdaki güncel `docker run` komutunu çalıştır.

Logları izlemek için:

```bash
docker logs -f vllm-coder-next
```

Claude Code'dan prompt gönderdiğinde bu loglarda request görüyorsan trafik DX10'a gidiyor demektir.

## DX10 Servis Testi

API key eklediysen:

```bash
curl -H "Authorization: Bearer local-key" \
  http://192.168.1.21:8000/v1/models
```

API key eklemediysen:

```bash
curl http://192.168.1.21:8000/v1/models
```

Beklenen model adlarından biri:

```text
claude-sonnet-4-6
```

## macOS Local Network İzni

VS Code'un LAN üzerindeki DX10 servisine erişebilmesi için:

```text
System Settings -> Privacy & Security -> Local Network
Visual Studio Code.app = ON
```

Bu kapalıysa terminalde `curl` çalışırken VS Code extension bağlantısı başarısız olabilir.

## Terminal Alias

MacBook üzerinde Claude Code CLI'ı DX10'a yönlendirmek için:

```bash
alias claude-gx10='
  export CLAUDE_CONFIG_DIR=~/.claude-gx10
  export ANTHROPIC_BASE_URL=http://192.168.1.21:8000
  export ANTHROPIC_API_KEY=local-key
  export ANTHROPIC_AUTH_TOKEN=local-key
  export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6
  export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-sonnet-4-6
  export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-sonnet-4-6
  echo "🟢 Qwen3-Coder-Next @ GX10"
  claude
'
```

Kullanım:

```bash
cd /Users/semih.sakiz/DEVELOPER/appium-test-agent
claude-gx10
```

`CLAUDE_CONFIG_DIR=~/.claude-gx10` sadece user-level Claude Code ayarlarını değiştirir. Proje içindeki `.claude/skills`, `.claude/agents`, `.claude/commands` ve `CLAUDE.md` yine bu repo kökünden okunur.

## VS Code Claude Code Extension Ayarı

VS Code `settings.json` içinde:

```json
{
  "claudeCode.preferredLocation": "panel",
  "claudeCode.environmentVariables": {
    "CLAUDE_CONFIG_DIR": "/Users/semih.sakiz/.claude-gx10",
    "ANTHROPIC_BASE_URL": "http://192.168.1.21:8000",
    "ANTHROPIC_API_KEY": "local-key",
    "ANTHROPIC_AUTH_TOKEN": "local-key",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-sonnet-4-6"
  }
}
```

VS Code workspace root şu dizin olmalıdır:

```text
/Users/semih.sakiz/DEVELOPER/appium-test-agent
```

Workspace root yanlışsa proje `.claude/` dosyaları bulunmayabilir.

## Continue Config

`~/.continue/config.yaml` içinde:

```yaml
models:
  - name: Qwen3-Coder-Next (GX10)
    provider: vllm
    model: claude-sonnet-4-6
    apiBase: http://192.168.1.21:8000/v1
    apiKey: local-key
```

## Claude Code Skill, Agent ve Command Doğrulama

Claude Code terminalinde:

```text
List available skills and project agents.
```

Beklenen skill:

```text
mobile-test-agent
```

Beklenen project agents:

```text
scenario-author
appium-automation-engineer
test-runner-debugger
```

Project commands listesini görmek için:

```text
What project commands are available?
```

Beklenen commands:

```text
/create-mobile-scenario
/automate-mobile-scenario
/run-mobile-tests
/fix-failing-mobile-test
```

Bu çıktı geliyorsa local Qwen/vLLM bağlantısı ile Claude Code proje varlıkları birlikte çalışıyor demektir.

## Mobil Test Agent Kullanım Akışı

### 1. İnsan Okunabilir Senaryo Oluştur

```text
/create-mobile-scenario login ekranında boş username ve dolu password ile negatif test senaryosu oluştur
```

Beklenen çıktı:

```text
test-scenarios/TS-0001-LOGIN/TC-000X-....md
```

Senaryo formatı:

```markdown
# TC-000X: Empty Username

App: com.demo.loginapp
Suite: TS-0001-LOGIN
Priority: Medium

Steps:
1. Launch the application
2. Enter password: password123
3. Leave username empty
4. Tap the Login button

Expected:
User remains on login screen. Error message is displayed.

Automation: tests/android/login/test_TC00X_empty_username.py
```

### 2. Senaryoyu Appium pytest Koduna Çevir

```text
/automate-mobile-scenario TC-000X
```

veya dosya yoluyla:

```text
/automate-mobile-scenario test-scenarios/TS-0001-LOGIN/TC-000X-empty-username.md
```

Beklenen çıktı:

```text
tests/android/login/test_TC00X_empty_username.py
```

Otomasyon agent'ı şu kuralları izler:

- Page Object Pattern kullanır.
- Test kodunu `tests/` altında üretir.
- Ortak ekran davranışlarını `tests/page_objects/` içine koyar.
- Raw locator kullanımını test dosyalarına yaymaz.
- `pytest` marker'larını ekler.

### 3. Testi Çalıştır

Tek test:

```text
/run-mobile-tests tests/android/login/test_TC00X_empty_username.py
```

Android suite:

```text
/run-mobile-tests --platform android
```

Smoke testleri:

```text
/run-mobile-tests --platform android -m smoke
```

CLI üzerinden doğrudan:

```bash
python3 run_tests.py tests/android/login/test_TC00X_empty_username.py
python3 run_tests.py --platform android
python3 run_tests.py --platform android -m smoke
```

Rapor:

```text
reports/YYYY-MM-DD/report.html
```

Failure screenshot:

```text
reports/YYYY-MM-DD/screenshots/
```

### 4. Hata Analizi ve Fix

```text
/fix-failing-mobile-test tests/android/login/test_TC00X_empty_username.py
```

Bu command şu sırayı izler:

1. İlgili test ve senaryoyu okur.
2. Latest report ve screenshot klasörünü kontrol eder.
3. Hatayı sınıflandırır:
   - ortam hatası
   - ürün/app davranışı hatası
   - otomasyon kodu hatası
4. Senaryo beklentisi doğruysa otomasyon kodunu düzeltir.
5. En küçük ilgili testi tekrar çalıştırır.

## Appium ve Mock API Servisleri

Android UI testleri için:

```bash
make appium
```

Mock API için:

```bash
make mock
```

Tüm servisleri başlatmak için:

```bash
make start-servers
```

Servisleri durdurmak için:

```bash
make stop-servers
```

Port kontrolleri:

```bash
lsof -i :4723
lsof -i :8080
```

## Raporlama

Test runner raporları tarih bazlı üretir:

```text
reports/
└── YYYY-MM-DD/
    ├── report.html
    └── screenshots/
```

API testlerini HTML raporla çalıştırmak için:

```bash
python3 run_tests.py --platform api --html
```

Android testlerini collect-only kontrol etmek için:

```bash
python3 run_tests.py --platform android --extra --collect-only
```

## Model Adı ve Billing Görünümü

Claude Code terminalinde şuna benzer bir başlık görünebilir:

```text
Sonnet 4.6 · API Usage Billing
```

Bu başlık yanıltıcı olabilir. `ANTHROPIC_BASE_URL` DX10 vLLM endpoint'ine yönlendirildiği için gerçek request'in nereye gittiğini DX10 loglarından doğrula:

```bash
docker logs -f vllm-coder-next
```

Prompt gönderildiğinde log akıyorsa istek DX10 local vLLM servisine gidiyor demektir.

## Troubleshooting

### Claude Code proje command'larını görmüyor

Kontrol et:

```bash
pwd
ls -la .claude
find .claude -maxdepth 3 -type f
```

Claude Code şu dizinden açılmalıdır:

```bash
cd /Users/semih.sakiz/DEVELOPER/appium-test-agent
claude-gx10
```

### vLLM cevap vermiyor

DX10 üzerinde:

```bash
docker ps
docker logs -f vllm-coder-next
```

MacBook üzerinde:

```bash
curl -H "Authorization: Bearer local-key" \
  http://192.168.1.21:8000/v1/models
```

### VS Code bağlanıyor ama terminal bağlanmıyor

Terminal alias içindeki env değerlerini kontrol et:

```bash
env | grep ANTHROPIC
env | grep CLAUDE_CONFIG_DIR
```

### Terminal bağlanıyor ama VS Code bağlanmıyor

Kontrol et:

- VS Code `settings.json` içinde `claudeCode.environmentVariables` doğru mu?
- macOS Local Network izni açık mı?
- VS Code workspace root repo kökü mü?
- DX10 IP adresi değişti mi?

### Tool call veya file edit davranışı zayıf

Qwen/vLLM tarafında şu parametreler kritik:

```text
--enable-auto-tool-choice
--tool-call-parser qwen3_coder
```

Bu parametreler yoksa model konuşabilir ama Claude Code tool çağrılarını güvenilir üretmeyebilir.

## Kısa Komut Özeti

DX10:

```bash
docker logs -f vllm-coder-next
```

MacBook terminal:

```bash
cd /Users/semih.sakiz/DEVELOPER/appium-test-agent
claude-gx10
```

Claude Code:

```text
List available skills and project agents.
What project commands are available?
/create-mobile-scenario ...
/automate-mobile-scenario TC-000X
/run-mobile-tests tests/android/login/test_TC00X_name.py
/fix-failing-mobile-test tests/android/login/test_TC00X_name.py
```

Pytest:

```bash
python3 run_tests.py --platform android --extra --collect-only
python3 run_tests.py --platform api --html
```
