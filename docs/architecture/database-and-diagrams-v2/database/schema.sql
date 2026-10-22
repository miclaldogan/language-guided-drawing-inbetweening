-- OTOMATİK ÜRETİLDİ: database/build_schema.sh. Elle düzenlemeyin; migrations/ kaynaktır.
-- Cue 0001_initial (UP) — PostgreSQL 18
-- Durum: ÖNERİ, ONAYLANMADI. v1/07_PHYSICAL_SCHEMA_SPECIFICATION.md'nin yürütülebilir ve test edilmiş halidir.
-- Kural: tüm zamanlar timestamptz (UTC); durum değerleri text + CHECK; kimlikler uuid.

CREATE TABLE app_user (
    id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    email         text        NOT NULL,
    password_hash text        NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT app_user_email_key UNIQUE (email),
    CONSTRAINT app_user_email_normalized CHECK (email = lower(email) AND char_length(email) BETWEEN 3 AND 254),
    CONSTRAINT app_user_password_hash_argon2id CHECK (password_hash ~ '^\$argon2id\$')
);

CREATE TABLE auth_session (
    id           uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      uuid        NOT NULL REFERENCES app_user (id) ON DELETE CASCADE,
    token_hash   bytea       NOT NULL,
    created_at   timestamptz NOT NULL DEFAULT now(),
    last_seen_at timestamptz NOT NULL DEFAULT now(),
    expires_at   timestamptz NOT NULL,
    CONSTRAINT auth_session_token_hash_key UNIQUE (token_hash),
    CONSTRAINT auth_session_token_hash_len CHECK (octet_length(token_hash) = 32),
    CONSTRAINT auth_session_expiry CHECK (expires_at > created_at)
);
CREATE INDEX auth_session_user_id_idx ON auth_session (user_id);

