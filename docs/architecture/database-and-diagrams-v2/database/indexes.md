# İndeks Stratejisi

**Durum:** ÖNERİ, ONAYLANMADI. **OTOMATİK ÜRETİLDİ** (`tools/generate_db_artifacts.py`). Performans iddiası yoktur; indeksler erişim yoluna göre seçilmiştir.

| Tablo | İndeks | Tanım | Amaç |
| --- | --- | --- | --- |
| `app_user` | `app_user_email_key` | `btree (email)` | Girişte e-posta araması; kayıtta benzersizlik (FR-01). |
| `app_user` | `app_user_pkey` | `btree (id)` | Birincil anahtar. |
| `auth_session` | `auth_session_pkey` | `btree (id)` | Birincil anahtar. |
| `auth_session` | `auth_session_token_hash_key` | `btree (token_hash)` | Her istekte oturum çözme (en sık sorgu, Q6). |
| `auth_session` | `auth_session_user_id_idx` | `btree (user_id)` | Hesap silme ve FK denetimi. |
| `model_version` | `model_version_name_label_key` | `btree (name, version_label)` | Aday anahtar: (ad, sürüm etiketi). |
| `model_version` | `model_version_pkey` | `btree (id)` | Birincil anahtar. |
| `model_version` | `model_version_single_active_idx` | `btree (is_active) WHERE is_active` | Değişmez: en çok bir etkin model sürümü; Q9. |
| `media_asset` | `media_asset_id_owner_key` | `btree (id, owner_id)` | Bileşik FK hedefi: iş→varlık sahiplik denetimi. |
| `media_asset` | `media_asset_owner_id_idx` | `btree (owner_id)` | Hesap silme, sahip başına envanter, FK denetimi. |
| `media_asset` | `media_asset_pkey` | `btree (id)` | Birincil anahtar. |
| `media_asset` | `media_asset_storage_key_key` | `btree (storage_key)` | Depo anahtarı benzersiz. |
| `animation_job` | `animation_job_end_asset_key` | `btree (end_asset_id)` | Bir varlık en çok bir işin bitiş çizimi; FK denetimi. |
| `animation_job` | `animation_job_frames_asset_key` | `btree (frames_asset_id) WHERE (frames_asset_id IS NOT NULL)` | Bir kare arşivi en çok bir işe ait (karar D-09). |
| `animation_job` | `animation_job_owner_created_idx` | `btree (owner_id, created_at DESC, id DESC)` | Kitaplık listesi + keyset sayfalama (Q1); sahip süzmesi. |
| `animation_job` | `animation_job_owner_idem_key` | `btree (owner_id, idempotency_key)` | İdempotency: (sahip, anahtar) benzersiz. |
| `animation_job` | `animation_job_pkey` | `btree (id)` | Birincil anahtar. |
| `animation_job` | `animation_job_queue_idx` | `btree (created_at, id) WHERE (status = 'queued'::text)` | Kuyruktan en eski bekleyen iş (Q3); yalnız queued satırlar. |
| `animation_job` | `animation_job_running_hb_idx` | `btree (heartbeat_at) WHERE (status = 'running'::text)` | Takılı iş bulma (Q4); yalnız running satırlar. |
| `animation_job` | `animation_job_start_asset_key` | `btree (start_asset_id)` | Bir varlık en çok bir işin başlangıç çizimi; FK denetimi. |
| `animation_job` | `animation_job_thumb_asset_key` | `btree (thumbnail_asset_id) WHERE (thumbnail_asset_id IS NOT NULL)` | Bir küçük resim en çok bir işe ait. |
| `animation_job` | `animation_job_video_asset_key` | `btree (video_asset_id) WHERE (video_asset_id IS NOT NULL)` | Bir video en çok bir işe ait. |

## Bilinçli olarak OLUŞTURULMAYAN indeksler

| Aday | Gerekçe |
| --- | --- |
| animation_job (owner_id, status, …) | Panelde süzme yok; kullanıcı başına satır sayısı küçük. |
| animation_job (finished_at) WHERE status='failed' | Çok seyrek operatör sorgusu (Q8); ölçülmeden eklenmez. |
| animation_job (model_version_id) | model_version satırları silinmez. |
| auth_session (expires_at) | Günlük temizlik küçük tabloda tarama; her oturum eklemesinde ek yazma maliyeti gereksiz. |
| media_asset (created_at) | Bağlanmamış yükleme temizliği günlük ve küçük tabloda. |
| GIN (plan jsonb) | Planı aramak gereksinimi yok. |

## Temsili sorgular ve doğrulanan erişim yolları

`database/validation/test_schema.py::test_indexes_are_usable_for_access_paths` her erişim yolunun ilgili indeksi **kullanabildiğini** `EXPLAIN` ile doğrular (küçük tabloda `enable_seqscan=off`). Bu bir hız ölçümü değildir.

| Erişim yolu | İndeks |
| --- | --- |
| Kitaplık, keyset sayfalama | `animation_job_owner_created_idx` |
| İş kapma (en eski `queued`) | `animation_job_queue_idx` |
| Takılı iş (`running`, eski heartbeat) | `animation_job_running_hb_idx` |
| İdempotency araması | `animation_job_owner_idem_key` |
| Oturum çözme | `auth_session_token_hash_key` |
| Girişte e-posta | `app_user_email_key` |
