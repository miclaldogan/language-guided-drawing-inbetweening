"""Eşzamanlılık ve çökme senaryoları: SKIP LOCKED kapma, heartbeat, koşullu geçişler, geç sonuç, idempotency."""
import threading, time, uuid
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import pytest
from psycopg import errors as E
import ops


def seed_jobs(db, n):
    u = db.user(); db.model()
    return u, [db.job(u) for _ in range(n)]


@pytest.mark.parametrize("claim_sql", [ops.CLAIM, ops.CLAIM_V1], ids=["cte", "v1-update-from"])
def test_many_workers_never_claim_same_job(db, claim_sql):
    N, W = 200, 8
    u, jobs = seed_jobs(db, N)
    claims = []
    lock = threading.Lock()

    def worker(i):
        c = db.conn("cue_worker", autocommit=False)
        mine = []
        while True:
            jid = ops.claim(c, f"w{i}", claim_sql)
            if jid is None:
                break
            mine.append(jid)
        with lock:
            claims.extend((jid, f"w{i}") for jid in mine)
        c.close()

    with ThreadPoolExecutor(W) as ex:
        list(ex.map(worker, range(W)))
    ids = [j for j, _ in claims]
    assert len(ids) == N and len(set(ids)) == N, "çift kapma veya kapılmayan iş"
    assert set(ids) == set(jobs)
    rows = db.su.execute("SELECT status, count(*) FROM animation_job GROUP BY status").fetchall()
    assert rows == [("running", N)]
    # kayıtlı locked_by, kapan işçiyle aynı
    owner_of = dict(claims)
    for jid, lb in db.su.execute("SELECT id, locked_by FROM animation_job").fetchall():
        assert owner_of[jid] == lb
    used = {w for _, w in claims}
    assert len(used) > 1, "yük tek işçide kaldı; yarış gerçekten sınanmadı"


def test_claim_returns_connection_to_idle_not_in_transaction(db):
    """Kapma işlemi hemen kapanır: işçi GPU çalışırken 'idle in transaction' DEĞİL."""
    u, jobs = seed_jobs(db, 1)
    w = db.conn("cue_worker", autocommit=False)
    ops.claim(w, "w1")
    pid = w.info.backend_pid
    state = db.su.execute("SELECT state FROM pg_stat_activity WHERE pid=%s", (pid,)).fetchone()[0]
    assert state == "idle"


def test_fifo_order_without_contention(db):
    u, jobs = seed_jobs(db, 5)
    c = db.conn("cue_worker", autocommit=False)
    got = [ops.claim(c, "w") for _ in range(5)]
    assert got == sorted(jobs, key=lambda j: db.su.execute("SELECT created_at,id FROM animation_job WHERE id=%s", (j,)).fetchone())


def test_no_active_model_means_no_claim(db):
    u = db.user(); db.job(u)
    c = db.conn("cue_worker", autocommit=False)
    assert ops.claim(c, "w") is None
    assert db.su.execute("SELECT status FROM animation_job").fetchone()[0] == "queued"


def test_crash_before_claim_commit_releases_job(db):
    """İşçi kapma işlemi commit olmadan ölürse iş kuyrukta kalır; diğer işçi başka işi atlayarak alır, ölünce geri döner."""
    u, jobs = seed_jobs(db, 2)
    a = db.conn("cue_worker", autocommit=False)
    first = a.execute(ops.CLAIM, {"worker": "dead"}).fetchone()[0]       # commit YOK
    b = db.conn("cue_worker", autocommit=False)
    second = ops.claim(b, "alive")
    assert second != first                                              # kilitli satır atlandı
    db.su.execute("SELECT pg_terminate_backend(%s)", (a.info.backend_pid,))
    time.sleep(0.3)
    third = ops.claim(b, "alive")
    assert third == first                                               # kilit düştü, iş kaybolmadı
    assert {second, third} == set(jobs)


