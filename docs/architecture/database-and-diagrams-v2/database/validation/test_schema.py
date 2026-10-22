"""Şema doğrulama: anahtarlar, bileşik sahiplik FK'si, CHECK matrisi, benzersizlik, silme davranışı, indeksler."""
import uuid
import psycopg
import pytest
from psycopg import errors as E
from conftest import ARGON

EXPECTED_INDEXES = {
    "app_user_pkey", "app_user_email_key",
    "auth_session_pkey", "auth_session_token_hash_key", "auth_session_user_id_idx",
    "model_version_pkey", "model_version_name_label_key", "model_version_single_active_idx",
    "media_asset_pkey", "media_asset_storage_key_key", "media_asset_id_owner_key", "media_asset_owner_id_idx",
    "animation_job_pkey", "animation_job_owner_created_idx", "animation_job_queue_idx", "animation_job_running_hb_idx",
    "animation_job_owner_idem_key", "animation_job_start_asset_key", "animation_job_end_asset_key",
    "animation_job_video_asset_key", "animation_job_frames_asset_key", "animation_job_thumb_asset_key",
}


def test_tables_and_indexes_exactly_as_specified(db):
    tables = {r[0] for r in db.su.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")}
    assert tables == {"app_user", "auth_session", "model_version", "media_asset", "animation_job"}
    idx = {r[0] for r in db.su.execute("SELECT indexname FROM pg_indexes WHERE schemaname='public'")}
    assert idx == EXPECTED_INDEXES


def test_valid_relationships_insert(db):
    u = db.user(); m = db.model()
    j = db.job(u, plan=True)
    assert db.su.execute("SELECT status FROM animation_job WHERE id=%s", (j,)).fetchone()[0] == "queued"
    s = db.su.execute("INSERT INTO auth_session(user_id,token_hash,expires_at) VALUES (%s,%s, now()+interval '7 days') RETURNING id",
                      (u, b"x" * 32)).fetchone()
    assert s


def test_composite_fk_rejects_other_owners_assets(db):
    a, b = db.user(), db.user()
    foreign = db.asset(b)
    mine = db.asset(a, "end_drawing")
    with pytest.raises(E.ForeignKeyViolation):
        db.su.execute("INSERT INTO animation_job(owner_id,idempotency_key,seed,start_asset_id,end_asset_id) VALUES (%s,%s,1,%s,%s)",
                      (a, uuid.uuid4(), foreign, mine))
    # çıktı varlıkları için de geçerli
    m = db.model()
    j = db.job(a)
    other_video, other_frames = db.asset(b, "result_video"), db.asset(b, "frames_archive")
    my_video, my_frames = db.asset(a, "result_video"), db.asset(a, "frames_archive")
    done = ("UPDATE animation_job SET status='done',started_at=clock_timestamp(),finished_at=clock_timestamp(),"
            "model_version_id=%s,video_asset_id=%s,frames_asset_id=%s,frame_count=16 WHERE id=%s")
    with pytest.raises(E.ForeignKeyViolation):   # durum CHECK'lerini sağlayan geçerli 'done' + başkasının videosu
        db.su.execute(done, (m, other_video, my_frames, j))
    with pytest.raises(E.ForeignKeyViolation):   # ... ve başkasının kare arşivi
        db.su.execute(done, (m, my_video, other_frames, j))


def test_asset_cannot_be_reused_and_inputs_distinct(db):
    u = db.user(); j1 = db.job(u)
    s, e = db.su.execute("SELECT start_asset_id,end_asset_id FROM animation_job WHERE id=%s", (j1,)).fetchone()
    e2 = db.asset(u, "end_drawing")
    with pytest.raises(E.UniqueViolation):  # aynı başlangıç varlığı ikinci işte
        db.su.execute("INSERT INTO animation_job(owner_id,idempotency_key,seed,start_asset_id,end_asset_id) VALUES (%s,%s,1,%s,%s)",
                      (u, uuid.uuid4(), s, e2))
    s3 = db.asset(u)
    with pytest.raises(E.CheckViolation):  # start == end
        db.su.execute("INSERT INTO animation_job(owner_id,idempotency_key,seed,start_asset_id,end_asset_id) VALUES (%s,%s,1,%s,%s)",
                      (u, uuid.uuid4(), s3, s3))


def test_known_gap_same_asset_start_in_one_job_end_in_another(db):
    """Belgelenmiş bilinen sınır (v1/07 §2): DB, bir varlığın bir işte start başka işte end olmasını engellemez; servis/test engeller."""
    u = db.user(); j1 = db.job(u)
    s1 = db.su.execute("SELECT start_asset_id FROM animation_job WHERE id=%s", (j1,)).fetchone()[0]
    s2 = db.asset(u)
    db.su.execute("INSERT INTO animation_job(owner_id,idempotency_key,seed,start_asset_id,end_asset_id) VALUES (%s,%s,1,%s,%s)",
                  (u, uuid.uuid4(), s2, s1))  # s1 başka işte start; burada end → DB izin verir


def test_email_and_password_constraints(db):
    with pytest.raises(E.CheckViolation):
        db.su.execute("INSERT INTO app_user(email,password_hash) VALUES ('Upper@Example.test',%s)", (ARGON,))
    with pytest.raises(E.CheckViolation):
        db.su.execute("INSERT INTO app_user(email,password_hash) VALUES ('a@example.test','plaintext-password')")
    with pytest.raises(E.CheckViolation):
        db.su.execute("INSERT INTO app_user(email,password_hash) VALUES ('b@example.test','$2b$12$abcdefghijklmnopqrstuv')")  # bcrypt
    db.user("dup@example.test")
    with pytest.raises(E.UniqueViolation):
        db.user("dup@example.test")


def test_session_constraints(db):
    u = db.user()
    with pytest.raises(E.CheckViolation):
        db.su.execute("INSERT INTO auth_session(user_id,token_hash,expires_at) VALUES (%s,%s,now()+interval '1 day')", (u, b"short"))
    with pytest.raises(E.CheckViolation):
        db.su.execute("INSERT INTO auth_session(user_id,token_hash,expires_at) VALUES (%s,%s,now()-interval '1 day')", (u, b"y" * 32))
    db.su.execute("INSERT INTO auth_session(user_id,token_hash,expires_at) VALUES (%s,%s,now()+interval '1 day')", (u, b"z" * 32))
    with pytest.raises(E.UniqueViolation):
        db.su.execute("INSERT INTO auth_session(user_id,token_hash,expires_at) VALUES (%s,%s,now()+interval '1 day')", (u, b"z" * 32))


def test_single_active_model_version(db):
    db.model(active=True)
    db.model(active=False)
    with pytest.raises(E.UniqueViolation):
        db.model(active=True)


def test_media_asset_constraints(db):
    u = db.user()
    base = dict(owner=u, key=lambda: f"assets/{uuid.uuid4().hex}")
    def ins(kind="start_drawing", ct="image/png", size=1, sha="a" * 64, w=1, h=1, key=None):
        db.su.execute("INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,width,height,sha256) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                      (u, kind, key or base["key"](), ct, size, w, h, sha))
    ins()
    for kw in [dict(kind="bogus"), dict(ct="image/gif"), dict(kind="result_video", ct="image/png"),
               dict(kind="start_drawing", ct="video/mp4"), dict(size=0), dict(w=0), dict(sha="xyz")]:
        with pytest.raises(E.CheckViolation):
            ins(**kw)
    ins(key="same")
    with pytest.raises(E.UniqueViolation):
        ins(key="same")


# ---- animation_job CHECK matrisi: her satır (ad, değişiklik) reddedilmeli ------------------------------------------
BAD_UPDATES = [
    ("animation_job_status_valid", "status='bogus'"),
    ("animation_job_plan_group", "command_text=NULL"),                       # komut yok, plan var (plan=True işi)
    ("animation_job_plan_group", "plan_approved_at=NULL"),
    ("animation_job_plan_group", "plan_schema_version=NULL"),
    ("animation_job_plan_object", "plan='[]'::jsonb"),
    ("animation_job_params_object", "inference_params='[]'::jsonb"),
    ("animation_job_command_len", "command_text=''"),
    ("animation_job_command_len", "command_text=repeat('x',1001)"),
    ("animation_job_state_queued", "started_at=now()"),
    ("animation_job_state_queued", "locked_by='w'"),
    ("animation_job_state_done", "status='done'"),                           # video/model/zamanlar yok
    ("animation_job_state_failed", "status='failed', finished_at=now()"),    # hata kodu yok
    ("animation_job_state_cancelled", "status='cancelled'"),                 # finished_at yok
    ("animation_job_state_running", "status='running', started_at=now()"),   # locked_by/heartbeat/model yok
    ("animation_job_started_after_created", "started_at=created_at - interval '1 second'"),
    ("animation_job_frame_count_range", "frame_count=17"),
    ("animation_job_frames_pair", "frame_count=8"),                            # arşiv yok, sayı var
]


@pytest.mark.parametrize("constraint,assignment", BAD_UPDATES)
def test_job_check_matrix(db, constraint, assignment):
    u = db.user(); j = db.job(u, plan=True)
    with pytest.raises(E.CheckViolation) as ei:
        db.su.execute(f"UPDATE animation_job SET {assignment} WHERE id=%s", (j,))
    assert ei.value.diag.constraint_name == constraint


def test_job_valid_state_rows(db):
    u = db.user(); m = db.model()
    # running
    j = db.job(u)
    db.su.execute("UPDATE animation_job SET status='running',started_at=clock_timestamp(),heartbeat_at=now(),locked_by='w1',model_version_id=%s WHERE id=%s", (m, j))
    # done
    v, fr = db.asset(u, "result_video"), db.asset(u, "frames_archive")
    db.su.execute("UPDATE animation_job SET status='done',finished_at=clock_timestamp(),video_asset_id=%s,frames_asset_id=%s,frame_count=16 WHERE id=%s", (v, fr, j))
    # failed (kuyruktan doğrudan da geçerli)
    j2 = db.job(u)
    db.su.execute("UPDATE animation_job SET status='failed',finished_at=clock_timestamp(),error_code='x',error_message='y' WHERE id=%s", (j2,))
    # cancelled
    j3 = db.job(u)
    db.su.execute("UPDATE animation_job SET status='cancelled',finished_at=clock_timestamp() WHERE id=%s", (j3,))
    with pytest.raises(E.CheckViolation):  # cancelled iş video taşıyamaz
        db.su.execute("UPDATE animation_job SET video_asset_id=%s WHERE id=%s", (db.asset(u, "result_video"), j3))


def test_deletion_behaviour(db):
    u = db.user(); j = db.job(u)
    with pytest.raises(E.RestrictViolation):     # kullanıcı: iş/varlık varken silinemez (ON DELETE RESTRICT)
        db.su.execute("DELETE FROM app_user WHERE id=%s", (u,))
    with pytest.raises(E.ForeignKeyViolation):   # varlık: işe bağlıyken silinemez (NO ACTION)
        db.su.execute("DELETE FROM media_asset WHERE id=(SELECT start_asset_id FROM animation_job WHERE id=%s)", (j,))
    # belgelenen silme sırası: iş → varlıklar → kullanıcı
    ids = db.su.execute("DELETE FROM animation_job WHERE id=%s RETURNING start_asset_id,end_asset_id", (j,)).fetchone()
    db.su.execute("DELETE FROM media_asset WHERE id = ANY(%s)", (list(ids),))
    db.su.execute("DELETE FROM app_user WHERE id=%s", (u,))
    # yalnız oturumu olan kullanıcı CASCADE ile silinir
    u2 = db.user()
    db.su.execute("INSERT INTO auth_session(user_id,token_hash,expires_at) VALUES (%s,%s,now()+interval '1 day')", (u2, b"q" * 32))
    db.su.execute("DELETE FROM app_user WHERE id=%s", (u2,))
    assert db.su.execute("SELECT count(*) FROM auth_session").fetchone()[0] == 0
    # model sürümü işte kullanılıyorsa silinemez
    m = db.model(); u3 = db.user(); j3 = db.job(u3)
    db.su.execute("UPDATE animation_job SET status='running',started_at=clock_timestamp(),heartbeat_at=now(),locked_by='w',model_version_id=%s WHERE id=%s", (m, j3))
    with pytest.raises(E.RestrictViolation):
        db.su.execute("DELETE FROM model_version WHERE id=%s", (m,))


def test_account_deletion_procedure_in_one_transaction(db):
    """Operatör prosedürü (BP-14): iş → varlık → oturum → kullanıcı sırası tek işlemde başarılı."""
    u = db.user(); db.job(u); db.job(u, plan=True)
    db.su.execute("INSERT INTO auth_session(user_id,token_hash,expires_at) VALUES (%s,%s,now()+interval '1 day')", (u, b"k" * 32))
    with db.su.transaction():
        db.su.execute("DELETE FROM animation_job WHERE owner_id=%s", (u,))
        keys = db.su.execute("DELETE FROM media_asset WHERE owner_id=%s RETURNING storage_key", (u,)).fetchall()
        db.su.execute("DELETE FROM app_user WHERE id=%s", (u,))
    assert len(keys) == 4
    assert db.su.execute("SELECT count(*) FROM app_user").fetchone()[0] == 0


@pytest.mark.parametrize("name,sql,index", [
    ("owner list keyset", "SELECT id FROM animation_job WHERE owner_id=%(o)s AND (created_at,id) < (now(), %(i)s) ORDER BY created_at DESC, id DESC LIMIT 20", "animation_job_owner_created_idx"),
    ("worker claim order", "SELECT id FROM animation_job WHERE status='queued' ORDER BY created_at,id LIMIT 1", "animation_job_queue_idx"),
    ("stale running", "SELECT id FROM animation_job WHERE status='running' AND heartbeat_at < now()", "animation_job_running_hb_idx"),
    ("idempotency lookup", "SELECT id FROM animation_job WHERE owner_id=%(o)s AND idempotency_key=%(i)s", "animation_job_owner_idem_key"),
    ("session by token", "SELECT user_id FROM auth_session WHERE token_hash=%(b)s", "auth_session_token_hash_key"),
    ("email lookup", "SELECT id FROM app_user WHERE email='x@example.test'", "app_user_email_key"),
])
def test_indexes_are_usable_for_access_paths(db, name, sql, index):
    """Küçük tabloda planlayıcı seq scan seçebilir; burada yalnız indeksin ERİŞİM YOLU olarak kullanılabildiği gösterilir (performans iddiası değil)."""
    u = db.user()
    for _ in range(30):
        db.job(u)
    db.su.execute("ANALYZE")
    db.su.execute("SET enable_seqscan = off")
    params = dict(o=u, i=uuid.uuid4(), b=b"x" * 32)
    plan = "\n".join(r[0] for r in db.su.execute("EXPLAIN " + sql, params).fetchall())
    assert index in plan, plan


def test_command_length_boundaries_and_plan_group_valid_row(db):
    """Sınır değerleri: komut tam 1000 karakter kabul, 1001 ve boş ret; plan grubu eksiksiz satır kabul."""
    u = db.user()
    ok = db.job(u, plan=True)
    db.su.execute("UPDATE animation_job SET command_text=repeat('x',1000) WHERE id=%s", (ok,))
    with pytest.raises(E.CheckViolation) as ei:
        db.su.execute("UPDATE animation_job SET command_text=repeat('x',1001) WHERE id=%s", (ok,))
    assert ei.value.diag.constraint_name == "animation_job_command_len"
    with pytest.raises(E.CheckViolation):
        db.su.execute("UPDATE animation_job SET command_text='' WHERE id=%s", (ok,))
    # komutsuz iş (plan, onay, sürüm hepsi NULL) geçerli
    db.job(u)


def test_turkish_and_unicode_text_roundtrip_in_command_and_email(db):
    """UTF-8: komut metni Türkçe/Unicode içerse de saklanır; e-posta CHECK'i küçük harf zorlar."""
    u = db.user("çağrı.öğün@example.test")
    j = db.job(u, plan=True)
    db.su.execute("UPDATE animation_job SET command_text=%s WHERE id=%s", ("önce gözleri sola çevir, sonra başı yavaşça döndür ✓", j))
    assert "gözleri" in db.su.execute("SELECT command_text FROM animation_job WHERE id=%s", (j,)).fetchone()[0]


def test_done_requires_both_video_and_frames_archive_and_a_valid_frame_count(db):
    """Karar D-09: done iş hem MP4 hem kare arşivi taşır; kare sayısı 2..16 (ilk ve son kare girdidir)."""
    u = db.user(); m = db.model(); j = db.job(u)
    db.su.execute("UPDATE animation_job SET status='running',started_at=clock_timestamp(),heartbeat_at=now(),locked_by='w',model_version_id=%s WHERE id=%s", (m, j))
    v, fr = db.asset(u, "result_video"), db.asset(u, "frames_archive")
    base = "UPDATE animation_job SET status='done',finished_at=clock_timestamp(),video_asset_id=%s{extra} WHERE id=%s"
    with pytest.raises(E.CheckViolation) as ei:                                   # yalnız video: kare arşivi eksik
        db.su.execute(base.format(extra=""), (v, j))
    assert ei.value.diag.constraint_name == "animation_job_state_done"
    for bad in (1, 17):                                                           # aralık dışı
        with pytest.raises(E.CheckViolation) as ei:
            db.su.execute(base.format(extra=f",frames_asset_id=%s,frame_count={bad}"), (v, fr, j))
        assert ei.value.diag.constraint_name == "animation_job_frame_count_range"
    db.su.execute(base.format(extra=",frames_asset_id=%s,frame_count=2"), (v, fr, j))     # alt sınır geçerli
    # aynı arşiv ikinci işe bağlanamaz
    j2 = db.job(u)
    db.su.execute("UPDATE animation_job SET status='running',started_at=clock_timestamp(),heartbeat_at=now(),locked_by='w',model_version_id=%s WHERE id=%s", (m, j2))
    v2 = db.asset(u, "result_video")
    with pytest.raises(E.UniqueViolation):
        db.su.execute(base.format(extra=",frames_asset_id=%s,frame_count=16"), (v2, fr, j2))
    # kind/içerik türü eşleşmesi
    with pytest.raises(E.CheckViolation):
        db.su.execute("INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,sha256) VALUES (%s,'frames_archive','k1','video/mp4',1,%s)", (u, "a" * 64))
    with pytest.raises(E.CheckViolation):
        db.su.execute("INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,sha256) VALUES (%s,'start_drawing','k2','application/zip',1,%s)", (u, "a" * 64))
