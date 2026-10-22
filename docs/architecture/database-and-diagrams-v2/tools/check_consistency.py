"""Gereksinim ↔ DDL ↔ diyagram tutarlılık denetimi (Review A'nın otomatik kısmı).
Tek kullanımlık PostgreSQL 18'e migration'ları uygular, katalogla diyagram kaynaklarını ve çıktılarını karşılaştırır.
Çıkış kodu 0 = tüm denetimler geçti. Kullanım: uv run --no-project --with 'psycopg[binary]' --with pytest python tools/check_consistency.py"""
import pathlib, re, struct, sys, xml.etree.ElementTree as ET
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "database" / "validation"))
import conftest as cf  # noqa: E402

D = ROOT / "diagrams"
results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (f"  -- {detail}" if detail and not ok else ""))


def catalog():
    pw = cf.secrets.token_hex(16); name = f"cue-chk-{cf.os.getpid()}"
    cf.sh("docker", "run", "-d", "--rm", "--name", name, "-e", f"POSTGRES_PASSWORD={pw}", "-p", "127.0.0.1::5432", "--tmpfs", "/var/lib/postgresql:rw", cf.IMAGE)
    try:
        port = cf.sh("docker", "port", name, "5432/tcp").stdout.strip().splitlines()[0].rsplit(":", 1)[1]
        srv = dict(name=name, host="127.0.0.1", port=port, password=pw)
        for _ in range(100):
            try:
                cf.connect(srv, "postgres").close(); break
            except Exception:
                cf.time.sleep(0.3)
        c = cf.connect(srv, "postgres"); cf.apply(c, "0001_initial", "0002_roles_and_grants")
        cols = {}
        for t, n, ty in c.execute("""SELECT c.relname, a.attname, format_type(a.atttypid,a.atttypmod) FROM pg_attribute a JOIN pg_class c ON c.oid=a.attrelid
            JOIN pg_namespace s ON s.oid=c.relnamespace WHERE s.nspname='public' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped"""):
            cols.setdefault(t, {})[n] = ty
        fks = c.execute("SELECT conname, conrelid::regclass::text, confrelid::regclass::text FROM pg_constraint WHERE contype='f'").fetchall()
        status_check = c.execute("SELECT pg_get_constraintdef(oid) FROM pg_constraint WHERE conname='animation_job_status_valid'").fetchone()[0]
        roles = [r for (r,) in c.execute("SELECT rolname FROM pg_roles WHERE rolname LIKE 'cue_%'")]
        names = {n for (n,) in c.execute("SELECT conname FROM pg_constraint WHERE connamespace='public'::regnamespace")} | \
                {n for (n,) in c.execute("SELECT indexname FROM pg_indexes WHERE schemaname='public'")}
        literals = set()
        for (d,) in c.execute("SELECT pg_get_constraintdef(oid) FROM pg_constraint WHERE contype='c'"):
            literals |= set(re.findall(r"'([a-z_]+)'", d))
        return cols, fks, set(re.findall(r"'(\w+)'", status_check)), set(roles), names, literals
    finally:
        cf.subprocess.run(["docker", "rm", "-f", name], capture_output=True)


