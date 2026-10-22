"""v1/04 §5 hata senaryolarının dosya sistemi tarafıyla birlikte çalıştırılması + yedekten dönüş provası."""
import os, subprocess, time, uuid
import pytest
import media_protocol as mp
import ops
from conftest import connect, apply


@pytest.fixture()
def store(tmp_path):
    return mp.LocalMediaStore(tmp_path / "media")


def age(store, key, seconds):
    p = store._p(key); t = time.time() - seconds
    os.utime(p, (t, t))


def test_s1_store_failure_leaves_no_row_and_no_final_file(db, store):
    u = db.user(); api = db.conn("cue_api")
    with pytest.raises(OSError):
        mp.upload(api, store, u, "start_drawing", b"x" * 100, store_fails=True)
    assert db.su.execute("SELECT count(*) FROM media_asset").fetchone()[0] == 0
    assert store.list_keys() == []                                   # son anahtar altında yarım dosya yok


def test_s2_db_insert_failure_orphan_is_swept_only_after_grace_period(db, store):
    u = db.user(); api = db.conn("cue_api"); maint = db.conn("cue_maintenance")
    good = mp.upload(api, store, u, "start_drawing", b"g" * 100)
    from psycopg import errors as E
    with pytest.raises(E.CheckViolation):
        mp.upload(api, store, u, "end_drawing", b"o" * 100, insert_fails=True)
    assert len(store.list_keys()) == 2                                # biri sahipsiz
    assert mp.sweep_orphans(maint, store, min_age_s=3600) == []       # taze dosya (uçuştaki yükleme) KORUNUR
    orphan = [k for k, _ in store.list_keys() if k != db.su.execute("SELECT storage_key FROM media_asset").fetchone()[0]][0]
    age(store, orphan, 7200)
    assert mp.sweep_orphans(maint, store, min_age_s=3600, apply=False) == [orphan]   # rapor modu silmez
    assert store.exists(orphan)
    assert mp.sweep_orphans(maint, store, min_age_s=3600) == [orphan]
    assert len(store.list_keys()) == 1 and db.su.execute("SELECT count(*) FROM media_asset").fetchone()[0] == 1


def test_s4_late_completion_deletes_its_file_and_leaves_no_row(db, store):
    u = db.user(); db.model(); j = db.job(u)
    w = db.conn("cue_worker", autocommit=False); api = db.conn("cue_api")
    assert ops.claim(w, "w") == j
    api.execute(ops.CANCEL, (j, u))                                   # iptal, işçi hâlâ üretiyor
    key = mp.new_key("mp4"); fkey = mp.new_key("zip")
    store.put(fkey, mp.build_frames_zip()); store.put(key, b"v" * 500)   # işçi kare arşivini ve MP4'ü yazdı (D-09)
    ok = ops.complete(w, j, u, "w", key, frames_key=fkey)
    assert ok is False
    store.delete(key); store.delete(fkey)                             # protokol: 0 satır -> İKİ dosya da silinir
    assert store.list_keys() == [] and db.su.execute("SELECT count(*) FROM media_asset WHERE kind IN ('result_video','frames_archive')").fetchone()[0] == 0


def make_done_job(db, store, u):
    """İki girdi + tamamlanmış iş (gerçek dosyalarla)."""
    api = db.conn("cue_api")
    s = mp.upload(api, store, u, "start_drawing", b"s" * 10); e = mp.upload(api, store, u, "end_drawing", b"e" * 10)
    db.su.execute("UPDATE model_version SET is_active=false"); db.model()
    j = db.su.execute("INSERT INTO animation_job(owner_id,idempotency_key,seed,start_asset_id,end_asset_id) VALUES (%s,%s,1,%s,%s) RETURNING id", (u, uuid.uuid4(), s, e)).fetchone()[0]
    w = db.conn("cue_worker", autocommit=False)
    assert ops.claim(w, "w") == j
    key = mp.new_key("mp4"); data = b"V" * 300; store.put(key, data)
    fkey = mp.new_key("zip"); zdata = mp.build_frames_zip(); store.put(fkey, zdata)
    import hashlib
    vid = w.execute("INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,width,height,sha256) VALUES (%s,'result_video',%s,'video/mp4',%s,512,320,%s) RETURNING id",
                    (u, key, len(data), hashlib.sha256(data).hexdigest())).fetchone()[0]
    fid = w.execute("INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,width,height,sha256) VALUES (%s,'frames_archive',%s,'application/zip',%s,512,320,%s) RETURNING id",
                    (u, fkey, len(zdata), hashlib.sha256(zdata).hexdigest())).fetchone()[0]
    assert w.execute(ops.COMPLETE, (vid, fid, 16, j, "w")).rowcount == 1; w.commit()
    return j, key


