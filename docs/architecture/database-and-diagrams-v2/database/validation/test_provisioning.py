"""Gerçek LOGIN hesaplarıyla sağlama akışı: migration hesabı, uygulama hesapları, sıra bağımlılığı. Yeni (izole) kapsayıcıda koşar:
küme genelindeki roller diğer testlerle çakışmasın diye."""
import pathlib, secrets, time, uuid
import psycopg
import pytest
from psycopg import errors as E
from conftest import IMAGE, sh, MIG, ARGON

PROV = pathlib.Path(__file__).resolve().parent.parent / "provisioning" / "01_roles_and_logins.example.sql"


@pytest.fixture(scope="module")
def pserver():
    pw = secrets.token_hex(16); name = f"cue-prov-{__import__('os').getpid()}"
    sh("docker", "run", "-d", "--rm", "--name", name, "-e", f"POSTGRES_PASSWORD={pw}", "-p", "127.0.0.1::5432", "--tmpfs", "/var/lib/postgresql:rw", IMAGE)
    try:
        port = sh("docker", "port", name, "5432/tcp").stdout.strip().splitlines()[0].rsplit(":", 1)[1]
        for _ in range(100):
            try:
                psycopg.connect(host="127.0.0.1", port=port, user="postgres", password=pw, dbname="postgres", connect_timeout=2).close(); break
            except psycopg.OperationalError:
                time.sleep(0.3)
        yield dict(host="127.0.0.1", port=port, pw=pw, name=name)
    finally:
        __import__("subprocess").run(["docker", "rm", "-f", name], capture_output=True)


def conn(ps, user, pw, db, autocommit=True):
    return psycopg.connect(host=ps["host"], port=ps["port"], user=user, password=pw, dbname=db, autocommit=autocommit)


def provision_sql(dbname, pws):
    s = PROV.read_text()
    for k, v in pws.items():
        s = s.replace(f":'{k}'", f"'{v}'")
    return s.replace(':"dbname"', f'"{dbname}"')


def test_migration_without_precreated_group_roles_fails_for_the_non_superuser_owner(pserver):
    """Sıra bağımlılığı: roller yoksa 0002'deki CREATE ROLE, CREATEROLE olmayan migration hesabında başarısız olur."""
    ps = pserver; a = conn(ps, "postgres", ps["pw"], "postgres")
    a.execute("CREATE DATABASE negdb"); a.execute("CREATE ROLE neg_migrator LOGIN PASSWORD 'x' NOCREATEROLE"); a.execute("ALTER DATABASE negdb OWNER TO neg_migrator")
    m = conn(ps, "neg_migrator", "x", "negdb")
    m.execute((MIG / "0001_initial.up.sql").read_text())
    with pytest.raises(E.InsufficientPrivilege):
        m.execute((MIG / "0002_roles_and_grants.up.sql").read_text())


def test_full_provisioning_flow_with_real_login_accounts(pserver):
    ps = pserver; su = conn(ps, "postgres", ps["pw"], "postgres")
    pws = {k: secrets.token_urlsafe(18) for k in ("mig_pw", "api_pw", "worker_pw", "maint_pw")}
    su.execute("CREATE DATABASE cue")
    su.execute(provision_sql("cue", pws))                                       # 1) roller + hesaplar (süper kullanıcı)
    mig = conn(ps, "cue_migrator", pws["mig_pw"], "cue")                        # 2) migration YALNIZ DDL sahibi hesapla
    mig.execute((MIG / "0001_initial.up.sql").read_text())
    mig.execute((MIG / "0002_roles_and_grants.up.sql").read_text())
    # 3) uygulama hesapları gerçek girişle
    api = conn(ps, "cue_api_login", pws["api_pw"], "cue")
    uid = api.execute("INSERT INTO app_user(email,password_hash) VALUES ('p@example.test',%s) RETURNING id", (ARGON,)).fetchone()[0]
    assert api.execute("SELECT count(*) FROM app_user").fetchone()[0] == 1
    with pytest.raises(E.InsufficientPrivilege):
        api.execute("CREATE TABLE evil(x int)")                                 # DDL yok
    with pytest.raises(E.InsufficientPrivilege):
        api.execute("UPDATE animation_job SET seed = 1")                        # değişmez sütun
    worker = conn(ps, "cue_worker_login", pws["worker_pw"], "cue")
    with pytest.raises(E.InsufficientPrivilege):
        worker.execute("SELECT password_hash FROM app_user")                    # işçi kimlik bilgisini okuyamaz
    assert worker.execute("SELECT count(*) FROM animation_job").fetchone()[0] == 0
    maint = conn(ps, "cue_maint_login", pws["maint_pw"], "cue")
    with pytest.raises(E.InsufficientPrivilege):
        maint.execute("SELECT * FROM app_user")
    # 4) sahiplik: tablolar migration hesabının; uygulama hesapları sahip DEĞİL (RLS FORCE'u anlamlı kılan koşul)
    cur = conn(ps, "postgres", ps["pw"], "cue")
    owners = {r[0] for r in cur.execute("SELECT DISTINCT tableowner FROM pg_tables WHERE schemaname='public'")}
    assert owners == {"cue_migrator"}
    # 5) hiçbir uygulama hesabı süper kullanıcı/RLS atlayan değil
    flags = cur.execute("SELECT rolname, rolsuper, rolbypassrls, rolcreaterole, rolcreatedb FROM pg_roles WHERE rolname LIKE 'cue\\_%'").fetchall()
    assert flags and all(not su_ and not byp and not cr and not cdb for _, su_, byp, cr, cdb in flags)
    # 6) parolasız ya da yanlış parola bağlantısı reddedilir; PUBLIC bağlanamaz
    with pytest.raises(psycopg.OperationalError):
        conn(ps, "cue_api_login", "wrong", "cue")
    su.execute("CREATE ROLE stranger LOGIN PASSWORD 'z'")
    with pytest.raises(psycopg.OperationalError):
        conn(ps, "stranger", "z", "cue")                                        # REVOKE CONNECT FROM PUBLIC
