# Teknoloji Yığını Tablosu (Hafta 2)

**Durum:** ÖNERİ, ONAYLANMADI. Kaynaklar: teslim edilen öneri formu, depo yapılandırması (`pyproject.toml`, `.github/workflows/ci.yml`, `requirements/*`, `.env.example`), bu çalışmanın doğrulamaları.

**Durum kodları:** **TAAHHÜT** = öneri formunda yazılı · **ÖNERİ** = bu çalışmada önerilen, onay bekliyor · **DOĞRULANDI** = bu makinede çalıştırılıp test edildi (kapsam notlu) · **SEÇİLMEDİ** = henüz karar yok (uydurma sürüm yazılmadı) · **MEVCUT** = depoda zaten tanımlı.

| Katman | Teknoloji | Rolü | Durum | Sürüm / kanıt | Değerlendirilen alternatif | Karar kimliği |
| --- | --- | --- | --- | --- | --- | --- |
| İstemci | React | 6 ekranlı tek sayfa uygulaması | TAAHHÜT | derleme aracı, yönlendirme, durum yönetimi, stil kitaplığı **SEÇİLMEDİ** (`requirements/app.txt`: "Frontend tooling will be selected separately") | – | – |
| Arka uç | FastAPI | API, kimlik doğrulama, sahiplik denetimi, Swagger/OpenAPI | TAAHHÜT | ASGI sunucusu **SEÇİLMEDİ** | – | – |
| Dil/çalışma zamanı | Python 3.11 | Arka uç, işçi, betikler | MEVCUT | `pyproject: >=3.11,<3.12`; CI 3.11; doğrulama paketi 3.11.15'te **DOĞRULANDI** | – | – |
| Veritabanı | PostgreSQL | Kullanıcı, oturum, iş (kuyruk), plan, model sürümü, medya meta verisi | TAAHHÜT; 18.x ÖNERİ | 18.6 (kapsayıcı) **DOĞRULANDI**: 110 test | MySQL, SQLite, MongoDB (`v1/03` matrisi: %95,6 / %77,2 / %66,8 / %67,8) | D-01 |
| Veritabanı sürücüsü | psycopg 3 | Test paketinde SQL | DOĞRULANDI (testlerde 3.3.6) | uygulamada ORM/sürücü **SEÇİLMEDİ** | SQLAlchemy 2.x + asyncpg/psycopg | D-12 |
| Migration | Düz SQL (`up`/`down`) şimdilik | Şema sürümleme (Hf 4: migration'lar) | DOĞRULANDI (up→down→up aynı şema) | – | Alembic (ÖNERİ, uygulamada) | D-12 |
| İş kuyruğu | PostgreSQL `FOR UPDATE SKIP LOCKED` | İşleri GPU işçisine dağıtma | TAAHHÜT (kuyruk PostgreSQL'de); mekanizma ÖNERİ | 200 iş × 8 işçi: çift kapma yok (gözlem) | Redis/RabbitMQ (gerekçesiz bulundu) | – |
| Parola | Argon2id (`argon2-cffi`) | Tuzlu parola özeti (NFR-01) | TAAHHÜT (tuzlu özet); Argon2id ÖNERİ | 25.1.0 **DOĞRULANDI**, varsayılan parametrelerle ≈47 ms (yalnız bu makine) | bcrypt, scrypt | – |
| Oturum | Sunucu tarafı tablo + HttpOnly/SameSite çerez | Çıkışta geçersiz kılma (NFR-01) | çerez TAAHHÜT; tablo ÖNERİ | `auth_session` testleri | JWT (sunucu tarafı iptal gerekir) | D-08 |
| Dosya deposu | Yerel dosya sistemi / Docker birimi, `MediaStore` arayüzü | Çizimler, **kare arşivi (ZIP)**, MP4, küçük resim | TAAHHÜT ("kareler ve videolar dosya deposunda"); arayüz ve arşiv biçimi ÖNERİ; **kareler saklanır: karar D-09 (2026-10-22)** | referans protokol testleri (10) **DOĞRULANDI**; gerçek dosya sistemi hataları yalnız benzetim | S3 uyumlu depo (gelecek); kare başına varlık (reddedildi) | D-09, D-13 |
| Dağıtım | Docker Compose | Tüm bileşenler (NFR-07) | TAAHHÜT | PostgreSQL ve PlantUML kapsayıcıları **DOĞRULANDI**; Compose dosyası **yazılmadı** | Kubernetes (gerekçesiz) | – |
| HTTPS/ters vekil | (ürün **SEÇİLMEDİ**) | TLS sonlandırma, React derlemesini sunma | HTTPS TAAHHÜT; ürün SEÇİLMEDİ | – | Caddy, Nginx, Traefik | – |
| GPU işçisi | Python süreci, veritabanı yoklaması | Model çalıştırma, MP4 üretme | ÖNERİ | PyTorch/CUDA sürümü **SEÇİLMEDİ** (`README`: mimari, kontrol noktası, çerçeve, CUDA seçilmedi) | – | – |
| Üretim modeli | ToonCrafter-512 (dondurulmuş) + LoRA + plan modülü (FiLM) | Ara kare üretimi | TAAHHÜT (araştırma hipotezi) | **doğrulanmadı**; ≥24 GB GPU varsayımı; eğitim yolunun ilk+son kare koşulu 1. hafta denetimi | RIFE (kontrol koşulu R0) | – |
| Plan çözümleyici | Yerel LLM (model **SEÇİLMEDİ**) + kural tabanlı doğrulayıcı | İngilizce komut → plan (isteğe bağlı) | TAAHHÜT | **doğrulanmadı**; konumu açık karar | – | D-18 |
| Veri hattı | XDoG (çizgi), RAFT (titreşim) | Veri seti hazırlama | TAAHHÜT | **doğrulanmadı** | – | – |
| Deney izleme | (**SEÇİLMEDİ**; dosya tabanlı koşu klasörleri önerilir) | Koşu/metrik kaydı | SEÇİLMEDİ | `.env.example` `EXPERIMENT_TRACKING_URI` boş | MLflow | D-14 |
| Test | pytest | Birim, entegrasyon, şema | MEVCUT (`pytest>=8,<9`) | doğrulama paketi **pytest 9.1.1** ile yalıtık ortamda koştu; depoya taşınırsa `<9` ile uyumlu hale getirilmeli | – | – |
| Kod kalitesi | ruff, pre-commit | Biçim ve lint | MEVCUT (`ruff>=0.9,<1`) | – | – | – |
| CI | GitHub Actions | ruff, pytest, pre-commit | MEVCUT | PostgreSQL gerektiren testler için CI'da servis **eklenmedi** | – | – |
| API belgesi | Swagger/OpenAPI (FastAPI), Postman | Hf 4 teslimi | TAAHHÜT | – | – | – |
| Diyagram | PlantUML + Graphviz (kapsayıcı) | Tüm UML ve ER diyagramları | ÖNERİ; DOĞRULANDI | PlantUML 1.2026.9, Graphviz 14.0.1 (`tools/TOOLCHAIN.lock`) | Mermaid (UML use case/aktivite zayıf) | – |
| Tasarım | Figma | 6 ekran tıklanabilir prototip | TAAHHÜT | tasarım belirtimi `docs/design/` (V4) hazır; **Figma dosyası oluşturulmadı** (bağlayıcı kimlik doğrulamasız) | – | – |

## Notlar
- Uydurma sürüm yazılmadı: `SEÇİLMEDİ` satırlarının sürümü kararla birlikte netleşecek.
- Doğrulananlar yalnızca bu makinede ve test kapsamında geçerlidir (ör. Argon2id süresi, kuyruk testi tek makine).
- Tüm `ÖNERİ` satırları `reports/05_DECISIONS_RECONCILIATION.md` ve `reports/07_OPEN_APPROVALS.md` ile birlikte onaylanmalıdır.