def main():
    cols, fks, statuses, roles, names, literals = catalog()
    src = {p: p.read_text() for p in D.rglob("*.puml") if "_style" not in p.parts and "tr" not in p.relative_to(D).parts[:1]}

    # 1. Fiziksel ERD == katalog
    erd = src[D / "database" / "physical-erd.puml"]
    ent = {m.group(1): m.group(2) for m in re.finditer(r'entity "(\w+)" as \w+ [^{]*\{(.*?)\n\}', erd, re.S)}
    check("physical ERD tables == catalog tables", set(ent) == set(cols), f"{set(ent) ^ set(cols)}")
    bad = []
    for t, body in ent.items():
        got = {}
        for line in body.splitlines():
            m = re.match(r"\s*\*?\s*\**(\w+)\**\s*:\s*([\w ]+?)(?:\s*<<\w+>>)?$", line.strip().lstrip("*").strip()) if ":" in line else None
            if m: got[m.group(1)] = m.group(2).strip()
        norm = lambda ty: ty.replace("timestamp with time zone", "timestamptz")
        want = {n: norm(ty) for n, ty in cols[t].items()}
        if got != want:
            bad.append((t, set(got.items()) ^ set(want.items())))
    check("physical ERD columns and types == catalog", not bad, str(bad)[:300])
    rel = len(re.findall(r"^\w+ [|o{}]+--[|o{}]+ \w+ :", erd, re.M))
    check("physical ERD relationship count == FK count", rel == len(fks), f"erd={rel} fk={len(fks)}")

    # 2. Durum makinesi == CHECK(status)
    sm = src[D / "state-machine" / "sm-01-job-state-machine.puml"]
    sm_states = set(re.findall(r'state "(\w+)" as', sm))
    check("state machine states == status CHECK values", sm_states == statuses, f"{sm_states ^ statuses}")

    # 3. Diyagramlarda geçen durum, hata kodu, rol, tablo adları geçerli mi
    all_text = "\n".join(v for k, v in src.items())
    used_status = set(re.findall(r"status\s*(?:=|IN \()\s*'?(\w+)", all_text)) - {"expected", "running"} | set()
    used_status = {s for s in re.findall(r"status\s*=\s*(\w+)", all_text)} | {s for s in re.findall(r"status IN \((\w+), (\w+)\)", all_text) for s in s}
    unknown = {s for s in used_status if s not in statuses and s not in {"done_or", "expected"}}
    check("statuses used in diagrams are valid", not unknown, str(unknown))
    codes = {"input_missing", "worker_lost", "generation_failed", "out_of_memory", "model_unavailable"}
    used_codes = set(re.findall(r"error_code\s*=?\s*(\w+_\w+)", all_text)) - {"error_code"}
    used_codes = {c for c in used_codes if c not in {"error_code"}}
    check("error codes used in diagrams are in the dictionary", used_codes <= codes, str(used_codes - codes))
    used_roles = set(re.findall(r"\b(cue_[a-z]+)\b", all_text))
    # cue_migrator = DDL sahibi hesap; dağıtımda oluşturulur, 0002 yalnız uygulama rollerini tanımlar
    check("DB roles named in diagrams exist (0002 roles + provisioned DDL owner cue_migrator)", used_roles <= roles | {"cue_migrator"}, str(used_roles - roles - {"cue_migrator"}))
    tables_mentioned = set(re.findall(r"\b(app_user|auth_session|media_asset|animation_job|model_version)\b", all_text))
    check("every DB table appears in at least one behavioural diagram", tables_mentioned == set(cols), str(set(cols) - tables_mentioned))
    # kolon adları: snake_case sözcükler katalogdaki sütun/tablo adı ya da bilinen SQL/uygulama terimi olmalı
    known_non_columns = {"clock_timestamp", "pg_advisory_xact_lock", "token_hash", "model_version", "idempotency_key", "docker_compose"}
    colnames = {n for c in cols.values() for n in c} | set(cols) | roles | names | literals
    allowed = known_non_columns | {"for_update", "skip_locked", "order_by", "range_requests", "dummy_hash", "job_id", "pg_dump"}  # job_id = JSON alanı (API), pg_dump = araç
    words = set(re.findall(r"\b([a-z]+_[a-z0-9_]+)\b", re.sub(r"<<.*?>>|!include.*|@start\w+ [\w-]+|\\n", " ", all_text)))
    ignore_prefix = ("cue_", "uc_", "act_", "sd_", "sm_", "dep_", "ai_", "arch_", "worker_lost", "input_missing", "generation_failed", "out_of_memory", "model_unavailable")
    unknown_cols = sorted(w for w in words if w not in colnames and w not in allowed and not w.startswith(ignore_prefix))
    check("snake_case identifiers in diagrams exist in the schema (or allow-list)", not unknown_cols, str(unknown_cols))

    # 4. Gereksinim kimlikleri
    valid_req = {f"FR-{i:02d}" for i in range(1, 13)} | {f"NFR-{i:02d}" for i in range(1, 8)}
    used_req = set(re.findall(r"\b(?:N?FR-\d\d)\b", all_text))
    check("requirement IDs in diagrams exist in the proposal", used_req <= valid_req, str(used_req - valid_req))
    must = {f"FR-{i:02d}" for i in range(1, 11)}
    check("FR-01..FR-10 each appear in at least one diagram", must <= used_req, str(must - used_req))
    check("decision IDs in diagrams are defined (D-02, D-03, D-07, D-09, D-13, D-18)", set(re.findall(r"\bD-\d\d\b", all_text)) <= {"D-02", "D-03", "D-07", "D-09", "D-13", "D-18"}, str(set(re.findall(r"\bD-\d\d\b", all_text))))

    # 5. Hf 1 zorunlu diyagramlar ve çıktı dosyaları
    required = ["use-case/uc-01-use-case", "architecture/arch-01-container", "activity/act-01-authentication", "activity/act-02-animation-creation",
                "activity/act-03-job-execution", "ai-pipeline/ai-01-pipeline", "state-machine/sm-01-job-state-machine",
                "database/physical-erd", "database/conceptual-erd", "deployment/dep-01-deployment", "sequence/sd-01-authentication",
                "sequence/sd-02-keyframe-upload", "sequence/sd-03-plan-preview", "sequence/sd-04a-job-submission", "sequence/sd-04b-job-execution",
                "sequence/sd-05-status-and-result", "sequence/sd-06-cancel-failure-delete"]
    for r in required:
        base = D / r
        files = {e: base.with_suffix(e) for e in (".puml", ".svg", ".png", ".pdf")}
        ok = all(p.exists() and p.stat().st_size > 1000 for p in files.values())
        why = ""
        if ok:
            svg = files[".svg"].read_text(errors="ignore")
            try:
                ET.fromstring(svg)
            except ET.ParseError as e:
                ok, why = False, f"svg xml: {e}"
            if "Syntax Error" in svg or "This syntax is deprecated" in svg or "is ignored" in svg:
                ok, why = False, "PlantUML hata/uyarı metni SVG içinde"
            w, h = struct.unpack(">II", files[".png"].read_bytes()[16:24])
            if w < 500 or h < 300:
                ok, why = False, f"png çok küçük {w}x{h}"
        check(f"artifact set complete and clean: {r}", ok, why or "eksik dosya")
    # PNG/SVG yeniliği: kaynak .puml'dan daha eski çıktı yok
    stale = [str(p.relative_to(D)) for p in D.rglob("*.puml") if "_style" not in p.parts and p.with_suffix(".png").exists() and p.stat().st_mtime > p.with_suffix(".png").stat().st_mtime + 1]
    check("no rendered artifact older than its source (EN and TR)", not stale, str(stale))

    # 6. Türkçe set: İngilizce kaynaktan yeniden üretilince birebir aynı, yapı ve kimlikler eşleşiyor, çıktılar temiz
    sys.path.insert(0, str(ROOT / "tools"))
    import build_tr
    errs = []
    in_sync, structure_ok, ids_ok, out_ok = [], [], [], []
    ident = re.compile(r"\b(?:N?FR-\d\d|D-\d\d|F-\d\d|SD-\d\w?|[a-z]+_[a-z0-9_]+)\b")
    for rel in sorted(build_tr.TR):
        en_path, tr_path = D / f"{rel}.puml", D / "tr" / f"{rel}.puml"
        expect = build_tr.render_tr(rel, errs)
        in_sync.append((rel, tr_path.exists() and tr_path.read_text() == expect))
        en_lines, tr_lines = en_path.read_text().splitlines(), tr_path.read_text().splitlines()
        tr_lines = [l for l in tr_lines if not l.startswith("' DİL:")]
        KEYWORDS = {"alt", "else", "opt", "loop", "group", "end", "note", "participant", "actor", "database", "storage", "rectangle", "node", "entity",
                    "state", "package", "usecase", "partition", "if", "elseif", "switch", "case", "repeat", "backward", "stop", "start", "legend",
                    "endlegend", "hide", "title", "skinparam", "autonumber", "@startuml", "@enduml", "!include", "left", "top"}
        def kind(l):   # serbest metin satırları 'text'; yapısal satırlar anahtar sözcük / ok / bölüm ayırıcı
            toks = l.split()
            if not toks:
                return ""
            if toks[0] in KEYWORDS or toks[0].startswith(("==", ":", "[*]", "'")):
                return toks[0] if not toks[0].startswith(":") else ":"
            if len(toks) > 1 and re.fullmatch(r"[-.<>|{}ox\[\]a-z]*[-.][-.<>|{}ox\]a-z]*", toks[1]) and ("-" in toks[1] or "." in toks[1]):
                return "arrow"
            return "text"
        structure_ok.append((rel, len(en_lines) == len(tr_lines) and [kind(l) for l in en_lines] == [kind(l) for l in tr_lines]))
        strip = lambda t: re.sub(r"!include.*|\\n|^' DİL:.*$", " ", t, flags=re.M)
        ids_en, ids_tr = set(ident.findall(strip(en_path.read_text()))), set(ident.findall(strip(tr_path.read_text())))
        ids_ok.append((rel, ids_en == ids_tr, sorted(ids_en ^ ids_tr)))
        base = D / "tr" / rel
        ok = all(base.with_suffix(e).exists() and base.with_suffix(e).stat().st_size > 1000 for e in (".svg", ".png", ".pdf"))
        if ok:
            svg = base.with_suffix(".svg").read_text(errors="ignore")
            try:
                ET.fromstring(svg)
            except ET.ParseError:
                ok = False
            if "Syntax Error" in svg or "is ignored" in svg or "This syntax is deprecated" in svg:
                ok = False
        out_ok.append((rel, ok))
    check("Turkish translation tables resolve against the English sources", not errs, str(errs)[:300])
    check("all 17 Turkish sources equal a fresh build from English + translation table", all(o for _, o in in_sync), str([r for r, o in in_sync if not o]))
    check("Turkish diagrams keep the English structure (line count, leading keywords)", all(o for _, o in structure_ok), str([r for r, o in structure_ok if not o]))
    check("Turkish diagrams keep all identifiers and requirement/decision IDs", all(o for _, o, _ in ids_ok), str([(r, d) for r, o, d in ids_ok if not o]))
    check("Turkish artifact sets (svg/png/pdf) exist and are clean", all(o for _, o in out_ok), str([r for r, o in out_ok if not o]))
    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    (ROOT / "reports" / "raw" / "consistency-check.txt").write_text("\n".join(("PASS " if ok else "FAIL ") + n + (f" -- {d}" if d and not ok else "") for n, ok, d in results) + f"\n\n{len(results) - len(failed)}/{len(results)} checks passed\n")
    sys.exit(1 if failed else 0)


main()
