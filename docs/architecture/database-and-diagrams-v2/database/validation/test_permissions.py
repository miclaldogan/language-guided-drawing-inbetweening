"""Sütun düzeyi yetkiler: değişmezlik ve en az yetki (trigger olmadan)."""
import uuid
import pytest
from psycopg import errors as E
from conftest import ARGON

DENIED_FOR_API = [  # (açıklama, SQL)
    ("plan", "UPDATE animation_job SET plan='{}'::jsonb"),
    ("command_text", "UPDATE animation_job SET command_text='x'"),
    ("seed", "UPDATE animation_job SET seed=7"),
    ("owner_id", "UPDATE animation_job SET owner_id=gen_random_uuid()"),
    ("start_asset_id", "UPDATE animation_job SET start_asset_id=gen_random_uuid()"),
    ("inference_params", "UPDATE animation_job SET inference_params='{}'::jsonb"),
    ("video_asset_id", "UPDATE animation_job SET video_asset_id=gen_random_uuid()"),
    ("frames_asset_id", "UPDATE animation_job SET frames_asset_id=gen_random_uuid()"),
    ("frame_count", "UPDATE animation_job SET frame_count=3"),
    ("app_user delete", "DELETE FROM app_user"),
    ("app_user update", "UPDATE app_user SET email='z@example.test'"),
    ("model_version insert", "INSERT INTO model_version(name,version_label,weights_sha256,supports_plan) VALUES ('a','b',repeat('a',64),true)"),
    ("media_asset update", "UPDATE media_asset SET byte_size=1"),
    ("DDL", "CREATE TABLE evil(x int)"),
]
DENIED_FOR_WORKER = [
    ("app_user read", "SELECT * FROM app_user"),
    ("auth_session read", "SELECT * FROM auth_session"),
    ("owner_id", "UPDATE animation_job SET owner_id=gen_random_uuid()"),
    ("plan", "UPDATE animation_job SET plan='{}'::jsonb"),
    ("seed", "UPDATE animation_job SET seed=7"),
    ("job insert", "INSERT INTO animation_job(owner_id,idempotency_key,seed,start_asset_id,end_asset_id) VALUES (gen_random_uuid(),gen_random_uuid(),1,gen_random_uuid(),gen_random_uuid())"),
    ("job delete", "DELETE FROM animation_job"),
    ("asset delete", "DELETE FROM media_asset"),
    ("model_version update", "UPDATE model_version SET is_active=false"),
]
DENIED_FOR_MAINT = [
    ("video_asset_id", "UPDATE animation_job SET video_asset_id=gen_random_uuid()"),
    ("frames_asset_id", "UPDATE animation_job SET frames_asset_id=gen_random_uuid()"),
    ("plan", "UPDATE animation_job SET plan='{}'::jsonb"),
    ("app_user read", "SELECT * FROM app_user"),
    ("job delete", "DELETE FROM animation_job"),
]


@pytest.mark.parametrize("name,sql", DENIED_FOR_API)
def test_api_denied(db, name, sql):
    c = db.conn("cue_api")
    with pytest.raises(E.InsufficientPrivilege):
        c.execute(sql)


@pytest.mark.parametrize("name,sql", DENIED_FOR_WORKER)
def test_worker_denied(db, name, sql):
    c = db.conn("cue_worker")
    with pytest.raises(E.InsufficientPrivilege):
        c.execute(sql)


@pytest.mark.parametrize("name,sql", DENIED_FOR_MAINT)
def test_maintenance_denied(db, name, sql):
    c = db.conn("cue_maintenance")
    with pytest.raises(E.InsufficientPrivilege):
        c.execute(sql)


def test_api_allowed_operations(db):
    api = db.conn("cue_api")
    uid = api.execute("INSERT INTO app_user(email,password_hash) VALUES ('new@example.test',%s) RETURNING id", (ARGON,)).fetchone()[0]
    api.execute("INSERT INTO auth_session(user_id,token_hash,expires_at) VALUES (%s,%s,now()+interval '1 day')", (uid, b"t" * 32))
    api.execute("UPDATE auth_session SET last_seen_at=now() WHERE user_id=%s", (uid,))
    a = api.execute("INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,sha256) VALUES (%s,'start_drawing','k1','image/png',1,%s) RETURNING id", (uid, "a" * 64)).fetchone()[0]
    b = api.execute("INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,sha256) VALUES (%s,'end_drawing','k2','image/png',1,%s) RETURNING id", (uid, "a" * 64)).fetchone()[0]
    j = api.execute("INSERT INTO animation_job(owner_id,idempotency_key,seed,start_asset_id,end_asset_id) VALUES (%s,%s,1,%s,%s) RETURNING id", (uid, uuid.uuid4(), a, b)).fetchone()[0]
    assert api.execute("UPDATE animation_job SET status='cancelled', finished_at=clock_timestamp() WHERE id=%s", (j,)).rowcount == 1
    api.execute("DELETE FROM animation_job WHERE id=%s", (j,))


def test_worker_allowed_operations(db):
    u = db.user(); db.model(); j = db.job(u)
    w = db.conn("cue_worker", autocommit=False)
    jid = w.execute("""WITH next AS (SELECT id FROM animation_job WHERE status='queued' ORDER BY created_at,id FOR UPDATE SKIP LOCKED LIMIT 1)
        UPDATE animation_job j SET status='running',started_at=clock_timestamp(),heartbeat_at=clock_timestamp(),locked_by='w',model_version_id=mv.id
        FROM next,(SELECT id FROM model_version WHERE is_active) mv WHERE j.id=next.id RETURNING j.id""").fetchone()
    w.commit()
    assert jid and jid[0] == j