def test_crash_after_commit_is_recovered_by_reaper_and_late_result_is_rejected(db):
    u, jobs = seed_jobs(db, 1)
    w = db.conn("cue_worker", autocommit=False)
    j = ops.claim(w, "w-dead")
    db.su.execute("UPDATE animation_job SET heartbeat_at = clock_timestamp() - interval '20 minutes' WHERE id=%s", (j,))
    m = db.conn("cue_maintenance")
    reaped = m.execute(ops.REAP, (900,)).fetchall()
    assert [r[0] for r in reaped] == [j]
    st = db.su.execute("SELECT status,error_code,finished_at IS NOT NULL FROM animation_job WHERE id=%s", (j,)).fetchone()
    assert st == ("failed", "worker_lost", True)
    # "ölü" sanılan işçi aslında canlı: geç tamamlama reddedilmeli, video kaydı kalmamalı
    ok = ops.complete(w, j, u, "w-dead", f"assets/{uuid.uuid4().hex}")
    assert ok is False
    assert db.su.execute("SELECT status,video_asset_id,frames_asset_id FROM animation_job WHERE id=%s", (j,)).fetchone() == ("failed", None, None)
    assert db.su.execute("SELECT count(*) FROM media_asset WHERE kind IN ('result_video','frames_archive')").fetchone()[0] == 0


def test_reaper_ignores_fresh_heartbeat(db):
    u, jobs = seed_jobs(db, 1)
    w = db.conn("cue_worker", autocommit=False)
    j = ops.claim(w, "w")
    m = db.conn("cue_maintenance")
    assert m.execute(ops.REAP, (900,)).fetchall() == []
    assert w.execute(ops.HEARTBEAT, (j, "w")).rowcount == 1
    assert w.execute(ops.HEARTBEAT, (j, "other-worker")).rowcount == 0     # yanlış işçi


def test_cancel_then_worker_cannot_complete_or_heartbeat(db):
    u, jobs = seed_jobs(db, 1)
    w = db.conn("cue_worker", autocommit=False)
    j = ops.claim(w, "w")
    api = db.conn("cue_api")
    assert api.execute(ops.CANCEL, (j, u)).rowcount == 1
    assert w.execute(ops.HEARTBEAT, (j, "w")).rowcount == 0; w.commit()
    assert ops.complete(w, j, u, "w", "assets/late") is False
    assert db.su.execute("SELECT status,video_asset_id,frames_asset_id FROM animation_job WHERE id=%s", (j,)).fetchone() == ("cancelled", None, None)
    assert db.su.execute("SELECT count(*) FROM media_asset WHERE storage_key LIKE 'assets/late%%'").fetchone()[0] == 0
    # terminal duruma ikinci iptal / başarısızlık de uygulanmaz
    assert api.execute(ops.CANCEL, (j, u)).rowcount == 0
    assert w.execute(ops.FAIL, ("generation_failed", "x", j, "w")).rowcount == 0


def test_cancel_by_other_user_has_no_effect(db):
    u, jobs = seed_jobs(db, 1)
    other = db.user()
    api = db.conn("cue_api")
    assert api.execute(ops.CANCEL, (jobs[0], other)).rowcount == 0
    assert db.su.execute("SELECT status FROM animation_job").fetchone()[0] == "queued"


def test_cancel_queued_job_is_never_claimed(db):
    u, jobs = seed_jobs(db, 1)
    db.conn("cue_api").execute(ops.CANCEL, (jobs[0], u))
    assert ops.claim(db.conn("cue_worker", autocommit=False), "w") is None


def test_cancel_vs_complete_race_has_consistent_final_state(db):
    outcomes = Counter()
    for trial in range(40):
        u = db.user(); db.su.execute("UPDATE model_version SET is_active=false")
        db.model(); j = db.job(u)
        w = db.conn("cue_worker", autocommit=False); api = db.conn("cue_api")
        assert ops.claim(w, "w") == j
        barrier = threading.Barrier(2)
        res = {}

        def do_cancel():
            barrier.wait(); res["cancel"] = api.execute(ops.CANCEL, (j, u)).rowcount

        def do_complete():
            barrier.wait(); res["complete"] = ops.complete(w, j, u, "w", f"assets/{uuid.uuid4().hex}")

        ts = [threading.Thread(target=do_cancel), threading.Thread(target=do_complete)]
        [t.start() for t in ts]; [t.join() for t in ts]
        st, vid, frs = db.su.execute("SELECT status, video_asset_id, frames_asset_id FROM animation_job WHERE id=%s", (j,)).fetchone()
        outs = db.su.execute("SELECT count(*) FROM media_asset WHERE owner_id=%s AND kind IN ('result_video','frames_archive')", (u,)).fetchone()[0]
        if st == "done":
            assert res == {"cancel": 0, "complete": True} and vid is not None and frs is not None and outs == 2
        else:
            assert st == "cancelled" and res == {"cancel": 1, "complete": False} and vid is None and frs is None and outs == 0
        outcomes[st] += 1
    print("race outcomes:", dict(outcomes))
    assert sum(outcomes.values()) == 40


