-- ÖRNEK sağlama (provisioning) betiği: dağıtımda bir kez, süper kullanıcıyla çalıştırılır. PAROLA İÇERMEZ.
-- psql ile:  psql -v mig_pw="$MIG_PW" -v api_pw="$API_PW" -v worker_pw="$WORKER_PW" -v maint_pw="$MAINT_PW" -v dbname=cue -f 01_roles_and_logins.example.sql
-- Parolalar gizli yöneticiden (Docker secrets / .env, depoda DEĞİL) gelir.
-- SIRA ÖNEMLİDİR: grup rolleri migration'dan ÖNCE yaratılmalıdır (0002 yalnız GRANT eder; migration hesabı CREATEROLE sahibi değildir).
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'cue_api')         THEN CREATE ROLE cue_api         NOLOGIN; END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'cue_worker')      THEN CREATE ROLE cue_worker      NOLOGIN; END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'cue_maintenance') THEN CREATE ROLE cue_maintenance NOLOGIN; END IF;
END $$;

-- DDL sahibi: şemayı yalnız bu hesap değiştirir; uygulama hesapları tablo sahibi DEĞİLDİR (RLS ve yetki modeli buna dayanır).
CREATE ROLE cue_migrator LOGIN PASSWORD :'mig_pw' NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
CREATE ROLE cue_api_login    LOGIN PASSWORD :'api_pw'    NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS IN ROLE cue_api;
CREATE ROLE cue_worker_login LOGIN PASSWORD :'worker_pw' NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS IN ROLE cue_worker;
CREATE ROLE cue_maint_login  LOGIN PASSWORD :'maint_pw'  NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS IN ROLE cue_maintenance;

ALTER DATABASE :"dbname" OWNER TO cue_migrator;
REVOKE ALL ON DATABASE :"dbname" FROM PUBLIC;
GRANT CONNECT ON DATABASE :"dbname" TO cue_migrator, cue_api_login, cue_worker_login, cue_maint_login;
