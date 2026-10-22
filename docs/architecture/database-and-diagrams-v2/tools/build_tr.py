"""İngilizce .puml kaynaklarından Türkçe sürümleri üretir: diagrams/tr/<grup>/<ad>.puml (çıktılar render.sh ile).
Yapı İngilizce kaynaktan gelir (tek doğruluk kaynağı); yalnızca tools/i18n_tr.py'deki etiket çiftleri değişir.
Bir çeviri çifti bulunamazsa derleme HATA verir (İngilizce kaynak değiştiyse çeviri sessizce eskimez).
Kullanım: python3 tools/build_tr.py"""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from i18n_tr import TR, BRANCH_FILES

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "diagrams"
HEADER = "' DİL: Türkçe — OTOMATİK ÜRETİLDİ (tools/build_tr.py); elle düzenlemeyin, İngilizce kaynak ve tools/i18n_tr.py esastır.\n"


def english_sources():
    return {str(p.relative_to(D).with_suffix("")) for p in D.rglob("*.puml")
            if "_style" not in p.parts and p.relative_to(D).parts[0] != "tr"}


def render_tr(rel, errors):
    """Bir diyagramın Türkçe kaynak metnini döndürür; bulunamayan çeviri çiftlerini errors'a ekler."""
    text = (D / f"{rel}.puml").read_text()
    for en, tr in sorted(TR[rel], key=lambda p: -len(p[0])):
        if en not in text:
            errors.append(f"{rel}: çeviri çifti bulunamadı: {en[:80]!r}")
            continue
        text = text.replace(en, tr)
    if rel in BRANCH_FILES:
        text = re.sub(r"\(yes([):,])", r"(evet\1", text)
        text = re.sub(r"\(no([):,])", r"(hayır\1", text)
    text = text.replace("!include ../_style/cue.iuml", "!include ../../_style/cue.iuml")
    return text.replace("@startuml ", HEADER + "@startuml ", 1)


def main():
    errors = []
    for rel in TR:
        text = render_tr(rel, errors)
        out = D / "tr" / f"{rel}.puml"
        out.parent.mkdir(parents=True, exist_ok=True)
        if not out.exists() or out.read_text() != text:      # içerik değişmediyse dokunma (çıktılar bayatlamasın)
            out.write_text(text)
    missing = english_sources() - set(TR)
    if missing:
        errors.append(f"çevirisi olmayan diyagramlar: {sorted(missing)}")
    if errors:
        print("\n".join(errors)); sys.exit(1)
    print(f"{len(TR)} Türkçe kaynak üretildi.")


if __name__ == "__main__":
    main()
