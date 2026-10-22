"""Migration davranışı: yukarı/aşağı/yukarı, schema.sql eşdeğerliği, işlemsel DDL geri alma."""
import subprocess, uuid
import pytest
from psycopg import errors as E
from conftest import connect, apply, sh


def dump(server, dbname):
    r = subprocess.run(["docker", "exec", "-e", f"PGPASSWORD={server['password']}", server["name"], "pg_dump", "-U", "postgres", "-s", "--no-owner", dbname],
                       check=True, capture_output=True, text=True)
    return "\n".join(l for l in r.stdout.splitlines() if not l.startswith(("--", "SET ", "\\restrict", "\\unrestrict")) and "set_config" not in l)


def fresh(server):
    name = "m_" + uuid.uuid4().hex[:10]
    a = connect(server, "postgres"); a.execute(f"CREATE DATABASE {name}"); a.close()
    return name


def test_up_down_up_gives_identical_schema_and_schema_sql_matches(server):
    n1 = fresh(server); c = connect(server, n1)
    apply(c, "0001_initial", "0002_roles_and_grants")
    d1 = dump(server, n1)
    apply(c, "0002_roles_and_grants", "0001_initial", direction="down")
    left = c.execute("SELECT count(*) FROM pg_tables WHERE schemaname='public'").fetchone()[0]
    assert left == 0
    apply(c, "0001_initial", "0002_roles_and_grants")
    assert dump(server, n1) == d1
    # schema.sql (birleşik) ile aynı şema
    n2 = fresh(server); c2 = connect(server, n2)
    import pathlib
    c2.execute((pathlib.Path(__file__).resolve().parent.parent / "schema.sql").read_text())
    assert dump(server, n2) == d1


def test_failed_migration_is_atomic_in_postgres(server):
    """İşlemsel DDL: başarısız migration yarım tablo bırakmaz."""
    n = fresh(server); c = connect(server, n)
    with pytest.raises(E.UndefinedTable):
        with c.transaction():
            c.execute("CREATE TABLE half_done(id int)")
            c.execute("ALTER TABLE does_not_exist ADD COLUMN x int")
    assert c.execute("SELECT to_regclass('half_done')").fetchone()[0] is None


def test_create_index_concurrently_cannot_run_in_transaction(server):
    """Not (SR-11): büyük tablolarda CONCURRENTLY gerekirse migration işlem dışında çalışmalı."""
    n = fresh(server); c = connect(server, n); apply(c, "0001_initial")
    with pytest.raises(E.ActiveSqlTransaction):
        with c.transaction():
            c.execute("CREATE INDEX CONCURRENTLY tmp_idx ON app_user (created_at)")


def test_postgres_version_is_18(server):
    c = connect(server, "postgres")
    assert c.execute("SHOW server_version").fetchone()[0].startswith("18.")
    assert c.execute("SHOW timezone").fetchone()[0] in ("UTC", "Etc/UTC")