def test_now_vs_clock_timestamp_hazard(db):
    """F-01: now() işlem BAŞLANGIÇ zamanıdır. Önce başlayan bir iptal işlemi, sonradan commit olan kapmanın
    started_at'inden ESKİ bir finished_at yazıp CHECK'e takılabilir. clock_timestamp() bunu önler."""
    u, jobs = seed_jobs(db, 1)
    api = db.conn("cue_api", autocommit=False)
    api.execute("SELECT 1")                                             # işlem (ve now()) burada başlar
    time.sleep(0.05)
    w = db.conn("cue_worker", autocommit=False)
    j = ops.claim(w, "w")                                               # started_at > api'nin now()'ı
    with pytest.raises(E.CheckViolation) as ei:
        api.execute("UPDATE animation_job SET status='cancelled', finished_at=now() WHERE id=%s AND status IN ('queued','running')", (j,))
    assert ei.value.diag.constraint_name == "animation_job_finished_after_started"
    api.rollback()
    api.execute("SELECT 1")
    time.sleep(0.05)
    w2 = db.conn("cue_worker", autocommit=False)
    assert api.execute("UPDATE animation_job SET status='cancelled', finished_at=clock_timestamp() WHERE id=%s AND status IN ('queued','running')", (j,)).rowcount == 1
    api.commit()


def test_idempotent_submit_under_concurrency(db):
    u = db.user(); key = uuid.uuid4()
    s, e = db.asset(u), db.asset(u, "end_drawing")

    def submit(_):
        c = db.conn("cue_api", autocommit=False)
        return ops.submit(c, u, key, s, e)

    with ThreadPoolExecutor(10) as ex:
        results = list(ex.map(submit, range(10)))
    assert Counter(c for _, c in results) == {True: 1, False: 9}
    assert len({i for i, _ in results}) == 1
    assert db.su.execute("SELECT count(*) FROM animation_job").fetchone()[0] == 1


def test_f02_plain_on_conflict_is_not_sufficient_under_concurrency(db):
    """F-02 kanıtı (olasılıksal): kilitsiz ON CONFLICT ile eşzamanlı yeniden gönderimlerde bazı denemeler
    asset-indeksi UniqueViolation'ı alabilir. Hiç görülmezse test bilgi amaçlı geçer; görülürse bulgu doğrulanmış olur."""
    seen = Counter()
    for _ in range(25):
        u = db.user(); key = uuid.uuid4()
        s, e = db.asset(u), db.asset(u, "end_drawing")
        def raw(_):
            c = db.conn("cue_api", autocommit=False)
            try:
                row = c.execute(ops.SUBMIT, (u, key, s, e)).fetchone(); c.commit()
                return "created" if row else "existing"
            except E.UniqueViolation as ex:
                c.rollback(); return "unique:" + ex.diag.constraint_name
        with ThreadPoolExecutor(10) as ex:
            seen.update(ex.map(raw, range(10)))
        assert db.su.execute("SELECT count(*) FROM animation_job WHERE owner_id=%s", (u,)).fetchone()[0] == 1  # veri yine tutarlı
    print("F-02 plain ON CONFLICT outcomes:", dict(seen))


def test_idempotency_key_is_scoped_per_owner(db):
    a, b = db.user(), db.user(); key = uuid.uuid4()
    db.job(a, key=key); db.job(b, key=key)      # farklı sahip: aynı anahtar çakışmaz
    with pytest.raises(E.UniqueViolation):
        db.job(a, key=key)


def test_active_job_cap_query_is_consistent(db):
    """D-07 için: kullanıcı başına etkin iş sayımı sahip indeksiyle yapılabilir (kısıt değil, servis kuralı)."""
    u = db.user(); db.model()
    for _ in range(3):
        db.job(u)
    n = db.conn("cue_api").execute("SELECT count(*) FROM animation_job WHERE owner_id=%s AND status IN ('queued','running')", (u,)).fetchone()[0]
    assert n == 3
