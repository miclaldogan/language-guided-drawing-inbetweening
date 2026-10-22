"""Gözlem amaçlı ölçek sondası (performans iddiası değil): sentetik büyük veri üzerinde gerçek planlayıcı seçimlerini ve süreleri kaydeder.
Tek kullanımlık PostgreSQL 18; seqscan kapatılmaz. Çıktı: reports/raw/scale-probe.txt. Süreler YALNIZ bu makine/kapsayıcı için gözlemdir."""
import pathlib, re, sys, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "database" / "validation"))
import conftest as cf  # noqa: E402

N_JOBS, N_USERS, N_SESSIONS = 150_000, 1_000, 50_000
out = []


def log(s=""):
    print(s); out.append(s)


def main():
    pw = cf.secrets.token_hex(16); name = f"cue-scale-{cf.os.getpid()}"
    cf.sh("docker", "run", "-d", "--rm", "--name", name, "-e", f"POSTGRES_PASSWORD={pw}", "-p", "127.0.0.1::5432", "--tmpfs", "/var/lib/postgresql:rw", "--shm-size=256m", cf.IMAGE)
    try:
        port = cf.sh("docker", "port", name, "5432/tcp").stdout.strip().splitlines()[0].rsplit(":", 1)[1]
        srv = dict(name=name, host="127.0.0.1", port=port, password=pw)
        for _ in range(100):
            try:
                cf.connect(srv, "postgres").close(); break
            except Exception:
                time.sleep(0.3)
        c = cf.connect(srv, "postgres"); cf.apply(c, "0001_initial", "0002_roles_and_grants")
        t0 = time.time()
        c.execute(f"INSERT INTO app_user(email,password_hash) SELECT 'u'||g||'@example.test','$argon2id$v=19$m=65536,t=3,p=4$c2FsdA$aGFzaA' FROM generate_series(1,{N_USERS}) g")
        c.execute("INSERT INTO model_version(name,version_label,weights_sha256,supports_plan,is_active) VALUES ('m','v1',repeat('b',64),true,true)")
        c.execute("CREATE TEMP TABLE u AS SELECT id, row_number() OVER (ORDER BY id)-1 AS i FROM app_user")
        c.execute(f"""CREATE TEMP TABLE tj AS SELECT g AS n, u.id AS owner, gen_random_uuid() sid, gen_random_uuid() eid, gen_random_uuid() vid, gen_random_uuid() fid, gen_random_uuid() jid,
                      now() - (({N_JOBS}-g) * interval '100 seconds') AS created
                      FROM generate_series(1,{N_JOBS}) g JOIN u ON u.i = g % {N_USERS}""")
        c.execute("""INSERT INTO media_asset(id,owner_id,kind,storage_key,content_type,byte_size,width,height,sha256,created_at)
                     SELECT sid,owner,'start_drawing','a/'||sid,'image/png',1000,512,320,repeat('a',64),created FROM tj
                     UNION ALL SELECT eid,owner,'end_drawing','a/'||eid,'image/png',1000,512,320,repeat('a',64),created FROM tj
                     UNION ALL SELECT vid,owner,'result_video','a/'||vid,'video/mp4',5000,512,320,repeat('a',64),created FROM tj WHERE n <= %s
                     UNION ALL SELECT fid,owner,'frames_archive','a/'||fid,'application/zip',20000,512,320,repeat('a',64),created FROM tj WHERE n <= %s""" % (N_JOBS - 60, N_JOBS - 60))
        c.execute("SELECT id FROM model_version")
        mv = c.execute("SELECT id FROM model_version").fetchone()[0]
        # done: n <= N-60 ; failed: her 1000'inci; queued: son 30 ; running: 20 (10 taze, 10 bayat)
        c.execute(f"""INSERT INTO animation_job(id,owner_id,idempotency_key,status,seed,start_asset_id,end_asset_id,video_asset_id,frames_asset_id,frame_count,model_version_id,created_at,started_at,finished_at,locked_by,heartbeat_at,error_code,error_message)
          SELECT jid,owner,gen_random_uuid(),
            CASE WHEN mod(n,1000) = 0 AND n <= {N_JOBS-60} THEN 'failed' WHEN n <= {N_JOBS-60} THEN 'done' WHEN n <= {N_JOBS-30} THEN 'running' ELSE 'queued' END,
            1,sid,eid, CASE WHEN n <= {N_JOBS-60} AND mod(n,1000) <> 0 THEN vid END,
            CASE WHEN n <= {N_JOBS-60} AND mod(n,1000) <> 0 THEN fid END, CASE WHEN n <= {N_JOBS-60} AND mod(n,1000) <> 0 THEN 16 END,
            CASE WHEN n <= {N_JOBS-30} THEN %s::uuid END, created,
            CASE WHEN n <= {N_JOBS-30} THEN created + interval '1 second' END,
            CASE WHEN n <= {N_JOBS-60} THEN created + interval '200 seconds' END,
            CASE WHEN n > {N_JOBS-60} AND n <= {N_JOBS-30} THEN 'w1' END,
            CASE WHEN n > {N_JOBS-60} AND n <= {N_JOBS-30} THEN CASE WHEN mod(n,2) = 0 THEN now() ELSE now() - interval '2 hours' END END,
            CASE WHEN mod(n,1000) = 0 AND n <= {N_JOBS-60} THEN 'generation_failed' END, CASE WHEN mod(n,1000) = 0 AND n <= {N_JOBS-60} THEN 'x' END
          FROM tj ORDER BY n""", (mv,))
        c.execute("DELETE FROM media_asset WHERE kind='result_video' AND id NOT IN (SELECT video_asset_id FROM animation_job WHERE video_asset_id IS NOT NULL)")
        c.execute("DELETE FROM media_asset WHERE kind='frames_archive' AND id NOT IN (SELECT frames_asset_id FROM animation_job WHERE frames_asset_id IS NOT NULL)")
        c.execute(f"""INSERT INTO auth_session(user_id,token_hash,expires_at)
                      SELECT u.id, sha256(('t'||g)::bytea), now()+interval '7 days' FROM generate_series(1,{N_SESSIONS}) g JOIN u ON u.i = g % {N_USERS}""")
        c.execute("ANALYZE")
        log(f"# Ölçek sondası (gözlem): {N_JOBS} iş, {N_USERS} kullanıcı, {N_SESSIONS} oturum; veri yükleme {time.time()-t0:.1f} sn")
        for t in ("app_user", "auth_session", "media_asset", "animation_job"):
            n, sz, isz = c.execute("SELECT (SELECT count(*) FROM %s), pg_size_pretty(pg_table_size('%s')), pg_size_pretty(pg_indexes_size('%s'))" % (t, t, t)).fetchone()
            log(f"{t:14s} satır={n:>8}  tablo={sz:>9}  indeksler={isz:>9}")
        job_bytes = c.execute("SELECT (pg_table_size('animation_job')+pg_indexes_size('animation_job'))::float/(SELECT count(*) FROM animation_job)").fetchone()[0]
        asset_bytes = c.execute("SELECT (pg_table_size('media_asset')+pg_indexes_size('media_asset'))::float/(SELECT count(*) FROM media_asset)").fetchone()[0]
        log(f"iş başına: iş satırı+indeks ≈ {job_bytes:.0f} B (plan JSON YOK); varlık satırı+indeks ≈ {asset_bytes:.0f} B; iş başına 4 varlık (başlangıç, bitiş, MP4, kare arşivi) ⇒ ≈ {job_bytes + 4*asset_bytes:.0f} B (plan JSON hariç)")
        log()
        user = c.execute("SELECT owner_id FROM animation_job WHERE status='done' LIMIT 1").fetchone()[0]
        cur = c.execute("SELECT created_at, id FROM animation_job WHERE owner_id=%s AND status='done' ORDER BY created_at DESC, id DESC OFFSET 40 LIMIT 1", (user,)).fetchone()
        tok = c.execute("SELECT token_hash FROM auth_session LIMIT 1 OFFSET 777").fetchone()[0]
        job = c.execute("SELECT id FROM animation_job WHERE owner_id=%s LIMIT 1", (user,)).fetchone()[0]
        idem = c.execute("SELECT idempotency_key FROM animation_job WHERE id=%s", (job,)).fetchone()[0]
        probes = [
            ("Q1 kitaplık, keyset sayfa (20 satır)", "SELECT id,status,created_at FROM animation_job WHERE owner_id=%(u)s AND (created_at,id) < (%(c)s,%(i)s) ORDER BY created_at DESC, id DESC LIMIT 20", dict(u=user, c=cur[0], i=cur[1])),
            ("Q2 tek iş (id + sahip)", "SELECT * FROM animation_job WHERE id=%(j)s AND owner_id=%(u)s", dict(j=job, u=user)),
            ("Q3 iş kapma (CTE, SKIP LOCKED; geri alınır)", None, None),
            ("Q4 takılı iş araması (15 dk eşiği)", "SELECT id FROM animation_job WHERE status='running' AND heartbeat_at < now() - interval '15 minutes'", {}),
            ("Q6 oturum çözme (token_hash)", "SELECT user_id FROM auth_session WHERE token_hash=%(t)s AND expires_at > now()", dict(t=tok)),
            ("Q-idem (sahip, anahtar) arama", "SELECT id FROM animation_job WHERE owner_id=%(u)s AND idempotency_key=%(k)s", dict(u=user, k=idem)),
            ("Q-cap kullanıcı başına etkin iş sayımı", "SELECT count(*) FROM animation_job WHERE owner_id=%(u)s AND status IN ('queued','running')", dict(u=user)),
            ("Q8 başarısız işler (İNDEKS YOK, karar)", "SELECT id FROM animation_job WHERE status='failed' ORDER BY finished_at DESC LIMIT 20", {}),
            ("Q7 bağlanmamış eski yüklemeler (indeks yok)", "SELECT a.id FROM media_asset a WHERE a.kind IN ('start_drawing','end_drawing') AND a.created_at < now() - interval '24 hours' AND NOT EXISTS (SELECT 1 FROM animation_job j WHERE j.start_asset_id=a.id OR j.end_asset_id=a.id)", {}),
            ("Q7b aynı iş, iki ayrı NOT EXISTS (alternatif yazım)", "SELECT a.id FROM media_asset a WHERE a.kind IN ('start_drawing','end_drawing') AND a.created_at < now() - interval '24 hours' AND NOT EXISTS (SELECT 1 FROM animation_job j WHERE j.start_asset_id=a.id) AND NOT EXISTS (SELECT 1 FROM animation_job j WHERE j.end_asset_id=a.id)", {}),
        ]
        from ops import CLAIM
        for label, sql, params in probes:
            if sql is None:
                c.execute("BEGIN")
                plan = c.execute("EXPLAIN (ANALYZE, BUFFERS) " + CLAIM, {"worker": "probe"}).fetchall()
                c.execute("ROLLBACK")
            else:
                plan = c.execute("EXPLAIN (ANALYZE, BUFFERS) " + sql, params).fetchall()
            txt = "\n".join(r[0] for r in plan)
            nodes = [re.sub(r"\s+\(cost.*", "", l).strip(" ->") for l in txt.splitlines() if re.search(r"(Scan|Index)", l) and "cost=" in l]
            ex = re.search(r"Execution Time: ([\d.]+) ms", txt)
            log(f"## {label}")
            log("   erişim: " + "; ".join(nodes[:4]))
            log(f"   yürütme süresi (gözlem): {ex.group(1)} ms")
        log()
        log("Not: süreler tek makinede, ısınmış önbellekle, tek çalıştırmada gözlenmiştir; hız vaadi değildir. Planlayıcı seçimleri (indeks/ardışık tarama) asıl bulgudur.")
        (ROOT / "reports" / "raw" / "scale-probe.txt").write_text("\n".join(out) + "\n")
    finally:
        cf.subprocess.run(["docker", "rm", "-f", name], capture_output=True)


main()
