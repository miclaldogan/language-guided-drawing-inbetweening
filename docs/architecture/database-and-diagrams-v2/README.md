# Cue — Veritabanı ve Diyagramlar v2

**Durum:** ÖNERİ, ONAYLANMADI. v1 (`../database-and-diagrams-v1/`) değiştirilmedi. Onay bekleyenler: `reports/07_OPEN_APPROVALS.md`.

| Yol | İçerik |
| --- | --- |
| `database/migrations/` | `0001_initial`, `0002_roles_and_grants` (up/down) — kaynak |
| `database/schema.sql` | migration'ların birleşimi (`build_schema.sh`) |
| `database/data-dictionary.md`, `indexes.md` | **otomatik üretilir** (çalışan PostgreSQL 18'den) |
| `database/queries.md` | uygulama sözleşmesi sorguları + test verisi stratejisi |
| `database/validation/` | **110 test** (şema, yetki, durum, eşzamanlılık, migration, kimlik, medya protokolü + yedekten dönüş, RLS önerisi, giriş hesaplarıyla sağlama); `run.sh`; `media_protocol.py` yalnız referans gerçeklemedir |
| `database/optional/` | **Uygulanmamış** RLS önerisi (`rls_proposal.up/down.sql`), karar D-06 |
| `database/provisioning/` | Örnek rol/hesap sağlama betiği (parolasız); migration'dan **önce** çalışır |
| `diagrams/` | 17 diyagram İngilizce (`diagrams/<grup>/`) + aynı 17 diyagramın **Türkçe** sürümü (`diagrams/tr/<grup>/`); `.puml` + `.svg`/`.png`/`.pdf`; `INDEX.md` amaç/gereksinim/durum |
| `reports/` | 01 araç kurulumu, 02 DB doğrulama, 03 envanter, 04 izlenebilirlik, 05 karar mutabakatı, 06 incelemeler, 07 onaylar, **08 ölçek gözlemi, 09 v1 errata**; `raw/` ham çıktılar |
| `tools/` | `render.sh`, `generate_db_artifacts.py`, `build_tr.py` + `i18n_tr.py` (Türkçe sürümleri üretir), `check_consistency.py`, `TOOLCHAIN.lock` |
| `week-02/` | Hafta 2 teslim dizini: teknoloji yığını tablosu ve teslim kontrol listesi |

## Yeniden üretim (Docker + uv gerekir; sudo gerekmez)
```bash
tools/render.sh diagrams/<grup>/<dosya>.puml                      # SVG + PNG + PDF
database/validation/run.sh                                        # 110 test, tek kullanımlık PostgreSQL 18
uv run --python 3.11 --no-project --with 'psycopg[binary]==3.3.6' --with pytest==9.1.1 python tools/scale_probe.py   # ölçek gözlemi (150 bin iş)
uv run --python 3.11 --no-project --with 'psycopg[binary]==3.3.6' --with pytest==9.1.1 python tools/generate_db_artifacts.py   # sözlük, indeks, fiziksel ERD
uv run --python 3.11 --no-project --with 'psycopg[binary]==3.3.6' --with pytest==9.1.1 python tools/check_consistency.py       # 35 tutarlılık denetimi (EN + TR)
```
`generate_db_artifacts.py` `physical-erd.puml`'i yeniden yazar; ardından `tools/render.sh` ile çıktıları yenileyin.

## Dil: İngilizce ↔ Türkçe
- İngilizce `.puml` **kaynaktır**. Türkçe sürümler `python3 tools/build_tr.py` ile (İngilizce kaynak + `tools/i18n_tr.py` etiket çevirileri) üretilir; `diagrams/tr/` altındaki dosyaları elle düzenlemeyin.
- Her Türkçe diyagram aynı yapıyı (düğümler, oklar, dallar) ve aynı kimlikleri (tablo/sütun/rol adları, SQL, FR/NFR, D-xx) taşır; yalnız etiketler çevrilir. Arayüz metinleri ("Email or password is incorrect." gibi) arayüz İngilizce olduğundan çevrilmez.
- İngilizce kaynak değişirse `build_tr.py` çevirisi bulunmayan etiket için **hata verir**; `check_consistency.py` Türkçe dosyaların güncel olduğunu denetler.
- Hafta 2 teslimi için dil seçimi: `week-02/HAFTA2_TESLIM_KONTROL_LISTESI.md`.