def test_s7_delete_active_job_is_refused_terminal_job_deleted(db, store):
    u = db.user(); api = db.conn("cue_api")
    j, key = make_done_job(db, store, u)
    active = db.job(u)
    assert mp.delete_job(api, store, active, u) == "conflict"
    other = db.user()
    assert mp.delete_job(api, store, j, other) == "not_found"          # başkasının işi: varlığı belli edilmez
    frames_key = db.su.execute("SELECT m.storage_key FROM animation_job j JOIN media_asset m ON m.id=j.frames_asset_id WHERE j.id=%s", (j,)).fetchone()[0]
    assert store.exists(frames_key)
    assert mp.delete_job(api, store, j, u) == "deleted"
    assert not store.exists(key) and not store.exists(frames_key)       # MP4 ve kare arşivi birlikte silinir
    assert db.su.execute("SELECT count(*) FROM animation_job WHERE id=%s", (j,)).fetchone()[0] == 0
    rep = mp.reconcile_report(db.su, store)       # etkin işin yardımcı varlıklarının dosyası yok (test düzeneği); silinen işin izi kalmamalı
    assert rep["orphan_files"] == [] and rep["mismatched"] == [] and key not in rep["missing_files"]


def test_s7b_file_delete_failure_leaves_orphan_that_sweeper_removes(db, store, tmp_path):
    u = db.user(); api = db.conn("cue_api"); maint = db.conn("cue_maintenance")
    j, key = make_done_job(db, store, u)
    assert mp.delete_job(api, store, j, u, file_delete_fails=True) == "deleted"   # kayıt gitti
    assert db.su.execute("SELECT count(*) FROM animation_job WHERE id=%s", (j,)).fetchone()[0] == 0
    leftover = [k for k, _ in store.list_keys()]
    assert key in leftover                                              # dosya sahipsiz kaldı
    for k in leftover:
        age(store, k, 7200)
    mp.sweep_orphans(maint, store, min_age_s=3600)
    assert store.list_keys() == []


def test_frames_archive_serves_single_frames_with_ownership_and_bounds(db, store):
    """Karar D-09: S6 kare gezinme için kareler tek arşivden sunulur; sahiplik, sınır ve eksik dosya davranışı."""
    u = db.user(); api = db.conn("cue_api")
    j, key = make_done_job(db, store, u)
    assert mp.serve_frame(api, store, j, u, 1) == ("200", b"\x89PNG-frame-001")
    assert mp.serve_frame(api, store, j, u, 16) == ("200", b"\x89PNG-frame-016")
    assert mp.serve_frame(api, store, j, u, 0) == ("404", None) and mp.serve_frame(api, store, j, u, 17) == ("404", None)
    assert mp.serve_frame(api, store, j, db.user(), 1) == ("404", None)           # başkasının işi
    active = db.job(u)
    assert mp.serve_frame(api, store, active, u, 1) == ("404", None)               # done değil
    fkey = db.su.execute("SELECT m.storage_key FROM animation_job j JOIN media_asset m ON m.id=j.frames_asset_id WHERE j.id=%s", (j,)).fetchone()[0]
    store.delete(fkey)
    assert mp.serve_frame(api, store, j, u, 1) == ("unavailable", None)
    assert db.su.execute("SELECT status FROM animation_job WHERE id=%s", (j,)).fetchone()[0] == "done"   # iş kaydı değişmez
    assert fkey in mp.reconcile_report(db.su, store)["missing_files"]


def test_s8_missing_video_file_is_reported_not_auto_repaired(db, store):
    u = db.user(); api = db.conn("cue_api")
    j, key = make_done_job(db, store, u)
    assert mp.serve_video(api, store, j, u)[0] == "200"
    store.delete(key)
    assert mp.serve_video(api, store, j, u) == ("unavailable", None)
    assert db.su.execute("SELECT status FROM animation_job WHERE id=%s", (j,)).fetchone()[0] == "done"   # iş kaydı değişmez
    rep = mp.reconcile_report(db.su, store)
    assert rep["missing_files"] == [key] and rep["orphan_files"] == []
    assert mp.serve_video(api, store, j, db.user()) == ("404", None)


