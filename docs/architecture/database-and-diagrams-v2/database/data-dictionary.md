# Veri Sözlüğü (PostgreSQL 18)

**Durum:** ÖNERİ, ONAYLANMADI. **OTOMATİK ÜRETİLDİ** (`tools/generate_db_artifacts.py`), tek kaynak `database/migrations/*.up.sql`. Elle düzenlemeyin.
Zaman damgaları `timestamptz` (UTC). Anahtar: **PK** birincil, **FK** yabancı, **UQ** tek sütunlu benzersiz. "Değişmez" sütunlar uygulama rollerine UPDATE yetkisi verilmeyerek korunur (bkz. Yetkiler).

## `app_user`

Hesap sahibi; sahiplik kökü (FR-01, FR-02).

| Sütun | Tip | Null | Varsayılan | Anahtar | Açıklama |
| --- | --- | --- | --- | --- | --- |
| `id` | `uuid` | hayır | `gen_random_uuid()` | PK | Kullanıcı kimliği (UUID). |
| `email` | `text` | hayır |  | UQ | Küçük harfe normalize e-posta; benzersiz. |
| `password_hash` | `text` | hayır |  |  | Argon2id PHC dizgesi; düz parola saklanmaz. |
| `created_at` | `timestamp with time zone` | hayır | `now()` |  | Hesap oluşturma zamanı (UTC). |

**Kısıtlar:**

- `app_user_email_normalized` (CHECK): `CHECK (((email = lower(email)) AND ((char_length(email) >= 3) AND (char_length(email) <= 254))))`
- `app_user_password_hash_argon2id` (CHECK): `CHECK ((password_hash ~ '^\$argon2id\$'::text))`
- `app_user_pkey` (PK): `PRIMARY KEY (id)`
- `app_user_email_key` (UNIQUE): `UNIQUE (email)`

## `auth_session`

Sunucu tarafı oturum; çıkışta satır silinir (FR-01, NFR-01).

| Sütun | Tip | Null | Varsayılan | Anahtar | Açıklama |
| --- | --- | --- | --- | --- | --- |
| `id` | `uuid` | hayır | `gen_random_uuid()` | PK | Oturum satırı kimliği. |
| `user_id` | `uuid` | hayır |  | FK | Oturum sahibi; kullanıcı silinince oturum da silinir. |
| `token_hash` | `bytea` | hayır |  | UQ | Ham belirtecin SHA-256 özeti (32 bayt); ham belirteç saklanmaz. |
| `created_at` | `timestamp with time zone` | hayır | `now()` |  | Oturum açılış zamanı (UTC). |
| `last_seen_at` | `timestamp with time zone` | hayır | `now()` |  | Son görülme (en çok dakikada bir güncellenir). |
| `expires_at` | `timestamp with time zone` | hayır |  |  | Mutlak bitiş zamanı (UTC). |

**Kısıtlar:**

- `auth_session_expiry` (CHECK): `CHECK ((expires_at > created_at))`
- `auth_session_token_hash_len` (CHECK): `CHECK ((octet_length(token_hash) = 32))`
- `auth_session_user_id_fkey` (FK): `FOREIGN KEY (user_id) REFERENCES app_user(id) ON DELETE CASCADE  — silme: CASCADE`
- `auth_session_pkey` (PK): `PRIMARY KEY (id)`
- `auth_session_token_hash_key` (UNIQUE): `UNIQUE (token_hash)`

## `model_version`

Üretimde kullanılan kayıtlı model yapılandırması (FR-10). Operatör yayın adımıyla eklenir.

| Sütun | Tip | Null | Varsayılan | Anahtar | Açıklama |
| --- | --- | --- | --- | --- | --- |
| `id` | `uuid` | hayır | `gen_random_uuid()` | PK | Model sürümü kimliği. |
| `name` | `text` | hayır |  |  | Model adı, örn. cue-m3, cue-m2. |
| `version_label` | `text` | hayır |  |  | Sürüm etiketi. |
| `weights_sha256` | `text` | hayır |  |  | Ağırlık dosyasının SHA-256 özeti (tekrarlanabilirlik, NFR-04). |
| `code_commit` | `text` | evet |  |  | Eğitim/çıkarım kodunun commit kimliği. |
| `training_run_ref` | `text` | evet |  |  | Deney kaydına opak başvuru; yabancı anahtar değildir. |
| `supports_plan` | `boolean` | hayır |  |  | Sürüm hareket planını kullanıyor mu (M3) yoksa yok sayıyor mu (M2). |
| `inference_defaults` | `jsonb` | hayır | `'{}'::jsonb` |  | Varsayılan çıkarım parametreleri (JSON nesnesi). |
| `is_active` | `boolean` | hayır | `false` |  | İşçinin yükleyeceği sürüm; en çok bir satır true olabilir. |
| `created_at` | `timestamp with time zone` | hayır | `now()` |  | Kayıt zamanı (UTC). |

