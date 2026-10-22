# Hafta 2 Teslim Kontrol Listesi (Mockup + Veritabanı)

**Resmî takvim (Hf 2):** "Figma tıklanabilir prototip (en az 6 ekran), ER diyagramı, şema, veri sözlüğü, teknoloji yığını tablosu" · Repoya teslim · Sınıfta 5 dk sunum. Belgeler `docs/` altında tutulur. **Hiçbir şey commit edilmedi veya push edilmedi.**

| İster | Durum | Dosya |
| --- | --- | --- |
| ER diyagramı (İngilizce) | HAZIR (onay bekliyor) | `diagrams/database/physical-erd.{puml,svg,png,pdf}` ve `diagrams/database/conceptual-erd.*` |
| ER diyagramı (Türkçe) | HAZIR (onay bekliyor) | `diagrams/tr/database/physical-erd.*`, `diagrams/tr/database/conceptual-erd.*` |
| Şema | HAZIR; PostgreSQL 18.6'da 110 test | `database/schema.sql`, `database/migrations/` |
| Veri sözlüğü | HAZIR (Türkçe; DDL'den üretilir) | `database/data-dictionary.md`, `database/indexes.md` |
| Teknoloji yığını tablosu | **YENİ, HAZIR** | `week-02/TEKNOLOJI_YIGINI_TABLOSU.md` |
| Figma tıklanabilir prototip (≥6 ekran) | **YAPILMADI** | Figma bağlayıcısı kimlik doğrulamasız; tasarım belirtimi hazır: `docs/design/v4-integrated-atelier/` (FIGMA_HANDOFF.md, SIX_SCREEN_SPEC.md). Figma'da oturum açılınca ayrı iş |
| 5 dk sınıf sunumu | Taslak aşağıda | – |

## Dil seçimi (teslim için)
İki dil de hazır; yalnızca birini ya da ikisini birlikte teslim edebilirsiniz. Öneri: ana teslim **Türkçe** (`diagrams/tr/`; açıklamalar Türkçe), İngilizce sürüm kaynak/yedek olarak depoda. Teknik kimlikler her iki sürümde aynıdır.

## Onayınıza bağlı kalanlar (teslimden önce)
`reports/07_OPEN_APPROVALS.md`: D-07, D-18, D-19. **Kapandı:** D-02 (iptal eylemi var), D-03 (etkin iş silinmez, önce iptal), D-09 (kareler saklanır) (kareler saklanır; şema ve diyagramlar buna göre güncellendi). Kalan kararlar şemayı küçük ölçüde etkileyebilir; Hf 2 sunumundan önce netleşmesi önerilir.

## Hf 1'den kalan eksik (bilgi)
- "İsterlerin GitHub Issues'a aktarılması" yapılmadı (depoya yazma/GitHub işlemi; sizin onayınız gerekir).
- Hf 1 diyagramları (use case, mimari, akış ×3, AI pipeline) hazır ve Türkçeleri de var: `diagrams/INDEX.md`.

## 5 dakikalık sunum akışı (taslak, ~5 slayt)
1. **Problem ve veri modeli (45 sn):** iki çizim → animasyon; 5 tablo; ekran ≠ tablo. (`conceptual-erd`)
2. **Neden PostgreSQL (60 sn):** öneri formundaki taahhüt + üç gerekçe (kuyruk, sahiplik, migration); alternatif matrisi %95,6 vs %77,2/%67,8/%66,8.
3. **Şema (75 sn):** `physical-erd`; bileşik FK ile sahiplik; durum başına CHECK; plan = jsonb.
4. **Doğrulama (75 sn):** 110 test; bulunan 2 gerçek yarış (F-01 `now()`, F-02 idempotency) ve düzeltmeleri; 8 işçi × 200 iş.
5. **Açık kararlar ve sonraki adım (45 sn):** D-07, D-18, D-19 (D-02, D-03, D-09 kapandı); teknoloji yığını tablosu; Hf 3 veri + baseline.