def test_reconcile_detects_corrupted_file(db, store):
    u = db.user()
    j, key = make_done_job(db, store, u)
    store._p(key).write_bytes(b"corrupt")
    assert mp.reconcile_report(db.su, store)["mismatched"] == [key]


def test_unattached_uploads_cleanup_after_24h(db, store):
    u = db.user(); api = db.conn("cue_api"); maint = db.conn("cue_maintenance")
    fresh = mp.upload(api, store, u, "start_drawing", b"f" * 10)
    old = mp.upload(api, store, u, "end_drawing", b"o" * 10)
    db.su.execute("UPDATE media_asset SET created_at = clock_timestamp() - interval '25 hours' WHERE id=%s", (old,))
    j, key = make_done_job(db, store, u)                               # bağlı varlıklar korunmalı
    removed = mp.cleanup_unattached(maint, store)
    assert len(removed) == 1
    assert db.su.execute("SELECT count(*) FROM media_asset WHERE id=%s", (fresh,)).fetchone()[0] == 1
    assert mp.reconcile_report(db.su, store)["orphan_files"] == []


# --------------------------------------------------------------------------------------------------------------
# S9: yedekten dönüş (pg_dump -Fc / pg_restore) ve dosya eşleşmesi
def dump_restore(server, src_db, dst_db, dump_name):
    env = ["docker", "exec", "-e", f"PGPASSWORD={server['password']}", server["name"]]
    subprocess.run(env + ["pg_dump", "-U", "postgres", "-Fc", "-f", f"/tmp/{dump_name}", src_db], check=True, capture_output=True)
    a = connect(server, "postgres"); a.execute(f"CREATE DATABASE {dst_db}"); a.close()
    subprocess.run(env + ["pg_restore", "-U", "postgres", "--no-owner", "-d", dst_db, f"/tmp/{dump_name}"], check=True, capture_output=True)


def test_s9_backup_restore_rehearsal_with_media_mismatch_and_deletion_resurrection(db, store, server, tmp_path):
    u = db.user()
    j1, k1 = make_done_job(db, store, u)                                # T0: yedeğe girecek
    j2, k2 = make_done_job(db, store, u)                                # T0'da var, sonra silinecek
    ledger = tmp_path / "deleted.log"
    dst = "r_" + uuid.uuid4().hex[:8]
    dump_restore(server, db.name, dst, "t0.dump")                       # --- T0 yedeği alındı
    # T1: yedekten SONRA yeni iş geliyor, j2 siliniyor, bir dosya kayboluyor
    api = db.conn("cue_api")
    j3, k3 = make_done_job(db, store, u)
    assert mp.delete_job(api, store, j2, u, ledger=ledger) == "deleted"
    restored = connect(server, dst)
    # (a) yedek eski, dosyalar yeni: j3'ün dosyaları sahipsiz görünür; j2'nin kaydı geri gelmiştir ama dosyası yoktur
    rep = mp.reconcile_report(restored, store)
    assert any(k.endswith(".mp4") and k == k3 for k in rep["orphan_files"])
    assert k2 in rep["missing_files"]                                   # silinmiş işin kaydı yeniden belirdi, dosyası yok
    assert restored.execute("SELECT count(*) FROM animation_job WHERE id=%s", (j2,)).fetchone()[0] == 1   # NFR-05 sorunu: yeniden belirme
    # dönüş sonrası kural: önce YALNIZ rapor; süpürücü apply=False hiçbir şey silmez
    for k, _ in store.list_keys():
        age(store, k, 7200)
    before = len(store.list_keys())
    maint = connect(server, dst, role="cue_maintenance")
    assert mp.sweep_orphans(maint, store, min_age_s=3600, apply=False)
    assert len(store.list_keys()) == before
    # silme defteri yeniden uygulanır
    removed = mp.reapply_deletions(restored, ledger)
    assert [r[0] for r in removed] == [str(j2)]
    assert restored.execute("SELECT count(*) FROM animation_job WHERE id=%s", (j2,)).fetchone()[0] == 0
    # (b) yedek yeni, dosyalar eski: dosyalar yedeklenen kayıtlardan geride -> eksik dosya raporu
    store.delete(k1)
    rep2 = mp.reconcile_report(restored, store)
    assert k1 in rep2["missing_files"]
    # geri yüklenen veritabanında kısıtlar ve roller yerinde
    assert restored.execute("SELECT count(*) FROM pg_constraint WHERE conrelid='animation_job'::regclass AND contype='c'").fetchone()[0] >= 10
    assert restored.execute("SELECT has_table_privilege('cue_worker','animation_job','SELECT')").fetchone()[0]
