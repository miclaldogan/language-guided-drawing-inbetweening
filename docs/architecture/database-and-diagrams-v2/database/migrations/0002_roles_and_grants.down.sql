-- Cue 0002 (DOWN): yetkileri geri alır; küme genelindeki roller başka veritabanlarında kullanılıyor olabilir, bu yüzden SİLİNMEZ.
REVOKE ALL ON app_user, auth_session, model_version, media_asset, animation_job FROM cue_api, cue_worker, cue_maintenance;