**Kısıtlar:**

- `model_version_defaults_object` (CHECK): `CHECK ((jsonb_typeof(inference_defaults) = 'object'::text))`
- `model_version_weights_sha256_fmt` (CHECK): `CHECK ((weights_sha256 ~ '^[0-9a-f]{64}$'::text))`
- `model_version_pkey` (PK): `PRIMARY KEY (id)`
- `model_version_name_label_key` (UNIQUE): `UNIQUE (name, version_label)`

## `media_asset`

Medya deposundaki bir dosyanın meta verisi; dosya veritabanında değildir (FR-03, FR-08).

| Sütun | Tip | Null | Varsayılan | Anahtar | Açıklama |
| --- | --- | --- | --- | --- | --- |
| `id` | `uuid` | hayır | `gen_random_uuid()` | PK | Varlık kimliği. |
| `owner_id` | `uuid` | hayır |  | FK | Varlığın sahibi. |
| `kind` | `text` | hayır |  |  | Rol: start_drawing, end_drawing, result_video, frames_archive, thumbnail. |
| `storage_key` | `text` | hayır |  | UQ | Medya deposundaki göreli, opak anahtar; yetkilendirme aracı değildir. |
| `content_type` | `text` | hayır |  |  | MIME türü (image/png, image/jpeg, video/mp4, application/zip); görüntü türleri R1 kararına bağlı. |
| `byte_size` | `bigint` | hayır |  |  | Dosya boyutu (bayt). |
| `width` | `integer` | evet |  |  | Görüntü genişliği (piksel); video için de doldurulabilir. |
| `height` | `integer` | evet |  |  | Görüntü yüksekliği (piksel). |
| `sha256` | `text` | hayır |  |  | İçerik SHA-256 özeti (bütünlük denetimi). |
| `created_at` | `timestamp with time zone` | hayır | `now()` |  | Kayıt zamanı (UTC). |

**Kısıtlar:**

- `media_asset_dims_pos` (CHECK): `CHECK ((((width IS NULL) OR (width > 0)) AND ((height IS NULL) OR (height > 0))))`
- `media_asset_kind_type` (CHECK): `CHECK ((((kind = 'result_video'::text) = (content_type = 'video/mp4'::text)) AND ((kind = 'frames_archive'::text) = (content_type = 'application/zip'::text))))`
- `media_asset_kind_valid` (CHECK): `CHECK ((kind = ANY (ARRAY['start_drawing'::text, 'end_drawing'::text, 'result_video'::text, 'frames_archive'::text, 'thumbnail'::text])))`
- `media_asset_sha256_fmt` (CHECK): `CHECK ((sha256 ~ '^[0-9a-f]{64}$'::text))`
- `media_asset_size_pos` (CHECK): `CHECK ((byte_size > 0))`
- `media_asset_type_valid` (CHECK): `CHECK ((content_type = ANY (ARRAY['image/png'::text, 'image/jpeg'::text, 'video/mp4'::text, 'application/zip'::text])))`
- `media_asset_owner_id_fkey` (FK): `FOREIGN KEY (owner_id) REFERENCES app_user(id) ON DELETE RESTRICT  — silme: RESTRICT`
- `media_asset_pkey` (PK): `PRIMARY KEY (id)`
- `media_asset_id_owner_key` (UNIQUE): `UNIQUE (id, owner_id)`
- `media_asset_storage_key_key` (UNIQUE): `UNIQUE (storage_key)`

## `animation_job`

Üretim isteği, yaşam döngüsü ve kuyruk girişi (FR-04..FR-07, FR-09, FR-10).

