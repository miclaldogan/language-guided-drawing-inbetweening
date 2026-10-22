"""Tek kullanımlık PostgreSQL 18 kapsayıcısı ve test yardımcıları. Gerçek veri yok; yalnız sentetik veri."""
import os, pathlib, secrets, subprocess, time, uuid
import psycopg
import pytest

IMAGE = "postgres:18@sha256:edb0c08dc33befd0262ab3b5cf1c4f3f8cfd8b09e88c05b45adee29d6761ddb6"
MIG = pathlib.Path(__file__).resolve().parent.parent / "migrations"
ARGON = "$argon2id$v=19$m=65536,t=3,p=4$c2FsdHNhbHRzYWx0$aGFzaGhhc2hoYXNoaGFzaGhhc2hoYXNoaGFzaGhhc2g"


def sh(*a, **k):
    return subprocess.run(a, check=True, capture_output=True, text=True, **k)


@pytest.fixture(scope="session")
def server():
    pw = secrets.token_hex(16)
    name = f"cue-validation-{os.getpid()}"
    sh("docker", "run", "-d", "--rm", "--name", name, "-e", f"POSTGRES_PASSWORD={pw}",
       "-p", "127.0.0.1::5432", "--tmpfs", "/var/lib/postgresql:rw", IMAGE)
    try:
        port = sh("docker", "port", name, "5432/tcp").stdout.strip().splitlines()[0].rsplit(":", 1)[1]
        for _ in range(100):
            try:
                psycopg.connect(host="127.0.0.1", port=port, user="postgres", password=pw, dbname="postgres", connect_timeout=2).close()
                break
            except psycopg.OperationalError:
                time.sleep(0.3)
        else:
            raise RuntimeError("PostgreSQL başlamadı")
        yield dict(name=name, host="127.0.0.1", port=port, password=pw)
    finally:
        subprocess.run(["docker", "rm", "-f", name], capture_output=True)


def connect(server, dbname, autocommit=True, role=None):
    c = psycopg.connect(host=server["host"], port=server["port"], user="postgres", password=server["password"],
                        dbname=dbname, autocommit=autocommit)
    if role:
        c.execute(f"SET ROLE {role}")
    return c


def apply(conn, *names, direction="up"):
    for n in names:
        conn.execute((MIG / f"{n}.{direction}.sql").read_text())


class DB:
    def __init__(self, server, name):
        self.server, self.name = server, name
        self.su = connect(server, name)

    def conn(self, role=None, autocommit=True):
        return connect(self.server, self.name, autocommit=autocommit, role=role)

    # --- sentetik veri üreticileri -------------------------------------
    def user(self, email=None):
        email = email or f"u{uuid.uuid4().hex[:8]}@example.test"
        return self.su.execute("INSERT INTO app_user(email,password_hash) VALUES (%s,%s) RETURNING id", (email, ARGON)).fetchone()[0]

    def asset(self, owner, kind="start_drawing"):
        ct = {"result_video": "video/mp4", "frames_archive": "application/zip"}.get(kind, "image/png")
        return self.su.execute(
            "INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,width,height,sha256) "
            "VALUES (%s,%s,%s,%s,1000,512,320,%s) RETURNING id",
            (owner, kind, f"assets/{uuid.uuid4().hex}", ct, "a" * 64)).fetchone()[0]

    def model(self, active=True, name=None):
        return self.su.execute(
            "INSERT INTO model_version(name,version_label,weights_sha256,supports_plan,is_active) VALUES (%s,'v1',%s,true,%s) RETURNING id",
            (name or f"m{uuid.uuid4().hex[:6]}", "b" * 64, active)).fetchone()[0]

    def job(self, owner, plan=False, status="queued", key=None, **extra):
        s, e = self.asset(owner), self.asset(owner, "end_drawing")
        cols = dict(owner_id=owner, idempotency_key=key or uuid.uuid4(), seed=42, start_asset_id=s, end_asset_id=e)
        if plan:
            cols.update(command_text="First move the eyes left, then turn the head.", plan='{"events":[]}',
                        plan_schema_version=1, plan_approved_at="2026-10-22T10:00:00Z")
        cols.update(extra)
        names = ",".join(cols)
        ph = ",".join(["%s"] * len(cols))
        return self.su.execute(f"INSERT INTO animation_job({names}) VALUES ({ph}) RETURNING id", list(cols.values())).fetchone()[0]


@pytest.fixture()
def db(server):
    name = "t_" + uuid.uuid4().hex[:10]
    admin = connect(server, "postgres")
    admin.execute(f"CREATE DATABASE {name}")
    admin.close()
    d = DB(server, name)
    apply(d.su, "0001_initial", "0002_roles_and_grants")
    yield d
    d.su.close()
    admin = connect(server, "postgres")
    admin.execute(f"DROP DATABASE {name} WITH (FORCE)")
    admin.close()
