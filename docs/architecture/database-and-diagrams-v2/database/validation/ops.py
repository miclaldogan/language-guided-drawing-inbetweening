"""Uygulama sözleşmesi: işçi/API/bakım SQL işlemleri (v1/07 §3 ve §5'in test edilmiş hali).
Zaman damgaları için now() DEĞİL clock_timestamp() kullanılır (bkz. reports/02 bulgu F-01)."""

CLAIM = """
WITH next AS (
    SELECT id FROM animation_job WHERE status = 'queued'
    ORDER BY created_at, id FOR UPDATE SKIP LOCKED LIMIT 1)
UPDATE animation_job j
SET    status = 'running', started_at = clock_timestamp(), heartbeat_at = clock_timestamp(),
       locked_by = %(worker)s, model_version_id = mv.id
FROM   next, (SELECT id FROM model_version WHERE is_active) mv
WHERE  j.id = next.id
RETURNING j.id
"""

# v1/07 §5 Q3 biçimi (alt sorguda SKIP LOCKED, UPDATE...FROM) — karşılaştırma için
CLAIM_V1 = """
UPDATE animation_job j
SET    status = 'running', started_at = clock_timestamp(), heartbeat_at = clock_timestamp(),
       locked_by = %(worker)s, model_version_id = mv.id
FROM   (SELECT id FROM model_version WHERE is_active) mv
WHERE  j.id = (SELECT id FROM animation_job WHERE status = 'queued'
               ORDER BY created_at, id FOR UPDATE SKIP LOCKED LIMIT 1)
RETURNING j.id
"""

HEARTBEAT = "UPDATE animation_job SET heartbeat_at = clock_timestamp() WHERE id = %s AND status = 'running' AND locked_by = %s"

INSERT_VIDEO = ("INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,width,height,sha256) "
                "VALUES (%s,'result_video',%s,'video/mp4',5000,512,320,%s) RETURNING id")
INSERT_FRAMES = ("INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,width,height,sha256) "
                 "VALUES (%s,'frames_archive',%s,'application/zip',20000,512,320,%s) RETURNING id")
COMPLETE = ("UPDATE animation_job SET status='done', finished_at=clock_timestamp(), video_asset_id=%s, frames_asset_id=%s, frame_count=%s "
            "WHERE id=%s AND status='running' AND locked_by=%s")
FAIL = ("UPDATE animation_job SET status='failed', finished_at=clock_timestamp(), error_code=%s, error_message=%s "
        "WHERE id=%s AND status='running' AND locked_by=%s")
CANCEL = ("UPDATE animation_job SET status='cancelled', finished_at=clock_timestamp() "
          "WHERE id=%s AND owner_id=%s AND status IN ('queued','running')")
REAP = ("UPDATE animation_job SET status='failed', finished_at=clock_timestamp(), error_code='worker_lost', "
        "error_message='The generation was interrupted.' "
        "WHERE status='running' AND heartbeat_at < clock_timestamp() - make_interval(secs => %s) RETURNING id")
SUBMIT = ("INSERT INTO animation_job(owner_id,idempotency_key,seed,start_asset_id,end_asset_id) VALUES (%s,%s,1,%s,%s) "
          "ON CONFLICT (owner_id, idempotency_key) DO NOTHING RETURNING id")


def complete(conn, job, owner, worker, storage_key, frames_key=None, frame_count=16):
    """İşçi tamamlama: kare arşivi kaydı + video kaydı + koşullu UPDATE TEK işlemde (conn autocommit=False olmalı; karar D-09).
    Koşullu UPDATE 0 satır döndürürse ROLLBACK; çağıran İKİ dosyayı da siler. True = done."""
    frames_key = frames_key or storage_key + ".frames.zip"
    try:
        vid = conn.execute(INSERT_VIDEO, (owner, storage_key, "c" * 64)).fetchone()[0]
        fid = conn.execute(INSERT_FRAMES, (owner, frames_key, "d" * 64)).fetchone()[0]
        if conn.execute(COMPLETE, (vid, fid, frame_count, job, worker)).rowcount != 1:
            conn.rollback()
            return False
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise


def claim(conn, worker, sql=CLAIM):
    """Tek deyimlik kapma + hemen commit (GPU çalışırken işlem açık kalmaz). Kapılan iş kimliği veya None."""
    row = conn.execute(sql, {"worker": worker}).fetchone()
    conn.commit()
    return row[0] if row else None


SUBMIT_LOCK = "SELECT pg_advisory_xact_lock(hashtextextended(%s::text || ':' || %s::text, 0))"


def submit(conn, owner, key, start_asset, end_asset):
    """İdempotent gönderim (bulgu F-02): (owner, key) üzerinde işlem düzeyinde advisory kilit + ON CONFLICT DO NOTHING.
    Kilit olmadan, aynı varlıklarla eşzamanlı yeniden gönderimde ON CONFLICT yalnız hakem indeksi (owner,key) için
    çalışır; asset benzersiz indeksleri önce çakışıp UniqueViolation fırlatabilir.
    conn autocommit=False olmalı. Dönüş: (job_id, created: bool)."""
    conn.execute(SUBMIT_LOCK, (owner, key))
    row = conn.execute(SUBMIT, (owner, key, start_asset, end_asset)).fetchone()
    if row:
        conn.commit()
        return row[0], True
    existing = conn.execute("SELECT id FROM animation_job WHERE owner_id=%s AND idempotency_key=%s", (owner, key)).fetchone()[0]
    conn.commit()
    return existing, False
