"""D-06 kanıtı: önerilen RLS politikaları (database/optional/rls_proposal.up.sql). Migration'a EKLENMEZ; yalnız uygulanabilirlik ve davranış testi."""
import pathlib, uuid
import pytest
from psycopg import errors as E
import ops

OPT = pathlib.Path(__file__).resolve().parent.parent / "optional"


@pytest.fixture()
def rdb(db):
    db.su.execute((OPT / "rls_proposal.up.sql").read_text())
    return db


def as_user(conn, user):
    """Havuzlu bağlantı taklidi: işlem içinde SET LOCAL."""
    conn.execute("SELECT set_config('app.user_id', %s, true)", (str(user),))


def test_fail_closed_without_setting_even_after_a_previous_transaction(rdb):
    a = rdb.user(); rdb.job(a); rdb.job(a)
    api = rdb.conn("cue_api", autocommit=False)
    assert api.execute("SELECT count(*) FROM animation_job").fetchone()[0] == 0          # ayar yok -> hiçbir satır
    as_user(api, a)
    assert api.execute("SELECT count(*) FROM animation_job").fetchone()[0] == 2
    api.commit()                                                                         # SET LOCAL işlemle biter
    assert api.execute("SELECT count(*) FROM animation_job").fetchone()[0] == 0          # sızıntı yok; '' durumu hata değil boş sonuç
    api.commit()


def test_cross_owner_isolation_read_update_delete_insert(rdb):
    a, b = rdb.user(), rdb.user(); ja, jb = rdb.job(a), rdb.job(b)
    api = rdb.conn("cue_api", autocommit=False)
    as_user(api, a)
    assert [r[0] for r in api.execute("SELECT id FROM animation_job").fetchall()] == [ja]
    assert api.execute("SELECT count(*) FROM animation_job WHERE id=%s", (jb,)).fetchone()[0] == 0   # tahmin edilen kimlik bile görünmez
    assert api.execute(ops.CANCEL, (jb, b)).rowcount == 0                                # sahip koşulu doğru verilse bile RLS kapatır
    assert api.execute("DELETE FROM animation_job WHERE id=%s", (jb,)).rowcount == 0
    assert api.execute(ops.CANCEL, (ja, a)).rowcount == 1
    api.commit()
    # başkası adına satır eklenemez (WITH CHECK)
    api = rdb.conn("cue_api", autocommit=False); as_user(api, a)
    s, e = rdb.asset(b), rdb.asset(b, "end_drawing")
    with pytest.raises(E.InsufficientPrivilege):                           # "new row violates row-level security policy"
        api.execute("INSERT INTO animation_job(owner_id,idempotency_key,seed,start_asset_id,end_asset_id) VALUES (%s,%s,1,%s,%s)", (b, uuid.uuid4(), s, e))
    api.rollback()


def test_media_assets_isolated_and_foreign_asset_reference_still_rejected(rdb):
    a, b = rdb.user(), rdb.user(); foreign = rdb.asset(b); mine = rdb.asset(a, "end_drawing")
    api = rdb.conn("cue_api", autocommit=False); as_user(api, a)
    assert api.execute("SELECT count(*) FROM media_asset WHERE id=%s", (foreign,)).fetchone()[0] == 0
    with pytest.raises(E.ForeignKeyViolation):                              # WITH CHECK geçer (owner=a); bileşik FK (RLS'den bağımsız) ikinci savunma yakalar
        api.execute("INSERT INTO animation_job(owner_id,idempotency_key,seed,start_asset_id,end_asset_id) VALUES (%s,%s,1,%s,%s)", (a, uuid.uuid4(), foreign, mine))
    api.rollback()


def test_worker_and_maintenance_keep_cross_owner_queue_access_under_rls(rdb):
    a, b = rdb.user(), rdb.user(); rdb.model(); ja, jb = rdb.job(a), rdb.job(b)
    w = rdb.conn("cue_worker", autocommit=False)
    claimed = {ops.claim(w, "w"), ops.claim(w, "w")}
    assert claimed == {ja, jb}                                                           # SKIP LOCKED claim RLS altında çalışır
    rdb.su.execute("UPDATE animation_job SET heartbeat_at = clock_timestamp() - interval '1 hour'")
    m = rdb.conn("cue_maintenance")
    assert {r[0] for r in m.execute(ops.REAP, (900,)).fetchall()} == {ja, jb}


def test_superuser_and_owner_bypass_is_a_deployment_rule_not_a_db_guarantee(rdb):
    a = rdb.user(); rdb.job(a)
    assert rdb.su.execute("SELECT count(*) FROM animation_job").fetchone()[0] == 1       # süper kullanıcı RLS'yi atlar: uygulama bununla bağlanmamalı


def test_control_without_rls_the_api_role_sees_every_owners_rows(db):
    """Negatif kontrol: izolasyonu RLS sağlıyor (yalnız rol yetkisi değil). RLS uygulanmadan cue_api tüm satırları görür."""
    a, b = db.user(), db.user(); db.job(a); db.job(b)
    api = db.conn("cue_api", autocommit=False)
    assert api.execute("SELECT count(*) FROM animation_job").fetchone()[0] == 2
