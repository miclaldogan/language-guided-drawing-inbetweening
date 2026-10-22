# Diyagram Dizini

**Durum sütunu:** `ÖNERİ` = teknik olarak doğrulandı, **onay bekliyor**. Hiçbir diyagram onaylanmış taahhüt değildir. Kaynak = düzenlenebilir `.puml` (PlantUML 1.2026.9); çıktılar `.svg`, `.png`, `.pdf` aynı klasördedir. Yeniden üretim: `tools/render.sh <dosya.puml>`. Ortak stil: `diagrams/_style/cue.iuml` (renk = katman: mavi kullanıcı/ön yüz, yeşil API, amber veritabanı/depolama, mor yapay zekâ/GPU, gri altyapı).

Hoca takvimi: **Hf 1** use case, sistem mimarisi, ≥3 akış (hata dallı), AI pipeline · **Hf 2** ER diyagramı, şema, veri sözlüğü, yığın tablosu.

| Hf 1 kimliği | Dosya | Amaç (yanıtladığı soru) | İlgili gereksinimler | Hoca takvimi | Durum |
| --- | --- | --- | --- | --- | --- |
| W1-D01 | `use-case/uc-01-use-case` | Kim ne yapabilir? Kapsam sınırı nedir? | FR-01…FR-10 | **Hf 1 zorunlu** | ÖNERİ |
| W1-D02 | `architecture/arch-01-container` | Hangi kapsayıcı ne yapar, senkron/asenkron sınırı, güven sınırı nerede? | FR-06, FR-07, NFR-01, NFR-07 | **Hf 1 zorunlu** (sistem mimarisi) | ÖNERİ (plan çözümleyici yeri D-18 bekliyor) |
| W1-D03 | `activity/act-01-authentication` | Kimlik/oturum karar mantığı ve yetkisiz erişim | FR-01, FR-02, NFR-01 | **Hf 1 zorunlu** (akış 1/3) | ÖNERİ |
| W1-D04 | `activity/act-02-animation-creation` | Yükleme → isteğe bağlı komut → plan → gönderim | FR-03…FR-06 | **Hf 1 zorunlu** (akış 2/3) | ÖNERİ (D-07 dalı bekliyor) |
| W1-D05 | `activity/act-03-job-execution` | İş yürütme, işçi çökmesi, iptal, tutarlı durum | FR-06, FR-07, FR-10, NFR-03 | **Hf 1 zorunlu** (akış 3/3) | ÖNERİ |
| W1-D06 | `ai-pipeline/ai-01-pipeline` | Yapay zekâ bileşenleri ve çevrimdışı/çevrimiçi ayrımı | FR-04…FR-06, FR-10…FR-12, NFR-04 | **Hf 1 zorunlu** | ÖNERİ (önerilen bileşenler doğrulanmadı) |
| W1-D07 | `state-machine/sm-01-job-state-machine` | Hangi iş durum geçişleri yasal? | FR-07, NFR-03 | Hf 1'de zorunlu değil; temel mühendislik çıktısı | ÖNERİ (CHECK'lerle doğrulandı) |
| W2-D01 | `database/physical-erd` | Şema nedir? (mantıksal + fiziksel birleşik; DDL'den **üretilir**) | FR-01…FR-10, NFR-01/03/04/05 | **Hf 2 zorunlu** (ER) | ÖNERİ |
| W2-D02 | `database/conceptual-erd` | İş varlıkları ve ilişkileri (tip yok) | aynı | Hf 2'de dolaylı | ÖNERİ |
| SD-1 | `sequence/sd-01-authentication` | Kayıt, giriş, yetkili istek, çıkış | FR-01, FR-02, NFR-01 | önerilen | ÖNERİ |
| SD-2 | `sequence/sd-02-keyframe-upload` | Dosya-önce yazma, kısmi hata, sahipsiz dosya | FR-03, NFR-03, NFR-05 | önerilen | ÖNERİ |
| SD-3 | `sequence/sd-03-plan-preview` | İsteğe bağlı komut, plan onayı, LM'nin zorunlu olmadığı | FR-04, FR-05 | önerilen | ÖNERİ |
| SD-4a | `sequence/sd-04a-job-submission` | Senkron gönderim, idempotency, sahiplik FK | FR-06, FR-10, NFR-03 | önerilen | ÖNERİ |
| SD-4b | `sequence/sd-04b-job-execution` | Asenkron işçi, kapma, heartbeat, tamamlama | FR-06, FR-07, FR-10, NFR-02/03 | önerilen | ÖNERİ |
| SD-5 | `sequence/sd-05-status-and-result` | Yoklama, oynatma, indirme, yetki | FR-02, FR-07…FR-10, NFR-01 | önerilen | ÖNERİ |
| SD-6 | `sequence/sd-06-cancel-failure-delete` | İptal, işçi kaybı, silme yarışları | FR-07, FR-09, NFR-03, NFR-05 | önerilen | ÖNERİ |
| DEP-1 | `deployment/dep-01-deployment` | Yerel Docker Compose ve gelecekteki yönetilen büyüme yolu | NFR-07 | Hf 8 zorunlu (taslak) | ÖNERİ (B bölümü taahhüt değil) |

**Paylaşım notu:** `.svg` dosyaları `DejaVu Sans` yazı tipini adıyla ister (yazı tipi gömülü değildir); başka bilgisayarda yazı genişlikleri değişebilir. Sunum, e-posta ve teslim için **`.png` veya `.pdf`** kullanın (PDF'de yazı tipleri gömülüdür, Türkçe karakterler doğrulandı).

Diğer: `_style/smoke.*` yalnız araç zinciri doğrulama çıktısıdır (teslim edilecek diyagram değildir).

## Türkçe sürümler
Her diyagramın Türkçe karşılığı `diagrams/tr/<grup>/<aynı-ad>.puml` (+ `.svg`/`.png`/`.pdf`) altındadır; başlıklar, etiketler, notlar ve açıklama kutuları Türkçedir, **kimlikler** (tablo/sütun/rol adları, SQL, HTTP yolları, FR/NFR/D-xx) ve arayüz metinleri İngilizce kalır. Üretim: `tools/build_tr.py`; durum ve gereksinimler yukarıdaki tabloyla aynıdır.

## Neden birleştirildi / üretilmedi
- **Mantıksal ER ile fiziksel ER tek diyagramda:** 5 tabloda ikisi aynı bilgiyi taşır; fiziksel diyagram anahtar, zorunluluk, çokluk ve tipi birlikte gösterir. Ayrı mantıksal diyagram yinelenir. Mantıksal bakış `database/data-dictionary.md` ve kavramsal ERD ile karşılanır.
- **SD-4 iki parçaya bölündü** (gönderim ve yürütme): tek diyagramda eşzamanlı kalan HTTP ile asenkron yürütmeyi karıştırma riski ve okunabilirlik.
- **Üretilmeyenler:** C4 Context, DFD, C4 Component, ayrı eğitim/değerlendirme boru hattı, model/veri sürüm akışı, oturum/varlık durum makineleri (gerekçe: `v1/10_ENGINEERING_DIAGRAM_INVENTORY.md`).
