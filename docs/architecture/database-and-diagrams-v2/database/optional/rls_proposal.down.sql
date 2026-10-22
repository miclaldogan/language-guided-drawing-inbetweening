DROP POLICY IF EXISTS job_api ON animation_job; DROP POLICY IF EXISTS job_worker ON animation_job; DROP POLICY IF EXISTS job_maint ON animation_job;
DROP POLICY IF EXISTS asset_api ON media_asset; DROP POLICY IF EXISTS asset_worker ON media_asset; DROP POLICY IF EXISTS asset_maint ON media_asset;
ALTER TABLE animation_job NO FORCE ROW LEVEL SECURITY; ALTER TABLE animation_job DISABLE ROW LEVEL SECURITY;
ALTER TABLE media_asset NO FORCE ROW LEVEL SECURITY; ALTER TABLE media_asset DISABLE ROW LEVEL SECURITY;
DROP FUNCTION IF EXISTS app_current_user();
