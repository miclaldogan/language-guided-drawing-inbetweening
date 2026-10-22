"""Medya deposu ↔ veritabanı protokolünün REFERANS gerçeklemesi (yalnız doğrulama amaçlı; uygulama kodu DEĞİLDİR).
v1/04 §4-5'teki yazma/silme sırası kurallarını ve hata senaryolarını çalıştırılabilir kılar:
  - önce dosya (tmp -> fsync -> atomik rename), sonra DB kaydı
  - silmede önce DB (RETURNING storage_key), commit sonrası dosya
  - sahipsiz dosya süpürücü (yaş eşiği), bağlanmamış yükleme temizliği, tutarlılık raporu, silme defteri."""
import hashlib, os, pathlib, time, uuid


class LocalMediaStore:
    def __init__(self, root):
        self.root = pathlib.Path(root)
        (self.root / "tmp").mkdir(parents=True, exist_ok=True)

    def _p(self, key):
        return self.root / key

    def put(self, key, data: bytes, fail_before_rename=False):
        tmp = self.root / "tmp" / uuid.uuid4().hex
        with open(tmp, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        if fail_before_rename:               # yazım yarıda kesildi: son anahtar altında hiçbir şey görünmez
            raise OSError("simulated crash before rename")
        final = self._p(key)
        final.parent.mkdir(parents=True, exist_ok=True)
        os.replace(tmp, final)

    def exists(self, key):
        return self._p(key).is_file()

    def read(self, key):
        return self._p(key).read_bytes()

    def delete(self, key, fail=False):
        if fail:
            raise OSError("simulated delete failure")
        self._p(key).unlink(missing_ok=True)

    def list_keys(self):
        """(anahtar, mtime) — tmp/ hariç."""
        out = []
        for p in self.root.rglob("*"):
            if p.is_file() and "tmp" not in p.relative_to(self.root).parts[:1]:
                out.append((str(p.relative_to(self.root)), p.stat().st_mtime))
        return out


def new_key(ext="png"):
    h = uuid.uuid4().hex
    return f"assets/{h[:2]}/{h}.{ext}"


def upload(conn, store, owner, kind, data, ext="png", store_fails=False, insert_fails=False):
    """Dosya önce, kayıt sonra. conn: cue_api (autocommit). Dönüş: asset id."""
    key = new_key(ext)
    store.put(key, data, fail_before_rename=store_fails)           # başarısızsa DB'ye hiç dokunulmaz
    sha = hashlib.sha256(data).hexdigest()
    ct = "video/mp4" if kind == "result_video" else "image/png"
    size = 0 if insert_fails else len(data)                        # size=0 -> CHECK ihlali (kayıt başarısız senaryosu)
    return conn.execute(
        "INSERT INTO media_asset(owner_id,kind,storage_key,content_type,byte_size,width,height,sha256) VALUES (%s,%s,%s,%s,%s,512,320,%s) RETURNING id",
        (owner, kind, key, ct, size, sha)).fetchone()[0]


def sweep_orphans(maint, store, min_age_s=3600, apply=True, now=None):
    """DB'de karşılığı olmayan ve yaşı >= eşik olan dosyalar. apply=False: yalnız rapor (yedekten dönüş sonrası kuralı)."""
    now = now or time.time()
    known = {k for (k,) in maint.execute("SELECT storage_key FROM media_asset")}
    orphans = [k for k, mt in store.list_keys() if k not in known and now - mt >= min_age_s]
    if apply:
        for k in orphans:
            store.delete(k)
    return orphans


def cleanup_unattached(maint, store, older_than="24 hours"):
    """İşe bağlanmamış eski giriş varlıkları: önce DB satırları, sonra dosyalar.
    İki ayrı NOT EXISTS (OR yerine): 450 bin varlıkta gözlenen süre ≈410-520 ms -> ≈110 ms (reports/08, bulgu F-07)."""
    rows = maint.execute(
        "DELETE FROM media_asset a WHERE a.kind IN ('start_drawing','end_drawing') AND a.created_at < clock_timestamp() - %s::interval "
        "AND NOT EXISTS (SELECT 1 FROM animation_job j WHERE j.start_asset_id=a.id) AND NOT EXISTS (SELECT 1 FROM animation_job j WHERE j.end_asset_id=a.id) RETURNING storage_key",
        (older_than,)).fetchall()
    for (k,) in rows:
        store.delete(k)
    return [k for (k,) in rows]


def delete_job(api, store, job_id, owner, ledger=None, file_delete_fails=False):
    """Terminal durumdaki işi siler. Dönüş: 'not_found' | 'conflict' | 'deleted'. Etkin işte silme reddedilir (karar D-03)."""
    st = api.execute("SELECT status FROM animation_job WHERE id=%s AND owner_id=%s", (job_id, owner)).fetchone()
    if st is None:
        return "not_found"
    if st[0] in ("queued", "running"):
        return "conflict"
    with api.transaction():
        ids = api.execute("DELETE FROM animation_job WHERE id=%s AND owner_id=%s AND status IN ('done','failed','cancelled') "
                          "RETURNING start_asset_id,end_asset_id,thumbnail_asset_id,video_asset_id,frames_asset_id", (job_id, owner)).fetchone()
        if ids is None:
            return "conflict"
        keys = [k for (k,) in api.execute("DELETE FROM media_asset WHERE id = ANY(%s) RETURNING storage_key", ([i for i in ids if i],))]
    if ledger is not None:
        with open(ledger, "a") as f:
            f.write(f"{job_id}\n")
    for i, k in enumerate(keys):                                    # commit sonrası; hata -> sahipsiz dosya kalır, kayıt zaten yok
        try:
            store.delete(k, fail=file_delete_fails)
        except OSError:
            pass
    return "deleted"


def serve_video(api, store, job_id, owner):
    """Video akıtma kararı: (durum, bayt). Dosya yoksa iş kaydı DEĞİŞMEZ."""
    row = api.execute("SELECT m.storage_key FROM animation_job j JOIN media_asset m ON m.id=j.video_asset_id "
                      "WHERE j.id=%s AND j.owner_id=%s AND j.status='done'", (job_id, owner)).fetchone()
    if row is None:
        return ("404", None)
    if not store.exists(row[0]):
        return ("unavailable", None)
    return ("200", store.read(row[0]))


def serve_frame(api, store, job_id, owner, n):
    """S6 kare gezinme: tek kareyi ZIP arşivinden okur. Dönüş: (durum, bayt). n 1..frame_count; başkasının işi 404."""
    import io, zipfile
    row = api.execute("SELECT m.storage_key, j.frame_count FROM animation_job j JOIN media_asset m ON m.id=j.frames_asset_id "
                      "WHERE j.id=%s AND j.owner_id=%s AND j.status='done'", (job_id, owner)).fetchone()
    if row is None or not (1 <= n <= row[1]):
        return ("404", None)
    if not store.exists(row[0]):
        return ("unavailable", None)
    with zipfile.ZipFile(io.BytesIO(store.read(row[0]))) as z:
        return ("200", z.read(f"{n:03d}.png"))


def build_frames_zip(n=16):
    """Test için: n adet sahte PNG içeren ZIP (store modu: PNG zaten sıkıştırılmış)."""
    import io, zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as z:
        for i in range(1, n + 1):
            z.writestr(f"{i:03d}.png", b"\x89PNG-frame-%03d" % i)
    return buf.getvalue()


def reconcile_report(conn, store):
    """DB ↔ dosya farkları (yalnız rapor): sahipsiz dosyalar, dosyası olmayan satırlar, boyut/özet uyuşmazlığı."""
    rows = conn.execute("SELECT storage_key, byte_size, sha256 FROM media_asset").fetchall()
    known = {k for k, _, _ in rows}
    on_disk = {k for k, _ in store.list_keys()}
    missing = sorted(k for k in known if k not in on_disk)
    mismatch = []
    for k, size, sha in rows:
        if k in on_disk:
            data = store.read(k)
            if len(data) != size or hashlib.sha256(data).hexdigest() != sha:
                mismatch.append(k)
    return dict(orphan_files=sorted(on_disk - known), missing_files=missing, mismatched=sorted(mismatch))


def reapply_deletions(admin, ledger):
    """Yedekten dönüşte yeniden beliren silinmiş işleri silme defterine göre tekrar siler (NFR-05)."""
    ids = [l.strip() for l in open(ledger) if l.strip()]
    removed = []
    for jid in ids:
        r = admin.execute("DELETE FROM animation_job WHERE id=%s RETURNING start_asset_id,end_asset_id,thumbnail_asset_id,video_asset_id,frames_asset_id", (jid,)).fetchone()
        if r:
            keys = [k for (k,) in admin.execute("DELETE FROM media_asset WHERE id = ANY(%s) RETURNING storage_key", ([i for i in r if i],))]
            removed.append((jid, keys))
    return removed
