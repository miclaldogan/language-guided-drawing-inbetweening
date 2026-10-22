-- Cue 0001_initial (DOWN): yalnızca geliştirme/test. Üretimde yalnız ileri migration uygulanır.
DROP TABLE IF EXISTS animation_job;
DROP TABLE IF EXISTS media_asset;
DROP TABLE IF EXISTS model_version;
DROP TABLE IF EXISTS auth_session;
DROP TABLE IF EXISTS app_user;