CREATE TABLE model_version (
    id                 uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    name               text        NOT NULL,
    version_label      text        NOT NULL,
    weights_sha256     text        NOT NULL,
    code_commit        text,
    training_run_ref   text,
    supports_plan      boolean     NOT NULL,
    inference_defaults jsonb       NOT NULL DEFAULT '{}'::jsonb,
    is_active          boolean     NOT NULL DEFAULT false,
    created_at         timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT model_version_name_label_key UNIQUE (name, version_label),
    CONSTRAINT model_version_weights_sha256_fmt CHECK (weights_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT model_version_defaults_object CHECK (jsonb_typeof(inference_defaults) = 'object')
);
CREATE UNIQUE INDEX model_version_single_active_idx ON model_version (is_active) WHERE is_active;

CREATE TABLE media_asset (
    id           uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id     uuid        NOT NULL REFERENCES app_user (id) ON DELETE RESTRICT,
    kind         text        NOT NULL,
    storage_key  text        NOT NULL,
    content_type text        NOT NULL,
    byte_size    bigint      NOT NULL,
    width        integer,
    height       integer,
    sha256       text        NOT NULL,
    created_at   timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT media_asset_storage_key_key UNIQUE (storage_key),
    CONSTRAINT media_asset_id_owner_key    UNIQUE (id, owner_id),
    CONSTRAINT media_asset_kind_valid CHECK (kind IN ('start_drawing', 'end_drawing', 'result_video', 'frames_archive', 'thumbnail')),
    CONSTRAINT media_asset_type_valid CHECK (content_type IN ('image/png', 'image/jpeg', 'video/mp4', 'application/zip')),
    CONSTRAINT media_asset_kind_type  CHECK ((kind = 'result_video') = (content_type = 'video/mp4') AND (kind = 'frames_archive') = (content_type = 'application/zip')),
    CONSTRAINT media_asset_size_pos   CHECK (byte_size > 0),
    CONSTRAINT media_asset_dims_pos   CHECK ((width IS NULL OR width > 0) AND (height IS NULL OR height > 0)),
    CONSTRAINT media_asset_sha256_fmt CHECK (sha256 ~ '^[0-9a-f]{64}$')
);
CREATE INDEX media_asset_owner_id_idx ON media_asset (owner_id);

CREATE TABLE animation_job (
    id                  uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id            uuid        NOT NULL REFERENCES app_user (id) ON DELETE RESTRICT,
    idempotency_key     uuid        NOT NULL,
    status              text        NOT NULL DEFAULT 'queued',

    command_text        text,
    plan                jsonb,
    plan_schema_version smallint,
    plan_approved_at    timestamptz,
    seed                bigint      NOT NULL,
    inference_params    jsonb       NOT NULL DEFAULT '{}'::jsonb,
    start_asset_id      uuid        NOT NULL,
    end_asset_id        uuid        NOT NULL,

    thumbnail_asset_id  uuid,
    video_asset_id      uuid,
    frames_asset_id     uuid,
    frame_count         smallint,
    model_version_id    uuid        REFERENCES model_version (id) ON DELETE RESTRICT,

    locked_by           text,
    heartbeat_at        timestamptz,
    created_at          timestamptz NOT NULL DEFAULT now(),
    started_at          timestamptz,
    finished_at         timestamptz,

    error_code          text,
    error_message       text,

    CONSTRAINT animation_job_start_asset_fk FOREIGN KEY (start_asset_id,     owner_id) REFERENCES media_asset (id, owner_id),
    CONSTRAINT animation_job_end_asset_fk   FOREIGN KEY (end_asset_id,       owner_id) REFERENCES media_asset (id, owner_id),
    CONSTRAINT animation_job_thumb_asset_fk FOREIGN KEY (thumbnail_asset_id, owner_id) REFERENCES media_asset (id, owner_id),
    CONSTRAINT animation_job_video_asset_fk FOREIGN KEY (video_asset_id,     owner_id) REFERENCES media_asset (id, owner_id),
    CONSTRAINT animation_job_frames_asset_fk FOREIGN KEY (frames_asset_id,   owner_id) REFERENCES media_asset (id, owner_id),

    CONSTRAINT animation_job_status_valid    CHECK (status IN ('queued', 'running', 'done', 'failed', 'cancelled')),
    CONSTRAINT animation_job_inputs_distinct CHECK (start_asset_id <> end_asset_id),
    CONSTRAINT animation_job_plan_group CHECK (
        (command_text IS NULL) = (plan IS NULL)
        AND (plan IS NULL) = (plan_approved_at IS NULL)
        AND (plan IS NULL) = (plan_schema_version IS NULL)),
    CONSTRAINT animation_job_plan_object   CHECK (plan IS NULL OR jsonb_typeof(plan) = 'object'),
    CONSTRAINT animation_job_params_object CHECK (jsonb_typeof(inference_params) = 'object'),
    CONSTRAINT animation_job_command_len   CHECK (command_text IS NULL OR char_length(command_text) BETWEEN 1 AND 1000),
    CONSTRAINT animation_job_frame_count_range CHECK (frame_count IS NULL OR frame_count BETWEEN 2 AND 16),
    CONSTRAINT animation_job_frames_pair   CHECK ((frames_asset_id IS NULL) = (frame_count IS NULL)),

    CONSTRAINT animation_job_state_queued CHECK (status <> 'queued' OR
        (started_at IS NULL AND finished_at IS NULL AND video_asset_id IS NULL AND frames_asset_id IS NULL AND locked_by IS NULL)),
    CONSTRAINT animation_job_state_running CHECK (status <> 'running' OR
        (started_at IS NOT NULL AND finished_at IS NULL AND video_asset_id IS NULL AND frames_asset_id IS NULL
         AND locked_by IS NOT NULL AND heartbeat_at IS NOT NULL AND model_version_id IS NOT NULL)),
    CONSTRAINT animation_job_state_done CHECK (status <> 'done' OR
        (started_at IS NOT NULL AND finished_at IS NOT NULL AND video_asset_id IS NOT NULL AND frames_asset_id IS NOT NULL
         AND model_version_id IS NOT NULL AND error_code IS NULL)),
    CONSTRAINT animation_job_state_failed CHECK (status <> 'failed' OR
        (finished_at IS NOT NULL AND video_asset_id IS NULL AND frames_asset_id IS NULL AND error_code IS NOT NULL AND error_message IS NOT NULL)),
    CONSTRAINT animation_job_state_cancelled CHECK (status <> 'cancelled' OR
        (finished_at IS NOT NULL AND video_asset_id IS NULL AND frames_asset_id IS NULL AND error_code IS NULL)),

    CONSTRAINT animation_job_started_after_created  CHECK (started_at  IS NULL OR started_at  >= created_at),
    CONSTRAINT animation_job_finished_after_started CHECK (finished_at IS NULL OR finished_at >= COALESCE(started_at, created_at))
);

CREATE INDEX animation_job_owner_created_idx ON animation_job (owner_id, created_at DESC, id DESC);
CREATE INDEX animation_job_queue_idx         ON animation_job (created_at, id) WHERE status = 'queued';
CREATE INDEX animation_job_running_hb_idx    ON animation_job (heartbeat_at)   WHERE status = 'running';
CREATE UNIQUE INDEX animation_job_owner_idem_key  ON animation_job (owner_id, idempotency_key);
CREATE UNIQUE INDEX animation_job_start_asset_key ON animation_job (start_asset_id);
CREATE UNIQUE INDEX animation_job_end_asset_key   ON animation_job (end_asset_id);
CREATE UNIQUE INDEX animation_job_video_asset_key ON animation_job (video_asset_id)     WHERE video_asset_id IS NOT NULL;
CREATE UNIQUE INDEX animation_job_frames_asset_key ON animation_job (frames_asset_id)    WHERE frames_asset_id IS NOT NULL;
CREATE UNIQUE INDEX animation_job_thumb_asset_key ON animation_job (thumbnail_asset_id) WHERE thumbnail_asset_id IS NOT NULL;

-- ---------------------------------------------------------------------------
-- Veri sözlüğü açıklamaları (data-dictionary.md bunlardan üretilir)
-- ---------------------------------------------------------------------------
COMMENT ON TABLE app_user      IS 'Hesap sahibi; sahiplik kökü (FR-01, FR-02).';
COMMENT ON TABLE auth_session  IS 'Sunucu tarafı oturum; çıkışta satır silinir (FR-01, NFR-01).';
COMMENT ON TABLE model_version IS 'Üretimde kullanılan kayıtlı model yapılandırması (FR-10). Operatör yayın adımıyla eklenir.';
COMMENT ON TABLE media_asset   IS 'Medya deposundaki bir dosyanın meta verisi; dosya veritabanında değildir (FR-03, FR-08).';
COMMENT ON TABLE animation_job IS 'Üretim isteği, yaşam döngüsü ve kuyruk girişi (FR-04..FR-07, FR-09, FR-10).';

COMMENT ON COLUMN app_user.id            IS 'Kullanıcı kimliği (UUID).';
COMMENT ON COLUMN app_user.email         IS 'Küçük harfe normalize e-posta; benzersiz.';
COMMENT ON COLUMN app_user.password_hash IS 'Argon2id PHC dizgesi; düz parola saklanmaz.';
COMMENT ON COLUMN app_user.created_at    IS 'Hesap oluşturma zamanı (UTC).';

COMMENT ON COLUMN auth_session.id           IS 'Oturum satırı kimliği.';
COMMENT ON COLUMN auth_session.user_id      IS 'Oturum sahibi; kullanıcı silinince oturum da silinir.';
COMMENT ON COLUMN auth_session.token_hash   IS 'Ham belirtecin SHA-256 özeti (32 bayt); ham belirteç saklanmaz.';
COMMENT ON COLUMN auth_session.created_at   IS 'Oturum açılış zamanı (UTC).';
COMMENT ON COLUMN auth_session.last_seen_at IS 'Son görülme (en çok dakikada bir güncellenir).';
COMMENT ON COLUMN auth_session.expires_at   IS 'Mutlak bitiş zamanı (UTC).';

COMMENT ON COLUMN model_version.id                 IS 'Model sürümü kimliği.';
COMMENT ON COLUMN model_version.name               IS 'Model adı, örn. cue-m3, cue-m2.';
COMMENT ON COLUMN model_version.version_label      IS 'Sürüm etiketi.';
COMMENT ON COLUMN model_version.weights_sha256     IS 'Ağırlık dosyasının SHA-256 özeti (tekrarlanabilirlik, NFR-04).';
COMMENT ON COLUMN model_version.code_commit        IS 'Eğitim/çıkarım kodunun commit kimliği.';
COMMENT ON COLUMN model_version.training_run_ref   IS 'Deney kaydına opak başvuru; yabancı anahtar değildir.';
COMMENT ON COLUMN model_version.supports_plan      IS 'Sürüm hareket planını kullanıyor mu (M3) yoksa yok sayıyor mu (M2).';
COMMENT ON COLUMN model_version.inference_defaults IS 'Varsayılan çıkarım parametreleri (JSON nesnesi).';
COMMENT ON COLUMN model_version.is_active          IS 'İşçinin yükleyeceği sürüm; en çok bir satır true olabilir.';
COMMENT ON COLUMN model_version.created_at         IS 'Kayıt zamanı (UTC).';

COMMENT ON COLUMN media_asset.id           IS 'Varlık kimliği.';
COMMENT ON COLUMN media_asset.owner_id     IS 'Varlığın sahibi.';
COMMENT ON COLUMN media_asset.kind         IS 'Rol: start_drawing, end_drawing, result_video, frames_archive, thumbnail.';
COMMENT ON COLUMN media_asset.storage_key  IS 'Medya deposundaki göreli, opak anahtar; yetkilendirme aracı değildir.';
COMMENT ON COLUMN media_asset.content_type IS 'MIME türü (image/png, image/jpeg, video/mp4, application/zip); görüntü türleri R1 kararına bağlı.';
COMMENT ON COLUMN media_asset.byte_size    IS 'Dosya boyutu (bayt).';
COMMENT ON COLUMN media_asset.width        IS 'Görüntü genişliği (piksel); video için de doldurulabilir.';
COMMENT ON COLUMN media_asset.height       IS 'Görüntü yüksekliği (piksel).';
COMMENT ON COLUMN media_asset.sha256       IS 'İçerik SHA-256 özeti (bütünlük denetimi).';
COMMENT ON COLUMN media_asset.created_at   IS 'Kayıt zamanı (UTC).';

COMMENT ON COLUMN animation_job.id                  IS 'İş kimliği.';
COMMENT ON COLUMN animation_job.owner_id            IS 'İşin sahibi (değişmez).';
COMMENT ON COLUMN animation_job.idempotency_key     IS 'İstemcinin ürettiği gönderim anahtarı; (owner_id, key) benzersiz (değişmez).';
COMMENT ON COLUMN animation_job.status              IS 'queued, running, done, failed, cancelled.';
COMMENT ON COLUMN animation_job.command_text        IS 'İsteğe bağlı İngilizce komut; plan ile birlikte dolu/boş (değişmez).';
COMMENT ON COLUMN animation_job.plan                IS 'Onaylanmış hareket planı (JSON nesnesi) (değişmez).';
COMMENT ON COLUMN animation_job.plan_schema_version IS 'Plan JSON şema sürümü (değişmez).';
COMMENT ON COLUMN animation_job.plan_approved_at    IS 'Kullanıcının planı onayladığı an (değişmez).';
COMMENT ON COLUMN animation_job.seed                IS 'Üretim tohumu (değişmez).';
COMMENT ON COLUMN animation_job.inference_params    IS 'Üretimde kullanılan çıkarım parametreleri anlık görüntüsü (değişmez).';
COMMENT ON COLUMN animation_job.start_asset_id      IS 'Başlangıç çizimi (aynı sahibe ait; değişmez).';
COMMENT ON COLUMN animation_job.end_asset_id        IS 'Bitiş çizimi (aynı sahibe ait; değişmez).';
COMMENT ON COLUMN animation_job.thumbnail_asset_id  IS 'İsteğe bağlı küçük resim varlığı.';
COMMENT ON COLUMN animation_job.video_asset_id      IS 'Sonuç MP4; yalnız done durumunda dolu.';
COMMENT ON COLUMN animation_job.frames_asset_id     IS 'Üretilen ara karelerin tek arşivi (ZIP, PNG kareleri; karar D-09); yalnız done durumunda dolu.';
COMMENT ON COLUMN animation_job.frame_count         IS 'Arşivdeki kare sayısı (2..16; ilk ve son kare girdi çizimleridir); yalnız done durumunda dolu.';
COMMENT ON COLUMN animation_job.model_version_id    IS 'İşçinin kapma anında kaydettiği model sürümü.';
COMMENT ON COLUMN animation_job.locked_by           IS 'Kapan işçi örneği etiketi.';
COMMENT ON COLUMN animation_job.heartbeat_at        IS 'İşçinin son canlılık işareti (running iken).';
COMMENT ON COLUMN animation_job.created_at          IS 'Gönderim zamanı (UTC).';
COMMENT ON COLUMN animation_job.started_at          IS 'Kapma zamanı (UTC).';
COMMENT ON COLUMN animation_job.finished_at         IS 'Terminal duruma geçiş zamanı (UTC).';
COMMENT ON COLUMN animation_job.error_code          IS 'Makine okunur hata kodu; yalnız failed durumunda.';
COMMENT ON COLUMN animation_job.error_message       IS 'Kullanıcıya gösterilebilir hata iletisi; yalnız failed durumunda.';
-- Cue 0002_roles_and_grants (UP): en az yetkili uygulama rolleri (NOLOGIN grup rolleri).
-- Giriş yapabilen hesaplar dağıtım adımında bu rollere üye yapılır; parola burada TANIMLANMAZ.
-- Rol nesneleri küme genelindedir: CREATE ROLE tekrar çalıştırılabilir olsun diye koşullu.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'cue_api')         THEN CREATE ROLE cue_api         NOLOGIN; END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'cue_worker')      THEN CREATE ROLE cue_worker      NOLOGIN; END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'cue_maintenance') THEN CREATE ROLE cue_maintenance NOLOGIN; END IF;
END $$;

