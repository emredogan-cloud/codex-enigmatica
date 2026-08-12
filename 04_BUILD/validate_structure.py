#!/usr/bin/env python3
"""
DEPO, BELGE VE ÇÖZÜM KORUMASI — Codex Enigmatica
================================================================================
Beş ayrı denetim. Beşincisi bu projenin VAROLUŞSAL kapısıdır:

  ① ZORUNLU DOSYALAR       — yol haritasının söz verdiği belgeler var mı
  ② GÖMÜLÜ SABİT DEĞER     — yazar/yayıncı adı bir betiğe gömülmüş mü
  ③ MANUSCRIPT SIZINTISI   — bulmaca prozası takip edilen bir dosyaya sızmış mı
  ④ SIR SIZINTISI          — .env veya anahtar benzeri dize depoya girmiş mi
  ⑤ ⭑ ÇÖZÜM SIZINTISI ⭑    — bir bulmaca çözümü public depoya girmiş mi

⑤ NEDEN VAROLUŞSAL: bir bulmaca kitabının ÇÖZÜMLERİ ürünün kendisidir.
Public depoda duran bir çözüm, kitabı YAYIMLANMADAN değersizleştirir. Ve
bu hata geri alınamaz: git geçmişine giren bir çözümü silmek, geçmişi
yeniden yazmak demektir.

Ama dikkat: KOD SIR DEĞİLDİR. Bir doğrulayıcının kendisi public kalır ve
kalmalıdır. Sır olan yalnızca ÇÖZÜMDÜR. Bu ayrım CONTENT_PROTECTION.md'de
tanımlıdır ve bu betik onu uygular.

② NEDEN VAR: World Myths Faz 6'da yazar adı ÜÇ betikte ayrı ayrı gömülüydü
(covers.py, epub.py, handoff.py) ve metadata.py yer tutucu basıyordu — aynı
kitabın KAPAĞI ile METADATASI farklı yazar taşıyordu. Kusur Bestiarium D17'de
de vardı. Tek doğruluk kaynağı project_config.json'dur ve bu kapı onu korur.

③ NEDEN VAR: .gitignore YOL kalıplarıyla çalışır ve yeni bir ada konan dosyayı
YAKALAMAZ. Bu yüzden ikinci bir hat gerekir: takip edilen dosyaların İÇERİĞİNE
bakan bir tarayıcı. Politikayı disipline değil MEKANİZMAYA bağlarız.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

REQUIRED_FILES = [
    "README.md",
    "PROJECT_CONTEXT.md",
    "BRIEF.md",
    "DECISIONS.md",
    "CHANGELOG.md",
    "ROADMAP_PROGRESS.md",
    "BOOK_STATS.md",
    "project_config.json",
    ".gate",
    ".gitignore",
    "CODEX_ENIGMATICA_IMPLEMENTATION_ROADMAP.md",
    "00_CONTEXT/STYLE.md",
    "00_CONTEXT/SOLVABILITY_STANDARD.md",
    "00_CONTEXT/CONTENT_PROTECTION.md",
    "00_CONTEXT/HINT_LADDER.md",
    "00_CONTEXT/LESSONS_FROM_CODEX.md",
    "01_SOURCE/puzzle.schema.json",
    "04_BUILD/qa_all.sh",
    "04_BUILD/validate_spec.py",
    "05_TESTS/selftest.py",
    ".github/workflows/validate.yml",
]

REQUIRED_DIRS = [
    "00_CONTEXT", "01_SOURCE", "02_MANUSCRIPT", "03_COVER", "04_BUILD",
    "05_TESTS", "06_REPORTS", "07_ASSETS", "08_OUTPUT", "09_ARCHIVE",
    "01_SOURCE/puzzles", "01_SOURCE/research", "05_TESTS/puzzle",
    "07_ASSETS/raw", "07_ASSETS/processed", "07_ASSETS/plates",
]

# ② Gömülü sabit değer taraması ------------------------------------------------
# Bu dizeler YALNIZCA project_config.json içinde geçebilir.
SINGLE_SOURCE_VALUES = ["Emre Doğan", "Vâliçe Press"]
SCAN_CODE_EXT = (".py", ".sh", ".yml", ".yaml")
# Bu dosyalar muaf: config'in kendisi ve onu ANLATAN belgeler.
EMBED_SCAN_SKIP = {
    "project_config.json",
    "04_BUILD/validate_structure.py",   # tarayıcının kendisi dizeleri taşır
}

# ③ Manuscript sızıntısı -------------------------------------------------------
# Kural prozasının parmak izleri. Bir belge bunlardan BİRDEN ÇOK taşıyorsa
# ve manuscript dizininde değilse, proza sızmış olabilir.
LEAK_MARKERS = [
    r"\bEnigma\s+[IVXLC]+\s*[:.]",
    r"\bWhat you seek\b",
    r"\bThe plate conceals\b",
    r"\bTurn to the leaf\b",
]
LEAK_MIN_HITS = 2
LEAK_SCAN_EXT = (".md", ".json", ".txt", ".html")
# Muafiyet = yalnızca bu dosyalar kural dilini ÖRNEK olarak taşıyabilir.
#
# ⚠ HER MUAFİYET selftest § ④ TARAFINDAN İKİ KEZ DENETLENİR:
#   (a) dosya gerçekten var mı        → yoksa ÖLÜ MUAFİYET
#   (b) muafiyet olmasaydı yakalanır mıydı → hayırsa GEREKSİZ MUAFİYET
#
# Bu yüzden listeye "ihtimale karşı" dosya eklenmez. Bir dosya ancak kural
# dilini GERÇEKTEN taşıdığı için buraya girer.
# (World Myths K14 · Bestiarium D28: ölü kural sessizce yanlış güven verir.)
# puzzle.schema.json BİLEREK BURADA DEĞİL: şema bulmaca PROZASI taşımaz,
# yalnızca alan adları taşır — dolayısıyla bu taramada zaten yakalanmaz.
# Gereksiz bir muafiyet, kapıda açılmış boş bir deliktir (selftest § ④).
LEAK_SCAN_SKIP = {
    "00_CONTEXT/STYLE.md",
}

# ⑤ ⭑ ÇÖZÜM SIZINTISI ⭑ — bu projenin varoluşsal kapısı ---------------------
# Çözüm ALAN ADLARI. Bunlar project_config.json §
# contentProtection.solutionFieldNames ile senkron olmak zorundadır ve
# validate_spec.py o senkronu ayrıca denetler.
SOLUTION_FIELD_MARKERS = [
    r'"solution"\s*:',
    r'"intendedSolution"\s*:',
    r'"answer"\s*:',
    r'"answerKey"\s*:',
    r'"solutionPath"\s*:',
    r'"hints"\s*:',
    r"\bSOLUTION\s*[:—-]",
    r"\bANSWER KEY\b",
]
SOLUTION_MIN_HITS = 1
# ⚠ MUAFİYET LİSTESİ ÇOK KISA TUTULUR.
# Şema alan adlarını TANIMLAR (değer taşımaz); bu betik ve selftest
# kalıpların kendisini taşır. Başka hiçbir dosya muaf DEĞİLDİR.
# ⚠ YALNIZCA İKİ DOSYA. Bu liste selftest § ④ tarafından hem UZUNLUK hem
# GEREKLİLİK açısından denetlenir.
#
# Burada OLMAYAN ve olması beklenebilecek iki dosya:
#   · validate_structure.py — kalıpları regex olarak taşır (`"solution"\s*:`),
#     düz metin olarak DEĞİL; bu taramada zaten yakalanmaz
#   · selftest.py — kurgu çözümü `["solution"] = "..."` biçiminde yazar,
#     yani iki nokta üst üste yoktur; bu taramada zaten yakalanmaz
# İkisi de muafiyet GEREKTİRMEZ ve bu yüzden listede DEĞİLDİR.
SOLUTION_SCAN_SKIP = {
    "01_SOURCE/puzzle.schema.json",
    "00_CONTEXT/CONTENT_PROTECTION.md",
}
# Bu dizinler ASLA takip edilemez. Bir dosyanın burada VE git'te olması
# tek başına ihlaldir — içeriğine bakmaya gerek yoktur.
PROTECTED_DIRS = ("01_SOURCE/solutions/", "09_ARCHIVE/solutions/",
                  "06_REPORTS/solver/")

# ④ Sır taraması ---------------------------------------------------------------
SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI benzeri anahtar"),
    (r"gh[pousr]_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"AKIA[0-9A-Z]{16}", "AWS anahtar kimliği"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "özel anahtar"),
]

FAKE_ISBN = re.compile(r"\b97[89][- ]?\d{1,5}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?\d\b")


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0

    def check(self, cond: bool, label: str) -> bool:
        self.checks += 1
        if cond:
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.errors.append(label)
            print("  ✗ %s" % label)
        return cond

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)


def tracked_files() -> list[str]:
    """git ls-files — TAKİP EDİLEN dosyalar. Sızıntı denetimi yalnızca
    bunlara bakar: takip edilmeyen dosya zaten public değildir."""
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            return []
        return [p for p in out.stdout.splitlines() if p.strip()]
    except (OSError, subprocess.SubprocessError):
        return []


def check_files(rep: Report) -> None:
    print("\n── zorunlu dosya ve dizinler ──")
    for rel in REQUIRED_DIRS:
        rep.check(os.path.isdir(os.path.join(ROOT, rel)), "dizin: %s" % rel)
    for rel in REQUIRED_FILES:
        rep.check(os.path.isfile(os.path.join(ROOT, rel)), "dosya: %s" % rel)


def check_gate_file(rep: Report) -> None:
    print("\n── .gate ──")
    path = os.path.join(ROOT, ".gate")
    if not os.path.exists(path):
        rep.check(False, ".gate dosyası var")
        return
    with open(path, encoding="utf-8") as fh:
        lvl = fh.read().strip()
    rep.check(lvl in ("phase0", "phase1", "phase2", "phase3", "phase4",
                      "phase5", "release"),
              ".gate geçerli bir seviye taşıyor: '%s'" % lvl)


def check_embedded(rep: Report, files: list[str]) -> None:
    print("\n── gömülü sabit değer (tek doğruluk kaynağı) ──")
    hits: list[str] = []
    for rel in files:
        if rel in EMBED_SCAN_SKIP or not rel.endswith(SCAN_CODE_EXT):
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        for val in SINGLE_SOURCE_VALUES:
            if val in body:
                hits.append("%s → '%s'" % (rel, val))
    rep.check(not hits,
              "kurucu değerleri yalnızca project_config.json'da" +
              ("" if not hits else " — GÖMÜLÜ: %s" % hits[:5]))


def check_manuscript_leak(rep: Report, files: list[str]) -> None:
    print("\n── manuscript sızıntısı ──")
    leaked: list[str] = []
    for rel in files:
        if rel in LEAK_SCAN_SKIP or not rel.endswith(LEAK_SCAN_EXT):
            continue
        if rel.startswith("02_MANUSCRIPT/"):
            # Manuscript dizinindeki TAKİP EDİLEN her dosya zaten ihlaldir.
            if os.path.basename(rel) not in (".gitkeep", "README.md"):
                leaked.append("%s (manuscript dizini takip ediliyor)" % rel)
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        hits = sum(1 for pat in LEAK_MARKERS if re.search(pat, body))
        if hits >= LEAK_MIN_HITS:
            leaked.append("%s (%d kural işareti)" % (rel, hits))
    rep.check(not leaked,
              "kural prozası depoya sızmamış" +
              ("" if not leaked else " — SIZINTI: %s" % leaked[:5]))


def check_secrets(rep: Report, files: list[str]) -> None:
    print("\n── sır ve sahte ISBN taraması ──")
    rep.check(".env" not in files, ".env takip edilmiyor")

    found: list[str] = []
    for rel in files:
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p) or os.path.getsize(p) > 2_000_000:
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        for pat, name in SECRET_PATTERNS:
            if re.search(pat, body):
                found.append("%s → %s" % (rel, name))
    rep.check(not found,
              "sır benzeri dize yok" + ("" if not found else " — %s" % found[:3]))

    # Sahte ISBN: kurucu kararı KDP ücretsiz ISBN. Uydurulmuş numara YASAK.
    cfgp = os.path.join(ROOT, "project_config.json")
    strategy = "kdp-free"
    if os.path.exists(cfgp):
        try:
            with open(cfgp, encoding="utf-8") as fh:
                strategy = json.load(fh).get("founder", {}).get(
                    "isbn", {}).get("strategy", "kdp-free")
        except (OSError, json.JSONDecodeError):
            pass
    if strategy == "kdp-free":
        isbn_hits: list[str] = []
        for rel in files:
            if not rel.endswith((".md", ".json", ".py")):
                continue
            if rel in ("04_BUILD/validate_structure.py",):
                continue
            p = os.path.join(ROOT, rel)
            if not os.path.isfile(p):
                continue
            try:
                with open(p, encoding="utf-8") as fh:
                    body = fh.read()
            except (OSError, UnicodeDecodeError):
                continue
            if FAKE_ISBN.search(body):
                isbn_hits.append(rel)
        rep.check(not isbn_hits,
                  "uydurulmuş ISBN yok (strateji: kdp-free)" +
                  ("" if not isbn_hits else " — %s" % isbn_hits[:3]))


def check_solution_leak(rep: Report, files: list[str]) -> None:
    """⑤ ⭑ Bir bulmaca çözümü public depoya girmiş mi. ⭑

    İki ayrı hat:
      (a) KORUMALI DİZİN — bu dizinlerdeki HERHANGİ bir takip edilen dosya
          tek başına ihlaldir; içeriğe bakılmaz.
      (b) İÇERİK TARAMASI — çözüm alan adları başka bir dosyaya taşınmışsa
          yol kalıbı onu yakalamaz; bu tarama yakalar.
    """
    print("\n── ⭑ ÇÖZÜM SIZINTISI ⭑ ──")

    in_protected = [f for f in files if f.startswith(PROTECTED_DIRS)
                    and os.path.basename(f) not in (".gitkeep", "README.md")]
    rep.check(not in_protected,
              "korumalı dizinlerde takip edilen dosya yok" +
              ("" if not in_protected else " — İHLAL: %s" % in_protected[:5]))

    leaked: list[str] = []
    for rel in files:
        if rel in SOLUTION_SCAN_SKIP:
            continue
        if not rel.endswith((".json", ".md", ".txt", ".html", ".csv")):
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        hits = sum(1 for pat in SOLUTION_FIELD_MARKERS if re.search(pat, body))
        if hits >= SOLUTION_MIN_HITS:
            leaked.append("%s (%d çözüm işareti)" % (rel, hits))
    rep.check(not leaked,
              "çözüm alanı public depoda YOK" +
              ("" if not leaked else " — ⛔ SIZINTI: %s" % leaked[:5]))


def check_doc_links(rep: Report) -> None:
    print("\n── belge bağları ──")
    broken: list[str] = []
    for rel in REQUIRED_FILES:
        if not rel.endswith(".md"):
            continue
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            body = fh.read()
        for m in re.finditer(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)", body):
            target = m.group(1).split("#")[0]
            if not target:
                continue
            base = os.path.dirname(p)
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                broken.append("%s → %s" % (rel, target))
    rep.check(not broken,
              "belge içi bağlar çözülüyor" +
              ("" if not broken else " — KIRIK: %s" % broken[:5]))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  DEPO, BELGE VE MANUSCRIPT KORUMASI")
    print("=" * 74)

    rep = Report(args.verbose)
    files = tracked_files()
    if not files:
        rep.warn("git takip listesi boş — depo henüz init edilmemiş olabilir; "
                 "sızıntı denetimleri boş koşuyor")

    check_files(rep)
    check_gate_file(rep)
    check_embedded(rep, files)
    check_manuscript_leak(rep, files)
    check_secrets(rep, files)
    check_solution_leak(rep, files)
    check_doc_links(rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil" % rep.checks)
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "trackedFiles": len(files)},
                      fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
