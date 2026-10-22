-- OPSİYONEL ÖNERİ (migration DEĞİL, uygulanmadı): satır düzeyi güvenlik (RLS), karar D-06.
-- Uygulama sözleşmesi: her API işleminde `SET LOCAL app.user_id = '<oturum kullanıcısı>'` (havuzlu bağlantıda yalnız SET LOCAL kullanılır).
-- Ayar yoksa ya da boş dizgeyse NULL döner -> koşul NULL -> satır görünmez (başarısızlıkta kapanma).
-- auth_session ve app_user için RLS YOKTUR: belirteç/e-posta ile arama, kullanıcı bilinmeden yapılır (kimlik doğrulamanın kendisi).
-- Tablo sahibi ve süper kullanıcı RLS'yi atlar: uygulama bu rollerle BAĞLANMAMALIDIR (cue_api/cue_worker/cue_maintenance sahip değildir).
CREATE FUNCTION app_current_user() RETURNS uuid LANGUAGE sql STABLE AS
$$ SELECT NULLIF(current_setting('app.user_id', true), '')::uuid $$;
GRANT EXECUTE ON FUNCTION app_current_user() TO cue_api;

ALTER TABLE animation_job ENABLE ROW LEVEL SECURITY;
ALTER TABLE animation_job FORCE ROW LEVEL SECURITY;
ALTER TABLE media_asset   ENABLE ROW LEVEL SECURITY;
ALTER TABLE media_asset   FORCE ROW LEVEL SECURITY;

CREATE POLICY job_api   ON animation_job TO cue_api USING (owner_id = app_current_user()) WITH CHECK (owner_id = app_current_user());
CREATE POLICY asset_api ON media_asset   TO cue_api USING (owner_id = app_current_user()) WITH CHECK (owner_id = app_current_user());
-- İşçi ve bakım kullanıcıdan bağımsız çalışır (kuyruk tüm sahiplere hizmet verir); yetkileri zaten sütun/tablo düzeyinde kısıtlı.
CREATE POLICY job_worker   ON animation_job TO cue_worker      USING (true) WITH CHECK (true);
CREATE POLICY asset_worker ON media_asset   TO cue_worker      USING (true) WITH CHECK (true);
CREATE POLICY job_maint    ON animation_job TO cue_maintenance USING (true) WITH CHECK (true);
CREATE POLICY asset_maint  ON media_asset   TO cue_maintenance USING (true) WITH CHECK (true);