| Sütun | Tip | Null | Varsayılan | Anahtar | Açıklama |
| --- | --- | --- | --- | --- | --- |
| `id` | `uuid` | hayır | `gen_random_uuid()` | PK | İş kimliği. |
| `owner_id` | `uuid` | hayır |  | FK | İşin sahibi (değişmez). |
| `idempotency_key` | `uuid` | hayır |  |  | İstemcinin ürettiği gönderim anahtarı; (owner_id, key) benzersiz (değişmez). |
| `status` | `text` | hayır | `'queued'::text` |  | queued, running, done, failed, cancelled. |
| `command_text` | `text` | evet |  |  | İsteğe bağlı İngilizce komut; plan ile birlikte dolu/boş (değişmez). |
| `plan` | `jsonb` | evet |  |  | Onaylanmış hareket planı (JSON nesnesi) (değişmez). |
| `plan_schema_version` | `smallint` | evet |  |  | Plan JSON şema sürümü (değişmez). |
| `plan_approved_at` | `timestamp with time zone` | evet |  |  | Kullanıcının planı onayladığı an (değişmez). |
| `seed` | `bigint` | hayır |  |  | Üretim tohumu (değişmez). |
| `inference_params` | `jsonb` | hayır | `'{}'::jsonb` |  | Üretimde kullanılan çıkarım parametreleri anlık görüntüsü (değişmez). |
| `start_asset_id` | `uuid` | hayır |  | FK | Başlangıç çizimi (aynı sahibe ait; değişmez). |
| `end_asset_id` | `uuid` | hayır |  | FK | Bitiş çizimi (aynı sahibe ait; değişmez). |
| `thumbnail_asset_id` | `uuid` | evet |  | FK | İsteğe bağlı küçük resim varlığı. |
| `video_asset_id` | `uuid` | evet |  | FK | Sonuç MP4; yalnız done durumunda dolu. |
| `frames_asset_id` | `uuid` | evet |  | FK | Üretilen ara karelerin tek arşivi (ZIP, PNG kareleri; karar D-09); yalnız done durumunda dolu. |
| `frame_count` | `smallint` | evet |  |  | Arşivdeki kare sayısı (2..16; ilk ve son kare girdi çizimleridir); yalnız done durumunda dolu. |
| `model_version_id` | `uuid` | evet |  | FK | İşçinin kapma anında kaydettiği model sürümü. |
| `locked_by` | `text` | evet |  |  | Kapan işçi örneği etiketi. |
| `heartbeat_at` | `timestamp with time zone` | evet |  |  | İşçinin son canlılık işareti (running iken). |
| `created_at` | `timestamp with time zone` | hayır | `now()` |  | Gönderim zamanı (UTC). |
| `started_at` | `timestamp with time zone` | evet |  |  | Kapma zamanı (UTC). |
| `finished_at` | `timestamp with time zone` | evet |  |  | Terminal duruma geçiş zamanı (UTC). |
| `error_code` | `text` | evet |  |  | Makine okunur hata kodu; yalnız failed durumunda. |
| `error_message` | `text` | evet |  |  | Kullanıcıya gösterilebilir hata iletisi; yalnız failed durumunda. |

**Kısıtlar:**