REVOKE ALL ON app_user, auth_session, model_version, media_asset, animation_job FROM PUBLIC;

-- API: kullanıcı kaydı/girişi, yükleme, iş gönderme, iptal, silme
GRANT SELECT, INSERT                     ON app_user      TO cue_api;               -- DELETE yok: hesap silme operatör işi
GRANT SELECT, INSERT, DELETE             ON auth_session  TO cue_api;
GRANT UPDATE (last_seen_at)              ON auth_session  TO cue_api;
GRANT SELECT                             ON model_version TO cue_api;
GRANT SELECT, INSERT, DELETE             ON media_asset   TO cue_api;
GRANT SELECT, INSERT, DELETE             ON animation_job TO cue_api;
GRANT UPDATE (status, finished_at)       ON animation_job TO cue_api;               -- yalnız iptal

-- İşçi: kapma, heartbeat, tamamlama/hata; girdiler ve kullanıcı kimlik bilgisi okunamaz
GRANT SELECT                             ON model_version TO cue_worker;
GRANT SELECT, INSERT                     ON media_asset   TO cue_worker;
GRANT SELECT                             ON animation_job TO cue_worker;
GRANT UPDATE (status, started_at, finished_at, heartbeat_at, locked_by,
              model_version_id, video_asset_id, frames_asset_id, frame_count, error_code, error_message)
                                         ON animation_job TO cue_worker;

-- Bakım: takılı iş, bağlanmamış yükleme, süresi dolmuş oturum
GRANT SELECT, DELETE                     ON auth_session  TO cue_maintenance;
GRANT SELECT, DELETE                     ON media_asset   TO cue_maintenance;
GRANT SELECT                             ON animation_job TO cue_maintenance;
GRANT UPDATE (status, finished_at, error_code, error_message)
                                         ON animation_job TO cue_maintenance;
