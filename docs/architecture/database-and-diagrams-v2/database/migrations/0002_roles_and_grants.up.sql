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