- `animation_job_command_len` (CHECK): `CHECK (((command_text IS NULL) OR ((char_length(command_text) >= 1) AND (char_length(command_text) <= 1000))))`
- `animation_job_finished_after_started` (CHECK): `CHECK (((finished_at IS NULL) OR (finished_at >= COALESCE(started_at, created_at))))`
- `animation_job_frame_count_range` (CHECK): `CHECK (((frame_count IS NULL) OR ((frame_count >= 2) AND (frame_count <= 16))))`
- `animation_job_frames_pair` (CHECK): `CHECK (((frames_asset_id IS NULL) = (frame_count IS NULL)))`
- `animation_job_inputs_distinct` (CHECK): `CHECK ((start_asset_id <> end_asset_id))`
- `animation_job_params_object` (CHECK): `CHECK ((jsonb_typeof(inference_params) = 'object'::text))`
- `animation_job_plan_group` (CHECK): `CHECK ((((command_text IS NULL) = (plan IS NULL)) AND ((plan IS NULL) = (plan_approved_at IS NULL)) AND ((plan IS NULL) = (plan_schema_version IS NULL))))`
- `animation_job_plan_object` (CHECK): `CHECK (((plan IS NULL) OR (jsonb_typeof(plan) = 'object'::text)))`
- `animation_job_started_after_created` (CHECK): `CHECK (((started_at IS NULL) OR (started_at >= created_at)))`
- `animation_job_state_cancelled` (CHECK): `CHECK (((status <> 'cancelled'::text) OR ((finished_at IS NOT NULL) AND (video_asset_id IS NULL) AND (frames_asset_id IS NULL) AND (error_code IS NULL))))`
- `animation_job_state_done` (CHECK): `CHECK (((status <> 'done'::text) OR ((started_at IS NOT NULL) AND (finished_at IS NOT NULL) AND (video_asset_id IS NOT NULL) AND (frames_asset_id IS NOT NULL) AND (model_version_id IS NOT NULL) AND (error_code IS NULL))))`
- `animation_job_state_failed` (CHECK): `CHECK (((status <> 'failed'::text) OR ((finished_at IS NOT NULL) AND (video_asset_id IS NULL) AND (frames_asset_id IS NULL) AND (error_code IS NOT NULL) AND (error_message IS NOT NULL))))`
- `animation_job_state_queued` (CHECK): `CHECK (((status <> 'queued'::text) OR ((started_at IS NULL) AND (finished_at IS NULL) AND (video_asset_id IS NULL) AND (frames_asset_id IS NULL) AND (locked_by IS NULL))))`
- `animation_job_state_running` (CHECK): `CHECK (((status <> 'running'::text) OR ((started_at IS NOT NULL) AND (finished_at IS NULL) AND (video_asset_id IS NULL) AND (frames_asset_id IS NULL) AND (locked_by IS NOT NULL) AND (heartbeat_at IS NOT NULL) AND (model_version_id IS NOT NULL))))`
- `animation_job_status_valid` (CHECK): `CHECK ((status = ANY (ARRAY['queued'::text, 'running'::text, 'done'::text, 'failed'::text, 'cancelled'::text])))`
- `animation_job_end_asset_fk` (FK): `FOREIGN KEY (end_asset_id, owner_id) REFERENCES media_asset(id, owner_id)  — silme: NO ACTION`
- `animation_job_frames_asset_fk` (FK): `FOREIGN KEY (frames_asset_id, owner_id) REFERENCES media_asset(id, owner_id)  — silme: NO ACTION`
- `animation_job_model_version_id_fkey` (FK): `FOREIGN KEY (model_version_id) REFERENCES model_version(id) ON DELETE RESTRICT  — silme: RESTRICT`
- `animation_job_owner_id_fkey` (FK): `FOREIGN KEY (owner_id) REFERENCES app_user(id) ON DELETE RESTRICT  — silme: RESTRICT`
- `animation_job_start_asset_fk` (FK): `FOREIGN KEY (start_asset_id, owner_id) REFERENCES media_asset(id, owner_id)  — silme: NO ACTION`
- `animation_job_thumb_asset_fk` (FK): `FOREIGN KEY (thumbnail_asset_id, owner_id) REFERENCES media_asset(id, owner_id)  — silme: NO ACTION`
- `animation_job_video_asset_fk` (FK): `FOREIGN KEY (video_asset_id, owner_id) REFERENCES media_asset(id, owner_id)  — silme: NO ACTION`
- `animation_job_pkey` (PK): `PRIMARY KEY (id)`

## Yetkiler (rol × tablo)

Roller `NOLOGIN` grup rolleridir; giriş hesapları dağıtımda üye yapılır. UPDATE yalnız listelenen sütunlarda.

| Rol | Tablo | Tablo yetkileri | Sütun düzeyi UPDATE |
| --- | --- | --- | --- |
| `cue_api` | `app_user` | INSERT, SELECT | — |
| `cue_api` | `auth_session` | DELETE, INSERT, SELECT | `last_seen_at` |
| `cue_api` | `model_version` | SELECT | — |
| `cue_api` | `media_asset` | DELETE, INSERT, SELECT | — |
| `cue_api` | `animation_job` | DELETE, INSERT, SELECT | `status`, `finished_at` |
| `cue_worker` | `model_version` | SELECT | — |
| `cue_worker` | `media_asset` | INSERT, SELECT | — |
| `cue_worker` | `animation_job` | SELECT | `status`, `video_asset_id`, `frames_asset_id`, `frame_count`, `model_version_id`, `locked_by`, `heartbeat_at`, `started_at`, `finished_at`, `error_code`, `error_message` |
| `cue_maintenance` | `auth_session` | DELETE, SELECT | — |
| `cue_maintenance` | `media_asset` | DELETE, SELECT | — |
| `cue_maintenance` | `animation_job` | SELECT | `status`, `finished_at`, `error_code`, `error_message` |
