"""Parola ve oturum varsayımları (argon2-cffi + hashlib). Ölçülen süre YALNIZ bu makine/kapsayıcı için bilgidir."""
import hashlib, secrets, time
import pytest
from argon2 import PasswordHasher
from psycopg import errors as E


def test_argon2id_hash_is_accepted_and_verified(db):
    ph = PasswordHasher()                       # kütüphane varsayılanları
    t0 = time.perf_counter(); h = ph.hash("correct horse battery staple"); t1 = time.perf_counter()
    assert h.startswith("$argon2id$")
    u = db.su.execute("INSERT INTO app_user(email,password_hash) VALUES ('p@example.test',%s) RETURNING id", (h,)).fetchone()[0]
    stored = db.su.execute("SELECT password_hash FROM app_user WHERE id=%s", (u,)).fetchone()[0]
    assert ph.verify(stored, "correct horse battery staple")
    with pytest.raises(Exception):
        ph.verify(stored, "wrong")
    assert "correct horse" not in stored
    print(f"argon2id varsayılan parametrelerle hash süresi (bu makine): {(t1 - t0) * 1000:.0f} ms; {h.split('$')[3]}")


def test_session_token_flow(db):
    u = db.user()
    raw = secrets.token_urlsafe(32)
    digest = hashlib.sha256(raw.encode()).digest()
    assert len(digest) == 32
    db.su.execute("INSERT INTO auth_session(user_id,token_hash,expires_at) VALUES (%s,%s,now()+interval '7 days')", (u, digest))
    # çözme: yalnız özet ile aranır; ham belirteç DB'de yok
    row = db.su.execute("SELECT user_id FROM auth_session WHERE token_hash=%s AND expires_at>now()", (hashlib.sha256(raw.encode()).digest(),)).fetchone()
    assert row[0] == u
    assert db.su.execute("SELECT count(*) FROM auth_session WHERE token_hash=%s", (raw.encode(),)).fetchone()[0] == 0
    # çıkış = satır silme; ardından aynı belirteç çözülmez
    db.su.execute("DELETE FROM auth_session WHERE token_hash=%s", (digest,))
    assert db.su.execute("SELECT user_id FROM auth_session WHERE token_hash=%s AND expires_at>now()", (digest,)).fetchone() is None


def test_expired_session_not_resolved_and_cleanup(db):
    u = db.user()
    db.su.execute("INSERT INTO auth_session(user_id,token_hash,created_at,expires_at) VALUES (%s,%s,now()-interval '2 days',now()-interval '1 day')", (u, b"e" * 32))
    assert db.su.execute("SELECT 1 FROM auth_session WHERE token_hash=%s AND expires_at>now()", (b"e" * 32,)).fetchone() is None
    m = db.conn("cue_maintenance")
    assert m.execute("DELETE FROM auth_session WHERE expires_at<now()").rowcount == 1
