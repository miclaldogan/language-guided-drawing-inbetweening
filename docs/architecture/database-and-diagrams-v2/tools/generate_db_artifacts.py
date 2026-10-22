"""Çalışan (tek kullanımlık) PostgreSQL 18'den veri sözlüğü, indeks belgesi ve fiziksel ERD kaynağını üretir.
Diyagram ile DDL arasındaki tutarlılık böylece yapıdan gelir: tek kaynak = migrations/*.up.sql.
Kullanım: uv run --no-project --with 'psycopg[binary]' --with pytest python tools/generate_db_artifacts.py"""
import pathlib, sys, uuid
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "database" / "validation"))
import conftest as cf  # noqa: E402

PURPOSE = {
    "app_user_email_key": "Girişte e-posta araması; kayıtta benzersizlik (FR-01).",
    "auth_session_token_hash_key": "Her istekte oturum çözme (en sık sorgu, Q6).",
    "auth_session_user_id_idx": "Hesap silme ve FK denetimi.",
    "model_version_name_label_key": "Aday anahtar: (ad, sürüm etiketi).",
    "model_version_single_active_idx": "Değişmez: en çok bir etkin model sürümü; Q9.",
    "media_asset_storage_key_key": "Depo anahtarı benzersiz.",
    "media_asset_id_owner_key": "Bileşik FK hedefi: iş→varlık sahiplik denetimi.",
    "media_asset_owner_id_idx": "Hesap silme, sahip başına envanter, FK denetimi.",
    "animation_job_owner_created_idx": "Kitaplık listesi + keyset sayfalama (Q1); sahip süzmesi.",
    "animation_job_queue_idx": "Kuyruktan en eski bekleyen iş (Q3); yalnız queued satırlar.",
    "animation_job_running_hb_idx": "Takılı iş bulma (Q4); yalnız running satırlar.",
    "animation_job_owner_idem_key": "İdempotency: (sahip, anahtar) benzersiz.",
    "animation_job_start_asset_key": "Bir varlık en çok bir işin başlangıç çizimi; FK denetimi.",
    "animation_job_end_asset_key": "Bir varlık en çok bir işin bitiş çizimi; FK denetimi.",
    "animation_job_video_asset_key": "Bir video en çok bir işe ait.",
    "animation_job_frames_asset_key": "Bir kare arşivi en çok bir işe ait (karar D-09).",
    "animation_job_thumb_asset_key": "Bir küçük resim en çok bir işe ait.",
}
NOT_CREATED = [
    ("animation_job (owner_id, status, …)", "Panelde süzme yok; kullanıcı başına satır sayısı küçük."),
    ("animation_job (finished_at) WHERE status='failed'", "Çok seyrek operatör sorgusu (Q8); ölçülmeden eklenmez."),
    ("animation_job (model_version_id)", "model_version satırları silinmez."),
    ("auth_session (expires_at)", "Günlük temizlik küçük tabloda tarama; her oturum eklemesinde ek yazma maliyeti gereksiz."),
    ("media_asset (created_at)", "Bağlanmamış yükleme temizliği günlük ve küçük tabloda."),
    ("GIN (plan jsonb)", "Planı aramak gereksinimi yok."),
]
ORDER = ["app_user", "auth_session", "model_version", "media_asset", "animation_job"]
DEL = {"a": "NO ACTION", "r": "RESTRICT", "c": "CASCADE", "n": "SET NULL", "d": "SET DEFAULT"}


def main():
    import contextlib
    pw = cf.secrets.token_hex(16); name = f"cue-gen-{cf.os.getpid()}"
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
        out = ROOT / "database"
        write_dictionary(c, out / "data-dictionary.md")
        write_indexes(c, out / "indexes.md")
        write_erd(c, ROOT / "diagrams" / "database" / "physical-erd.puml")
    finally:
        cf.subprocess.run(["docker", "rm", "-f", name], capture_output=True)


def write_if_changed(path, text):
    """İçerik değişmediyse dosyaya dokunma (render çıktıları bayatlamasın)."""
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


def cols(c, t):
    return c.execute("""
      SELECT a.attname, format_type(a.atttypid,a.atttypmod), a.attnotnull, pg_get_expr(d.adbin,d.adrelid), col_description(a.attrelid,a.attnum), a.attnum
      FROM pg_attribute a LEFT JOIN pg_attrdef d ON d.adrelid=a.attrelid AND d.adnum=a.attnum
      WHERE a.attrelid=%s::regclass AND a.attnum>0 AND NOT a.attisdropped ORDER BY a.attnum""", (t,)).fetchall()


