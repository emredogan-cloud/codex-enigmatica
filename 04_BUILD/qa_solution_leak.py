#!/usr/bin/env python3
"""
⭑ ÇÖZÜM KANARYASI ⭑ — değer tarafı sızıntı denetimi
================================================================================
validate_structure.py bir bulmaca çözümünün ALAN ADINI ve ETİKETİNİ arar.
Bu betik CEVABIN KENDİSİNİ arar. Aradaki fark, bu projedeki en büyük
gizlilik boşluğuydu:

    BOOK_STATS.md içine şu satırı yazın —
    "Kapı I kapanış kelimesi filanca, meta-misterin cevabı falanca" —
    ve alan adı taraması hiçbir şey görmez. Alan adı yoktur. Etiket yoktur.
    Yalnızca cevap vardır.

Kanarya bunu üç kipte kapatır:

  KİP A · YEREL (korumalı katman diskte)
    Bütün cevaplar okunur, normalize edilir ve TAKİP EDİLEN HER DOSYADA,
    HER DOSYA ADINDA ve SON COMMIT MESAJLARINDA aranır. En güçlü kip;
    yanlış pozitif üretmez çünkü gerçek cevabı arar.

  KİP B · CI (korumalı katman yok, tuzlu künye var)
    Korumalı katman CI'da YOKTUR — bu kasıtlıdır. Bu yüzden kanarya
    cevapları değil, TUZLU KARMALARINI taşır: her cevabın normalize
    edilmiş biçiminin karması künyeye yazılır, tuz bir CI sırrıdır.
    CI her dosyanın kelime ve karakter pencerelerini aynı tuzla karar ve
    künyede arar. Cevap hiçbir yerde açık durmaz ama sızıntı yakalanır.

  KİP C · KOŞMADI
    Ne korumalı katman ne tuz var. Kanarya KOŞMADIĞINI SÖYLER ve Faz 2'den
    itibaren KIRMIZI yanar. Sessizce yeşil yanan bir kanarya, kanarya
    değildir.

⚠ BU BETİK CEVAP YAZDIRMAZ. Bulguda yalnızca bulmaca kimliği ve dosya
adı geçer. Bir sızıntı raporunun kendisinin sızıntı olması, bu depoda
düşülebilecek en gülünç tuzaktır.

Ayrıca Faz 6 görevi: `08_OUTPUT/` yayın paketinde çözüm dosyası aranır.
Bir çözümün dağıtım paketine girmesi, depoya girmesinden DAHA KÖTÜDÜR —
çünkü doğrudan alıcıya ulaşır.

Kullanım:
    qa_solution_leak.py                      # denetle
    qa_solution_leak.py --emit-manifest      # künyeyi üret (yerelde, tuzla)

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("ENIGMATICA_ROOT", os.path.dirname(HERE))

SOLUTIONS_DIR = os.path.join(ROOT, "01_SOURCE", "solutions")
DESIGN_DIR = os.path.join(ROOT, "01_SOURCE", "design")
MANIFEST = os.path.join(ROOT, "06_REPORTS", "tracked", "canary-manifest.json")
OUTPUT_DIR = os.path.join(ROOT, "08_OUTPUT")

SALT_ENV = "ENIGMATICA_CANARY_SALT"
# Kanaryanın koşmadan geçmesine izin verilen kapı seviyeleri. Faz 2'den
# itibaren yazılmış bulmaca vardır, yani korunacak bir cevap vardır.
CANARY_OPTIONAL_GATES = ("phase0", "phase1")
VALID_GATES = ["phase0", "phase1", "phase2", "phase3", "phase4", "phase5",
               "release"]

# Cevap sayılacak alanlar. 3. kademe ipucu bilerek DAHİLDİR: "neredeyse-cevap"
# public bir dosyada durursa cevap durmuş sayılır.
ANSWER_FIELDS = ("finalAnswer", "intendedSolution")
MIN_ANSWER_CHARS = 6

BINARY_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff",
              ".pdf", ".zip", ".gz", ".bz2", ".xz", ".7z", ".ttf", ".otf",
              ".woff", ".woff2", ".eot", ".ico", ".mp3", ".mp4", ".mov",
              ".psd", ".ai", ".indd", ".pyc", ".so", ".dylib", ".dll")
MAX_SCAN_BYTES = 2_000_000
COMMIT_SCAN_DEPTH = 100

# Korumalı dizinler kanaryanın KAYNAĞIDIR, bulgusu değil: cevaplar oradan
# okunur, dolayısıyla orada bulunmaları tanım gereğidir. Bu dizinlerde
# TAKİP EDİLEN bir dosyanın varlığı zaten tek başına ihlaldir ve onu
# validate_structure § PROTECTED_DIRS yakalar. Burada tekrar raporlamak
# gerçek bulguyu gürültüye boğardı.
PROTECTED_PREFIXES = ("01_SOURCE/solutions/", "01_SOURCE/design/",
                      "09_ARCHIVE/solutions/", "06_REPORTS/solver/")

_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
# ⚠ _protected_layer.py § _TR_FOLD ile AYNI OLMAK ZORUNDA. Ayrışırlarsa
# kanarya ile ipucu kapısı farklı iki dizeye bakar ve ayrışan taraf
# sessizce körleşir. Gerekçenin tamamı orada yazılıdır: NFKD noktasız
# 'ı' ile noktalı 'İ'yi ÇÖZMEZ, dolayısıyla Türkçe bir cevap iki farklı
# normal biçime sahip olur.
_TR_FOLD = str.maketrans({"ı": "i", "İ": "i", "I": "i", "ﬁ": "fi"})


def norm(text: str) -> str:
    t = unicodedata.normalize("NFKD", (text or "").translate(_TR_FOLD))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return " ".join(_PUNCT.sub(" ", t.lower()).split())


def squeeze(text: str) -> str:
    return norm(text).replace(" ", "")


def h(salt: str, value: str) -> str:
    return hashlib.sha256((salt + "\0" + value).encode("utf-8")).hexdigest()[:24]


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

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


def read_gate() -> str:
    p = os.path.join(ROOT, ".gate")
    if not os.path.exists(p):
        return "phase0"
    with open(p, encoding="utf-8") as fh:
        return fh.read().strip()


def tracked_files() -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                             capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            return []
        return [p for p in out.stdout.split("\0") if p.strip()]
    except (OSError, subprocess.SubprocessError):
        return []


def commit_messages() -> list[str]:
    """Commit MESAJLARI da public'tir ve geri alınamaz.
    'g1-007 düzeltme: kapı kelimesi ...' biçiminde bir mesaj, dosya
    taramasının hiç bakmadığı kalıcı bir sızıntıdır."""
    try:
        out = subprocess.run(
            ["git", "log", "-%d" % COMMIT_SCAN_DEPTH, "--format=%B"],
            cwd=ROOT, capture_output=True, text=True, timeout=30)
        return out.stdout.splitlines() if out.returncode == 0 else []
    except (OSError, subprocess.SubprocessError):
        return []


def collect_answers() -> dict[str, list[str]]:
    """{puzzleId: [cevap dizeleri]} — YALNIZCA yerelde çalışır."""
    out: dict[str, list[str]] = {}
    for d in (SOLUTIONS_DIR, DESIGN_DIR):
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".json"):
                continue
            try:
                with open(os.path.join(d, name), encoding="utf-8") as fh:
                    data = json.load(fh)
            except (OSError, json.JSONDecodeError):
                continue
            records = data if isinstance(data, list) else data.get("puzzles", [data])
            for rec in records:
                if not isinstance(rec, dict) or not rec.get("puzzleId"):
                    continue
                vals = [str(rec.get(f, "")) for f in ANSWER_FIELDS]
                hints = rec.get("hints") or []
                if len(hints) == 3:
                    vals.append(str(hints[2]))
                vals = [v for v in vals if len(squeeze(v)) >= MIN_ANSWER_CHARS]
                if vals:
                    out.setdefault(rec["puzzleId"], []).extend(vals)
    return out


def scannable(rel: str) -> bool:
    if rel.lower().endswith(BINARY_EXT):
        return False
    p = os.path.join(ROOT, rel)
    try:
        return os.path.isfile(p) and os.path.getsize(p) <= MAX_SCAN_BYTES
    except OSError:
        return False


def read_text(rel: str) -> str:
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8",
                  errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def build_manifest(answers: dict[str, list[str]], salt: str) -> dict:
    """Tuzlu künye: cevaplar değil, karmaları. Tuz olmadan geri çevrilemez."""
    word_lens, char_lens = set(), set()
    digests: set[str] = set()
    for vals in answers.values():
        for v in vals:
            toks = norm(v).split()
            sq = squeeze(v)
            if len(toks) >= 1:
                word_lens.add(len(toks))
                digests.add(h(salt, " ".join(toks)))
            if len(sq) >= MIN_ANSWER_CHARS:
                char_lens.add(len(sq))
                digests.add(h(salt, sq))
                digests.add(h(salt, sq[::-1]))     # ters basım / ayna
    return {
        "$comment": [
            "⭑ TUZLU KANARYA KÜNYESİ ⭑",
            "Bu dosya CEVAP TAŞIMAZ; cevapların tuzlu karmalarını taşır.",
            "Tuz bir CI sırrıdır (ENIGMATICA_CANARY_SALT) ve depoda DURMAZ.",
            "Tuz olmadan bu karmalardan cevap türetilemez.",
            "Ters karmalar da vardır: ipuçları TERS BASILIR (HINT_LADDER § 3)",
            "ve ters basılacak bir dizeyi düz aramak onu kaçırır."
        ],
        "version": 1,
        "saltFingerprint": hashlib.sha256(salt.encode()).hexdigest()[:16],
        "wordWindowLengths": sorted(word_lens),
        "charWindowLengths": sorted(char_lens),
        "digests": sorted(digests),
        "answerCount": sum(len(v) for v in answers.values()),
    }


def scan_with_manifest(text: str, man: dict, salt: str) -> bool:
    toks = norm(text).split()
    for k in man.get("wordWindowLengths", []):
        if k <= 0 or k > len(toks):
            continue
        for i in range(len(toks) - k + 1):
            if h(salt, " ".join(toks[i:i + k])) in man["_set"]:
                return True
    sq = squeeze(text)
    for k in man.get("charWindowLengths", []):
        if k <= 0 or k > len(sq):
            continue
        for i in range(len(sq) - k + 1):
            if h(salt, sq[i:i + k]) in man["_set"]:
                return True
    return False


def scan_plain(text: str, answers: dict[str, list[str]]) -> list[str]:
    n, s = norm(text), squeeze(text)
    hit = []
    for pid, vals in answers.items():
        for v in vals:
            vn, vs = norm(v), squeeze(v)
            if len(vs) < MIN_ANSWER_CHARS:
                continue
            if vn in n or vs in s or vs[::-1] in s:
                hit.append(pid)
                break
    return hit


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    ap.add_argument("--emit-manifest", action="store_true",
                    help="tuzlu künyeyi üret (yerelde, korumalı katman varken)")
    args = ap.parse_args()

    gate_level = args.gate or read_gate()
    if gate_level not in VALID_GATES:
        print("HATA: geçersiz kapı seviyesi: %s" % gate_level, file=sys.stderr)
        return 2

    print("=" * 74)
    print("  ⭑ ÇÖZÜM KANARYASI ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = Report(args.verbose)
    salt = os.environ.get(SALT_ENV, "")
    answers = collect_answers()
    files = [f for f in tracked_files()
             if scannable(f) and not f.startswith(PROTECTED_PREFIXES)]
    all_paths = tracked_files()

    rep.facts["trackedScanned"] = len(files)
    rep.facts["answersLoaded"] = sum(len(v) for v in answers.values())

    if args.emit_manifest:
        print("\n── künye üretimi ──")
        if not answers:
            print("  ⊘ korumalı katman boş — üretilecek künye yok")
            return 0
        if not salt:
            print("  ⛔ %s kurulu değil — tuzsuz künye üretilmez" % SALT_ENV,
                  file=sys.stderr)
            return 2
        man = build_manifest(answers, salt)
        os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
        with open(MANIFEST, "w", encoding="utf-8") as fh:
            json.dump(man, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("  ✅ %d cevaptan %d karma üretildi → %s"
              % (man["answerCount"], len(man["digests"]),
                 os.path.relpath(MANIFEST, ROOT)))
        return 0

    # ── kip seçimi ──────────────────────────────────────────────────────
    man = None
    if os.path.exists(MANIFEST):
        try:
            with open(MANIFEST, encoding="utf-8") as fh:
                man = json.load(fh)
            man["_set"] = set(man.get("digests", []))
        except (OSError, json.JSONDecodeError):
            man = None

    if answers:
        mode = "A"
    elif man and salt:
        mode = "B"
    else:
        mode = "C"
    rep.facts["mode"] = mode

    print("\n── kip ──")
    if mode == "A":
        print("  KİP A · YEREL — %d bulmacadan %d cevap dizesi yüklendi"
              % (len(answers), rep.facts["answersLoaded"]))
    elif mode == "B":
        print("  KİP B · CI — tuzlu künye (%d karma) ile taranıyor"
              % len(man["_set"]))
        if man.get("saltFingerprint") != hashlib.sha256(
                salt.encode()).hexdigest()[:16]:
            rep.check(False, "künye tuzu ile ortam tuzu UYUŞUYOR")
            return 1
    else:
        print("  KİP C · KOŞMADI — ne korumalı katman ne tuz var")
        if gate_level in CANARY_OPTIONAL_GATES:
            rep.warn("kanarya koşmadı (kapı %s'te bu kabul edilir: henüz "
                     "korunacak cevap yok)" % gate_level)
            print("\n" + "=" * 74)
            print("  ⊘ kanarya BOŞ KOŞTU — bu bir GEÇİŞ DEĞİLDİR")
            print("=" * 74)
            if args.json:
                os.makedirs(os.path.dirname(args.json), exist_ok=True)
                with open(args.json, "w", encoding="utf-8") as fh:
                    json.dump({"status": "not-run", "gate": gate_level,
                               "checks": 0, "errors": [],
                               "warnings": rep.warnings, "facts": rep.facts},
                              fh, ensure_ascii=False, indent=2)
            return 0
        rep.check(False, "⛔ kanarya KOŞMADI ama kapı %s — yazılmış bulmaca "
                         "varken kanarya zorunludur (tuz: %s)"
                  % (gate_level, SALT_ENV))
        return 1

    # ── tarama ──────────────────────────────────────────────────────────
    print("\n── takip edilen dosyalar ──")
    leaked_files: list[str] = []
    for rel in files:
        body = read_text(rel)
        if mode == "A":
            if scan_plain(body, answers):
                leaked_files.append(rel)
        elif scan_with_manifest(body, man, salt):
            leaked_files.append(rel)
    rep.check(not leaked_files,
              "⭑ hiçbir takip edilen dosya bir CEVAP taşımıyor ⭑"
              + ("" if not leaked_files else " — ⛔ SIZINTI: %s" % leaked_files[:5]))

    print("\n── dosya adları ──")
    path_blob = "\n".join(p for p in all_paths
                          if not p.startswith(PROTECTED_PREFIXES))
    if mode == "A":
        hit = scan_plain(path_blob, answers)
    else:
        hit = ["künye eşleşmesi"] if scan_with_manifest(path_blob, man, salt) else []
    rep.check(not hit, "hiçbir DOSYA ADI bir cevap taşımıyor"
              + ("" if not hit else " — ⛔ SIZINTI: %d bulmaca" % len(hit)))

    print("\n── commit mesajları ──")
    msgs = "\n".join(commit_messages())
    if msgs:
        if mode == "A":
            hit = scan_plain(msgs, answers)
        else:
            hit = ["künye eşleşmesi"] if scan_with_manifest(msgs, man, salt) else []
        rep.check(not hit,
                  "son %d commit mesajı temiz" % COMMIT_SCAN_DEPTH
                  + ("" if not hit else " — ⛔ GERİ ALINAMAZ SIZINTI: %d bulmaca"
                     % len(hit)))
    else:
        rep.warn("commit geçmişi okunamadı — mesaj taraması boş koştu")

    print("\n── yayın paketi (08_OUTPUT) ──")
    out_hits: list[str] = []
    if os.path.isdir(OUTPUT_DIR):
        for base, _dirs, names in os.walk(OUTPUT_DIR):
            for n in names:
                p = os.path.join(base, n)
                rel = os.path.relpath(p, ROOT)
                if not scannable(rel):
                    continue
                body = read_text(rel)
                if (scan_plain(body, answers) if mode == "A"
                        else scan_with_manifest(body, man, salt)):
                    out_hits.append(rel)
    rep.check(not out_hits,
              "yayın paketinde çözüm YOK"
              + ("" if not out_hits else " — ⛔ ALICIYA ULAŞIR: %s" % out_hits[:5]))

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · kip %s · %d dosya tarandı"
              % (rep.checks, mode, len(files)))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "gate": gate_level,
                       "checks": rep.checks, "errors": rep.errors,
                       "warnings": rep.warnings, "facts": rep.facts},
                      fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
