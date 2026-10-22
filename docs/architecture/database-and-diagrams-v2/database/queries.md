# Temsili Sorgular (uygulama sözleşmesi)

**Durum:** ÖNERİ, ONAYLANMADI. Kaynak: `database/validation/ops.py` (testlerce **çalıştırılan** biçim). Zaman damgalarında `now()` değil `clock_timestamp()` (bulgu F-01).

| Amaç | Rol | Dosya/İşlev | Doğrulayan test |
| --- | --- | --- | --- |
| İş kapma (CTE + `FOR UPDATE SKIP LOCKED`) | `cue_worker` | `ops.CLAIM` | `test_many_workers_never_claim_same_job[cte]` |
| İş kapma (v1 biçimi, alt sorgu) | `cue_worker` | `ops.CLAIM_V1` | `…[v1-update-from]` |
| Heartbeat | `cue_worker` | `ops.HEARTBEAT` | `test_reaper_ignores_fresh_heartbeat`, `test_cancel_then_worker_cannot_complete_or_heartbeat` |
| Tamamlama: kare arşivi + MP4 + koşullu UPDATE, tek işlem; 0 satır → ROLLBACK ve iki dosya silinir (D-09) | `cue_worker` | `ops.complete` | `test_cancel_vs_complete_race_has_consistent_final_state` |
| Hata | `cue_worker` | `ops.FAIL` | `test_cancel_then_worker_cannot_complete_or_heartbeat` |
| İptal | `cue_api` | `ops.CANCEL` | `test_cancel_by_other_user_has_no_effect`, `test_cancel_queued_job_is_never_claimed` |
| Takılı iş | `cue_maintenance` | `ops.REAP` | `test_crash_after_commit_is_recovered_by_reaper_and_late_result_is_rejected` |
| İdempotent gönderim (advisory kilit + ON CONFLICT) | `cue_api` | `ops.submit` | `test_idempotent_submit_under_concurrency` |
| Kitaplık (keyset) | `cue_api` | `test_schema.py::test_indexes_are_usable_for_access_paths` | aynı |
| Etkin iş sayımı (D-07) | `cue_api` | `test_active_job_cap_query_is_consistent` | aynı |
| Silme sırası / hesap silme prosedürü | operatör | `test_deletion_behaviour`, `test_account_deletion_procedure_in_one_transaction` | aynı |

| Bağlanmamış eski yükleme temizliği (iki `NOT EXISTS`) | `cue_maintenance` | `media_protocol.cleanup_unattached` | `test_unattached_uploads_cleanup_after_24h`; ölçek gözlemi `reports/08` |
| Kare sunma (S6; ZIP'ten tek PNG) | `cue_api` | `media_protocol.serve_frame` | `test_frames_archive_serves_single_frames_with_ownership_and_bounds` |
| Sahipsiz dosya süpürücü, tutarlılık raporu, silme defteri | `cue_maintenance` / operatör | `media_protocol.py` | `test_media_protocol.py` (9 test) |

## Test verisi stratejisi
- Yalnız sentetik veri: rastgele e-posta (`@example.test`), sahte Argon2id PHC dizgesi, rastgele depo anahtarları; gerçek görüntü, gerçek kullanıcı veya katılımcı verisi **yoktur**.
- Her test kendi veritabanını (`CREATE DATABASE`) ve migration'ları kurar; kapsayıcı `tmpfs` üzerinde, rastgele parolalı, yalnız `127.0.0.1`'e bağlı ve test bitince silinir.
- Çalıştırma: `database/validation/run.sh` (sürümler `tools/TOOLCHAIN.lock`).