def keys(c, t):
    pk, uq, fk = set(), set(), set()
    for ctype, cols_ in c.execute("""SELECT contype, array(SELECT attname FROM pg_attribute WHERE attrelid=conrelid AND attnum=ANY(conkey)) FROM pg_constraint WHERE conrelid=%s::regclass""", (t,)):
        if ctype == "p": pk |= set(cols_)
        elif ctype == "u" and len(cols_) == 1: uq |= set(cols_)
        elif ctype == "f": fk |= set(cols_)
    return pk, uq, fk


def write_dictionary(c, path):
    L = ["# Veri Sözlüğü (PostgreSQL 18)", "",
         "**Durum:** ÖNERİ, ONAYLANMADI. **OTOMATİK ÜRETİLDİ** (`tools/generate_db_artifacts.py`), tek kaynak `database/migrations/*.up.sql`. Elle düzenlemeyin.",
         "Zaman damgaları `timestamptz` (UTC). Anahtar: **PK** birincil, **FK** yabancı, **UQ** tek sütunlu benzersiz. \"Değişmez\" sütunlar uygulama rollerine UPDATE yetkisi verilmeyerek korunur (bkz. Yetkiler).", ""]
    for t in ORDER:
        desc = c.execute("SELECT obj_description(%s::regclass)", (t,)).fetchone()[0]
        pk, uq, fk = keys(c, t)
        L += [f"## `{t}`", "", desc or "", "", "| Sütun | Tip | Null | Varsayılan | Anahtar | Açıklama |", "| --- | --- | --- | --- | --- | --- |"]
        for n, ty, nn, dflt, cm, _ in cols(c, t):
            k = ", ".join(x for x, s in (("PK", pk), ("FK", fk), ("UQ", uq)) if n in s)
            L.append(f"| `{n}` | `{ty}` | {'hayır' if nn else 'evet'} | {('`'+dflt+'`') if dflt else ''} | {k} | {cm or ''} |")
        L += ["", "**Kısıtlar:**", ""]
        for cn, ct, df in c.execute("SELECT conname, contype, pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid=%s::regclass ORDER BY contype, conname", (t,)):
            if ct == "n":   # PostgreSQL 18 NOT NULL kısıtlarını da pg_constraint'te tutar; sütun tablosunda zaten gösterilir
                continue
            if ct == "f":
                act = c.execute("SELECT confdeltype FROM pg_constraint WHERE conname=%s AND conrelid=%s::regclass", (cn, t)).fetchone()[0]
                df += f"  — silme: {DEL[act]}"
            L.append(f"- `{cn}` ({ {'p':'PK','u':'UNIQUE','f':'FK','c':'CHECK'}[ct] }): `{df}`")
        L.append("")
    L += ["## Yetkiler (rol × tablo)", "", "Roller `NOLOGIN` grup rolleridir; giriş hesapları dağıtımda üye yapılır. UPDATE yalnız listelenen sütunlarda.", "",
          "| Rol | Tablo | Tablo yetkileri | Sütun düzeyi UPDATE |", "| --- | --- | --- | --- |"]
    for role in ("cue_api", "cue_worker", "cue_maintenance"):
        for t in ORDER:
            tp = [p for (p,) in c.execute("SELECT privilege_type FROM information_schema.role_table_grants WHERE grantee=%s AND table_name=%s ORDER BY 1", (role, t))]
            up = [n for (n,) in c.execute(
                "SELECT cp.column_name FROM information_schema.column_privileges cp "
                "JOIN information_schema.columns ic USING (table_schema,table_name,column_name) "
                "WHERE cp.grantee=%s AND cp.table_name=%s AND cp.privilege_type='UPDATE' ORDER BY ic.ordinal_position", (role, t))]
            tp_nonupd = [p for p in tp if p != "UPDATE"]
            if tp_nonupd or up:
                L.append(f"| `{role}` | `{t}` | {', '.join(tp_nonupd) or '—'} | {', '.join('`'+u+'`' for u in up) or '—'} |")
            # hiçbir uygulama rolüne tablo düzeyi UPDATE verilmemiş olmalı (yalnız sütun düzeyi)
            assert "UPDATE" not in tp, f"{role}.{t}: tablo düzeyi UPDATE olmamalı"
    write_if_changed(path, "\n".join(L) + "\n")


def write_indexes(c, path):
    L = ["# İndeks Stratejisi", "", "**Durum:** ÖNERİ, ONAYLANMADI. **OTOMATİK ÜRETİLDİ** (`tools/generate_db_artifacts.py`). Performans iddiası yoktur; indeksler erişim yoluna göre seçilmiştir.", "",
         "| Tablo | İndeks | Tanım | Amaç |", "| --- | --- | --- | --- |"]
    for t in ORDER:
        for n, df in c.execute("SELECT indexname, indexdef FROM pg_indexes WHERE schemaname='public' AND tablename=%s ORDER BY indexname", (t,)):
            if n.endswith("_pkey"): why = "Birincil anahtar."
            else: why = PURPOSE[n]
            L.append(f"| `{t}` | `{n}` | `{df.split(' USING ')[1]}` | {why} |")
    L += ["", "## Bilinçli olarak OLUŞTURULMAYAN indeksler", "", "| Aday | Gerekçe |", "| --- | --- |"]
    L += [f"| {a} | {b} |" for a, b in NOT_CREATED]
    L += ["", "## Temsili sorgular ve doğrulanan erişim yolları", "",
          "`database/validation/test_schema.py::test_indexes_are_usable_for_access_paths` her erişim yolunun ilgili indeksi **kullanabildiğini** `EXPLAIN` ile doğrular (küçük tabloda `enable_seqscan=off`). Bu bir hız ölçümü değildir.", "",
          "| Erişim yolu | İndeks |", "| --- | --- |",
          "| Kitaplık, keyset sayfalama | `animation_job_owner_created_idx` |", "| İş kapma (en eski `queued`) | `animation_job_queue_idx` |",
          "| Takılı iş (`running`, eski heartbeat) | `animation_job_running_hb_idx` |", "| İdempotency araması | `animation_job_owner_idem_key` |",
          "| Oturum çözme | `auth_session_token_hash_key` |", "| Girişte e-posta | `app_user_email_key` |"]
    write_if_changed(path, "\n".join(L) + "\n")


def write_erd(c, path):
    fkeys = {}
    for t in ORDER:
        fkeys[t] = keys(c, t)
    L = ["@startuml physical-erd", "!include ../_style/cue.iuml", "hide circle", "skinparam ranksep 150", "skinparam nodesep 45", "left to right direction", "",
         "title Cue — Physical ERD (PostgreSQL 18)\\nGenerated from database/migrations/*.up.sql", ""]
    layer = {"app_user": "#E6F4EA;line:2F855A", "auth_session": "#E6F4EA;line:2F855A", "model_version": "#F1E8FB;line:6B46C1",
             "media_asset": "#FFF4DB;line:B7791F", "animation_job": "#E6F4EA;line:2F855A"}
    for t in ORDER:
        pk, uq, fk = fkeys[t]
        L.append(f'entity "{t}" as {t} {layer[t]} {{')
        for n, ty, nn, dflt, cm, _ in cols(c, t):
            if n in pk:
                L.append(f"  * **{n}** : {ty} <<PK>>")
        L.append("  --")
        for n, ty, nn, dflt, cm, _ in cols(c, t):
            if n in pk: continue
            tag = " <<FK>>" if n in fk else (" <<UQ>>" if n in uq else "")
            L.append(f"  {'*' if nn else ' '} {n} : {ty.replace('timestamp with time zone', 'timestamptz')}{tag}")
        L.append("}")
        L.append("")
    # ilişkiler (katalogdan türetilir)
    rels = []
    for t in ORDER:
        for cn, ref, colnames, deltype in c.execute("""
            SELECT conname, confrelid::regclass::text, array(SELECT attname FROM pg_attribute WHERE attrelid=conrelid AND attnum=ANY(conkey)), confdeltype
            FROM pg_constraint WHERE contype='f' AND conrelid=%s::regclass ORDER BY conname""", (t,)):
            nullable = any(not nn for n, _, nn, *_ in cols(c, t) if n in colnames)
            uniq = False
            for (idxcols,) in c.execute("""SELECT array(SELECT attname FROM pg_attribute WHERE attrelid=i.indrelid AND attnum=ANY(i.indkey)) FROM pg_index i WHERE i.indrelid=%s::regclass AND i.indisunique""", (t,)):
                if set(idxcols) <= set(colnames): uniq = True
            parent_sym = "|o" if nullable else "||"
            child_sym = "o|" if uniq else "o{"
            label = ", ".join(x for x in colnames if x != "owner_id") if len(colnames) > 1 else colnames[0]
            rels.append((ref, t, parent_sym, child_sym, f"{label}"))
    for ref, t, p, ch, label in rels:
        L.append(f'{ref} {p}--{ch} {t} : "{label}"')
    L += ["", "legend right", "  * = NOT NULL", "  PK/FK/UQ = primary / foreign / single-column unique key",
          "  media_asset -> animation_job relations are composite FKs: (<label>, owner_id) -> media_asset(id, owner_id);",
          "  the job and its assets must belong to the same user. Delete: auth_session CASCADE; the others RESTRICT/NO ACTION.",
          "  Details: database/data-dictionary.md (columns, constraints), database/indexes.md (indexes)", "endlegend", "@enduml"]
    write_if_changed(path, "\n".join(L) + "\n")


if __name__ == "__main__":
    main()
