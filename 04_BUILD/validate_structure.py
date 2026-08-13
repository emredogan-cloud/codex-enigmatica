#!/usr/bin/env python3
"""
DEPO, BELGE VE ÇÖZÜM KORUMASI — Codex Enigmatica
================================================================================
Altı ayrı denetim. Beşincisi bu projenin VAROLUŞSAL kapısıdır:

  ① ZORUNLU DOSYALAR       — yol haritasının söz verdiği belgeler var mı
  ② GÖMÜLÜ SABİT DEĞER     — yazar/yayıncı adı bir betiğe gömülmüş mü
  ③ MANUSCRIPT SIZINTISI   — bulmaca prozası takip edilen bir dosyaya sızmış mı
  ④ SIR SIZINTISI          — .env veya anahtar benzeri dize depoya girmiş mi
  ⑤ ⭑ ÇÖZÜM SIZINTISI ⭑    — bir bulmaca çözümü public depoya girmiş mi
  ⑥ SÖZLEŞME SENKRONU      — kapı sabitleri config ile aynı şeyi mi söylüyor

⑤ NEDEN VAROLUŞSAL: bir bulmaca kitabının ÇÖZÜMLERİ ürünün kendisidir.
Public depoda duran bir çözüm, kitabı YAYIMLANMADAN değersizleştirir. Ve
bu hata geri alınamaz: git geçmişine giren bir çözümü silmek, geçmişi
yeniden yazmak demektir.

Ama dikkat: KOD SIR DEĞİLDİR. Bir doğrulayıcının kendisi public kalır ve
kalmalıdır. Sır olan yalnızca ÇÖZÜMDÜR.

────────────────────────────────────────────────────────────────────────
FAZ 1 KIRMIZI TAKIM DÜZELTMELERİ — bu kapı bir denetimden geçti ve
aşağıdaki delikler KANITLANARAK kapatıldı. Her biri bir POC ile
gösterildi; her birinin bir selftest fikstürü vardır.

  · KAPALI BAŞARISIZLIK — `git ls-files` çalışmazsa liste boş dönüyor ve
    bütün sızıntı denetimleri BOŞ KOŞUP YEŞİL YANIYORDU. Artık .git varken
    boş liste bir HATADIR. (Bu, bütün kapının ana şalteriydi.)
  · UZANTI SÜZGECİ — tarama yalnızca beş uzantıya bakıyordu ve
    `str.endswith` BÜYÜK/KÜÇÜK HARFE DUYARLIYDI: `ANSWERS.JSON` geçiyordu.
    Artık takip edilen HER metin dosyası taranır; yalnızca ikili biçimler
    ve dev dosyalar dışlanır.
  · TEMEL AD MUAFİYETİ — `README.md` ve `.gitkeep` ADI taşıyan her dosya,
    HER DERİNLİKTE muaftı: `01_SOURCE/solutions/gate-1/README.md` bir
    çözüm anahtarı taşıyabiliyordu. Artık muafiyet TAM YOLDUR ve muaf
    dosyalar yine de içerik taramasından GEÇER.
  · TÜRKÇE KÖRLÜĞÜ — kalıplar yalnızca İngilizce JSON alan adlarıydı;
    belgelerin dili Türkçe. `Kapı I kapanış kelimesi: ...` hiçbir şeye
    takılmıyordu. Artık değer tarafı da, iki dilde de aranır.
  · DEĞER TARAFI — bu betik alan ADI arar, CEVAP aramaz. O iş
    `qa_solution_leak.py` kanaryasınındır ve bu betiğin sınırı burada
    açıkça yazılıdır. Bir kapının ne YAPMADIĞINI bilmemek, onu olduğundan
    güçlü sanmaktır.

② NEDEN VAR: World Myths Faz 6'da yazar adı ÜÇ betikte ayrı ayrı gömülüydü
ve aynı kitabın KAPAĞI ile METADATASI farklı yazar taşıyordu. Tek doğruluk
kaynağı project_config.json'dur ve bu kapı onu korur.

③ NEDEN VAR: .gitignore YOL kalıplarıyla çalışır ve yeni bir ada konan
dosyayı YAKALAMAZ. Politikayı disipline değil MEKANİZMAYA bağlarız.

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
    "00_CONTEXT/PUZZLE_TAXONOMY.md",
    "00_CONTEXT/SOLVER_TEST_PROTOCOL.md",
    "00_CONTEXT/INTERNAL_SOLVER_PROTOCOL.md",
    "00_CONTEXT/RED_TEAM_CHECKLIST.md",
    "00_CONTEXT/SOURCING_STANDARD.md",
    "00_CONTEXT/VISUAL_ARCHITECTURE.md",
    "00_CONTEXT/VALIDATION_REFERENCE.md",
    "01_SOURCE/puzzle.schema.json",
    "01_SOURCE/gate_index.json",
    "01_SOURCE/mechanism_families.json",
    "01_SOURCE/puzzle_index.json",
    "01_SOURCE/research/sources.json",
    "04_BUILD/qa_all.sh",
    "04_BUILD/validate_spec.py",
    "04_BUILD/qa_dependency.py",
    "04_BUILD/qa_taxonomy.py",
    "04_BUILD/qa_solution_leak.py",
    "05_TESTS/selftest.py",
    ".github/workflows/validate.yml",
]

REQUIRED_DIRS = [
    "00_CONTEXT", "01_SOURCE", "02_MANUSCRIPT", "03_COVER", "04_BUILD",
    "05_TESTS", "06_REPORTS", "07_ASSETS", "08_OUTPUT", "09_ARCHIVE",
    "01_SOURCE/puzzles", "01_SOURCE/research", "01_SOURCE/design",
    "01_SOURCE/solutions", "05_TESTS/puzzle", "06_REPORTS/tracked",
    "06_REPORTS/solver", "07_ASSETS/raw", "07_ASSETS/processed",
    "07_ASSETS/plates", "09_ARCHIVE/solutions",
]

# ── tarama evreni ─────────────────────────────────────────────────────────
# İZİN LİSTESİ DEĞİL, YASAK LİSTESİ: takip edilen her dosya taranır,
# yalnızca metin OLMAYANLAR dışlanır. Ters kurgu (yalnızca beş uzantıyı
# taramak) `ANSWERS.JSON`, `leak.yml`, `ANSWERKEY` gibi dosyaları
# görmüyordu ve uzantı testi büyük/küçük harfe duyarlıydı.
BINARY_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff",
              ".pdf", ".zip", ".gz", ".bz2", ".xz", ".7z", ".ttf", ".otf",
              ".woff", ".woff2", ".eot", ".ico", ".mp3", ".mp4", ".mov",
              ".psd", ".ai", ".indd", ".pyc", ".so", ".dylib", ".dll")
MAX_SCAN_BYTES = 2_000_000

# ⚠ İKİ AYRI TARAMA EVRENİ — ve ayrım bir KATEGORİ ayrımıdır.
#
# ALAN ADI ve PROZA kalıpları VERİ biçimlerini hedefler: `"hints":` bir JSON
# anahtarıdır. Aynı kalıbı Python kaynağında aramak bir kategori hatasıdır —
# `counts = {"hints": 0}` bir sayaçtır, bir çözüm değil. Kendi
# doğrulayıcılarımız bu alan adlarını TANIMLAMAK zorundadır; onları kendi
# kapılarında yakalamak, kapıyı gürültüye boğar ve gürültülü kapı kapatılır.
#
# DEĞER TARAFI ve SIR kalıpları ise HER metin dosyasını gezer: bir cevabın
# hangi uzantıda durduğu önemsizdir.
#
# Kaynak kodda gizlenmiş bir DEĞER bu ayrımdan kaçabilir; onu qa_solution_leak
# kanaryası yakalar. Sınır RED_TEAM_CHECKLIST § 4'te yazılıdır.
DATA_DOC_EXT = (".json", ".jsonl", ".md", ".mdx", ".txt", ".csv", ".tsv",
                ".html", ".xml", ".svg", ".yml", ".yaml", ".tex", ".rst")

# ② Gömülü sabit değer taraması ------------------------------------------------
# Bu dizeler YALNIZCA project_config.json içinde geçebilir.
SINGLE_SOURCE_VALUES = ["Emre Doğan", "Vâliçe Press"]
# ⚠ KAPSAM BİLEREK KOD VE VERİDİR, PROZA DEĞİL.
# Bu kapının derdi "yazar adı hiçbir yerde geçmesin" değil; derdi bir
# ÜRETİCİNİN değeri kendi içine gömmesidir — kapak betiği ile metadata
# betiğinin farklı yazar basması böyle oldu (D1). Bir belgenin yayıncıdan
# söz etmesi bir sürüklenme riski değildir; metadata.py'nin adı sabit
# yazması ise tam olarak odur. Uzantı listesi bu ayrımı çizer.
SCAN_EMBED_EXT = (".py", ".sh", ".yml", ".yaml", ".json", ".toml",
                  ".cfg", ".ini", ".csv")
EMBED_SCAN_SKIP = {
    "project_config.json",
    "04_BUILD/validate_structure.py",   # tarayıcının kendisi dizeleri taşır
    "06_REPORTS/tracked/PHASE_1_REPORT.md",
}

# ③ Manuscript sızıntısı -------------------------------------------------------
# Kural prozasının parmak izleri.
LEAK_MARKERS = [
    r"\bWhat you seek\b",
    r"\bThe plate conceals\b",
    r"\bTurn to the leaf\b",
]
LEAK_MIN_HITS = 2
# ⚠ TEK BAŞINA YETEN KALIP: bir bulmaca BAŞLIĞI public dosyada görülmemelidir.
# Başlık bu kitapta bir yönlendirmedir (puzzle.schema § title → PROTECTED),
# dolayısıyla iki-vuruş eşiğini beklemez.
LEAK_MARKERS_SOLO = [
    r"\bEnigma\s+[IVXLC]+\s*[:.]",
]
LEAK_SCAN_SKIP = {
    "00_CONTEXT/STYLE.md",
}

# ⑤ ⭑ ÇÖZÜM SIZINTISI ⭑ — bu projenin varoluşsal kapısı ---------------------
# (a) ALAN ADI kalıpları — yapısal sızıntı.
# Kalıplar ADLARDAN TÜRETİLİR: elle yazılan bir regex ile config'deki ad
# listesi ayrışabilir ve ayrışan taraf sessizce korumasız kalır.
SOLUTION_FIELD_NAMES = ["solution", "intendedSolution", "answer", "answerKey",
                        "solutionPath", "hints", "finalAnswer"]
SOLUTION_FIELD_MARKERS = [r'"%s"\s*:' % re.escape(n)
                          for n in SOLUTION_FIELD_NAMES]
# (b) DEĞER TARAFI kalıpları — proza sızıntısı, İKİ DİLDE.
# Yalnızca "etiket + cevap gibi görünen dize" biçimini arar: büyük harfli,
# en az altı karakterlik bir dize. Böylece "Karar: proje durur" gibi normal
# Türkçe cümleler yakalanmaz ama 'CEVAP' etiketinin ardından gelen büyük harfli bir dize yakalanır.
ANSWER_SHAPE = r'\s*[:=]\s*["\'“‘]?[A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ \-]{5,}'
SOLUTION_VALUE_MARKERS = [
    (r'\b(?:SOLUTION|ANSWER|ANSWER\s+KEY|HINT)' + ANSWER_SHAPE, "İngilizce etiketli cevap"),
    (r'\b(?:ÇÖZÜM|CEVAP|İPUCU|ANAHTAR\s+KELİME)' + ANSWER_SHAPE, "Türkçe etiketli cevap"),
]
# 'ANSWER KEY' bir BAŞLIKTIR, bir değer değil — bu yüzden değer hattında
# değil ALAN hattındadır ve muafiyet listesi ona uygulanır. Değer hattına
# konulduğunda, kalıpları AÇIKLAYAN belgeyi kendi kalıbıyla vuruyordu.
SOLUTION_FIELD_MARKERS.append(r"\bANSWER KEY\b")
SOLUTION_MIN_HITS = 1
# ⚠ MUAFİYET LİSTESİ DONDURULMUŞTUR ve selftest TAM KÜME EŞİTLİĞİ arar.
# Gerekçe: eski selftest "muafiyet gerekli mi" diye sorup dosyada bir çözüm
# işareti ARIYORDU — yani yeni bir muafiyeti meşrulaştırmanın yolu, dosyaya
# bir çözüm işareti koymaktı. Test saldırganın kontrol listesiydi.
#
# Bu muafiyet YALNIZCA (a) ALAN ADI taramasını kapsar. (b) DEĞER TARAFI ve
# qa_solution_leak kanaryası HİÇBİR dosyayı muaf tutmaz — yani bu iki dosyaya
# gerçek bir cevap yazmak yine yakalanır.
SOLUTION_SCAN_SKIP = frozenset({
    "01_SOURCE/puzzle.schema.json",
    "00_CONTEXT/CONTENT_PROTECTION.md",
})
# Bu dizinler ASLA takip edilemez. Bir dosyanın burada VE git'te olması
# tek başına ihlaldir. project_config § contentProtection.protectedDirs
# ile SENKRON olmak zorundadır (⑥).
PROTECTED_DIRS = ("01_SOURCE/solutions/", "01_SOURCE/design/",
                  "01_SOURCE/playtests/", "09_ARCHIVE/solutions/",
                  "06_REPORTS/solver/")
# ⚠ TAM YOL muafiyeti. Eski kurgu TEMEL ADA bakıyordu, yani her alt dizin
# bedava bir serbest dosya kazanıyordu: `01_SOURCE/solutions/gate-1/README.md`.
PROTECTED_DIR_ALLOW = frozenset({
    "01_SOURCE/playtests/.gitkeep",
    "01_SOURCE/solutions/.gitkeep",
    "01_SOURCE/solutions/README.md",
    "01_SOURCE/design/.gitkeep",
    "09_ARCHIVE/solutions/.gitkeep",
    "06_REPORTS/solver/.gitkeep",
})
MANUSCRIPT_ALLOW = frozenset({
    "02_MANUSCRIPT/.gitkeep",
    "02_MANUSCRIPT/README.md",
})

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


def tracked_files(rep: Report) -> list[str]:
    """git ls-files — TAKİP EDİLEN dosyalar.

    ⚠ KAPALI BAŞARISIZLIK. Eskiden buradaki her hata boş liste döndürüyor
    ve main() onu bir UYARIYA çeviriyordu — yani `git` bulunamadığında,
    depo bozukken veya `.git` taşındığında bütün sızıntı denetimleri boş
    koşup YEŞİL yanıyordu. Depoda çözüm dosyaları dururken bile.

    Artık: `.git` varsa liste boş OLAMAZ."""
    has_git = os.path.isdir(os.path.join(ROOT, ".git"))
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                             capture_output=True, text=True, timeout=30)
        files = [p for p in out.stdout.split("\0") if p.strip()] \
            if out.returncode == 0 else []
    except (OSError, subprocess.SubprocessError):
        files = []

    if has_git:
        rep.check(len(files) >= 20,
                  "git takip listesi okundu (%d dosya) — sızıntı denetimleri "
                  "GERÇEKTEN koşuyor" % len(files))
    elif not files:
        rep.warn("depo yok ve takip listesi boş — sızıntı denetimleri boş koşuyor")
    return files


def scannable(rel: str) -> bool:
    """Metin olarak taranabilir mi. Uzantı testi KÜÇÜK HARFE ÇEVRİLİR:
    `ANSWERS.JSON` ile `answers.json` aynı dosyadır."""
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


def check_files(rep: Report, files: list[str]) -> None:
    """⚠ İKİ AYRI SORU — ve ikincisi bir CI kırmızısıyla öğrenildi.

    ① dizin DİSKTE var mı
    ② dizin KLONDA var mı — yani içinde TAKİP EDİLEN bir dosya var mı

    git boş dizin saklamaz. `.gitkeep` dosyaları `.gitignore` tarafından
    gölgelenirse dizin yerelde VARDIR ama klonda YOKTUR: yerelde yeşil,
    CI'da kırmızı. Depo sınırı denetimi bağlar için bu ayrışmayı zaten
    kapatıyordu; bu denetim onu DİZİNLER için kapatır."""
    print("\n── zorunlu dosya ve dizinler ──")
    tracked_dirs = {os.path.dirname(f) for f in files}
    for rel in REQUIRED_DIRS:
        rep.check(os.path.isdir(os.path.join(ROOT, rel)), "dizin: %s" % rel)
        if files:
            rep.check(any(d == rel or d.startswith(rel + "/")
                          for d in tracked_dirs),
                      "dizin KLONDA da var (takip edilen dosya taşıyor): %s" % rel)
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
        if rel in EMBED_SCAN_SKIP or not scannable(rel):
            continue
        if not rel.lower().endswith(SCAN_EMBED_EXT):
            continue
        body = read_text(rel)
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
        if rel.startswith("02_MANUSCRIPT/") and rel not in MANUSCRIPT_ALLOW:
            leaked.append("%s (manuscript dizini takip ediliyor)" % rel)
            continue
        if rel in LEAK_SCAN_SKIP or not scannable(rel):
            continue
        if not rel.lower().endswith(DATA_DOC_EXT):
            continue
        body = read_text(rel)
        # ⚠ Muaf dosyalar bile TEK BAŞINA YETEN kalıplardan muaf değildir.
        solo = [p for p in LEAK_MARKERS_SOLO if re.search(p, body)]
        if solo:
            leaked.append("%s (bulmaca BAŞLIĞI)" % rel)
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
    isbn_hits: list[str] = []
    cfgp = os.path.join(ROOT, "project_config.json")
    strategy = "kdp-free"
    if os.path.exists(cfgp):
        try:
            with open(cfgp, encoding="utf-8") as fh:
                strategy = json.load(fh).get("founder", {}).get(
                    "isbn", {}).get("strategy", "kdp-free")
        except (OSError, json.JSONDecodeError):
            pass

    for rel in files:
        if not scannable(rel):
            continue
        body = read_text(rel)
        for pat, name in SECRET_PATTERNS:
            if re.search(pat, body):
                found.append("%s → %s" % (rel, name))
        if strategy == "kdp-free" and rel != "04_BUILD/validate_structure.py":
            if FAKE_ISBN.search(body):
                isbn_hits.append(rel)

    rep.check(not found,
              "sır benzeri dize yok" + ("" if not found else " — %s" % found[:3]))
    rep.check(not isbn_hits,
              "uydurulmuş ISBN yok (strateji: %s)" % strategy +
              ("" if not isbn_hits else " — %s" % isbn_hits[:3]))


def check_solution_leak(rep: Report, files: list[str]) -> None:
    """⑤ ⭑ Bir bulmaca çözümü public depoya girmiş mi. ⭑

    Üç ayrı hat:
      (a) KORUMALI DİZİN — bu dizinlerdeki takip edilen her dosya tek
          başına ihlaldir; içeriğe bakılmaz. Muafiyet TAM YOLDUR.
      (b) ALAN ADI TARAMASI — yapısal sızıntı; iki dosya muaftır.
      (c) DEĞER TARAFI TARAMASI — etiketli cevap dizeleri; MUAFİYET YOKTUR.

    ⚠ BU KAPININ SINIRI: alan adı ve etiket arar, CEVABIN KENDİSİNİ aramaz.
    Etiketsiz düz proza içindeki bir cevabı yakalayamaz. O iş
    qa_solution_leak.py kanaryasınındır ve bu sınırın yazılı olması,
    kapının olduğundan güçlü sanılmasını engeller."""
    print("\n── ⭑ ÇÖZÜM SIZINTISI ⭑ ──")

    in_protected = [f for f in files if f.startswith(PROTECTED_DIRS)
                    and f not in PROTECTED_DIR_ALLOW]
    rep.check(not in_protected,
              "korumalı dizinlerde takip edilen dosya yok" +
              ("" if not in_protected else " — İHLAL: %s" % in_protected[:5]))

    by_field: list[str] = []
    by_value: list[str] = []
    for rel in files:
        if not scannable(rel):
            continue
        body = read_text(rel)
        if rel not in SOLUTION_SCAN_SKIP and rel.lower().endswith(DATA_DOC_EXT):
            hits = sum(1 for pat in SOLUTION_FIELD_MARKERS if re.search(pat, body))
            if hits >= SOLUTION_MIN_HITS:
                by_field.append("%s (%d alan işareti)" % (rel, hits))
        # (c) muafiyetsiz
        for pat, name in SOLUTION_VALUE_MARKERS:
            if re.search(pat, body):
                by_value.append("%s (%s)" % (rel, name))
                break

    rep.check(not by_field,
              "çözüm ALANI public depoda YOK" +
              ("" if not by_field else " — ⛔ SIZINTI: %s" % by_field[:5]))
    rep.check(not by_value,
              "etiketli CEVAP dizesi public depoda YOK (muafiyetsiz tarama)" +
              ("" if not by_value else " — ⛔ SIZINTI: %s" % by_value[:5]))


def check_contract_sync(rep: Report) -> None:
    """⑥ Kapı sabitleri ile config aynı şeyi mi söylüyor.

    NEDEN: iki yerde yazılmış bir liste, er geç iki farklı liste olur — ve
    ayrışan taraf SESSİZCE korumasız kalır. `PROTECTED_DIRS`'e yazılan bir
    yazım hatası ('solvers/' yerine 'solver/') hiçbir yerde fark edilmezdi
    ve o dizin tamamen açılırdı."""
    print("\n── sözleşme senkronu ──")
    cfgp = os.path.join(ROOT, "project_config.json")
    try:
        with open(cfgp, encoding="utf-8") as fh:
            cp = json.load(fh).get("contentProtection", {})
    except (OSError, json.JSONDecodeError):
        rep.check(False, "project_config.json okunabiliyor")
        return

    rep.check(set(cp.get("solutionFieldNames", [])) == set(SOLUTION_FIELD_NAMES),
              "çözüm alan adları config ↔ tarayıcı SENKRON")
    rep.check(tuple(cp.get("protectedDirs", [])) == PROTECTED_DIRS,
              "korumalı dizin listesi config ↔ tarayıcı SENKRON")

    # Korumalı dizinler GERÇEKTEN var mı ve .gitignore onları KAPSIYOR mu.
    for d in PROTECTED_DIRS:
        rep.check(os.path.isdir(os.path.join(ROOT, d)),
                  "korumalı dizin diskte var: %s" % d)
    probe_ok = True
    for d in PROTECTED_DIRS:
        probe = os.path.join(d, "leak-probe.json")
        try:
            r = subprocess.run(["git", "check-ignore", "-q", probe],
                               cwd=ROOT, capture_output=True, timeout=15)
            if r.returncode != 0:
                probe_ok = False
                rep.warn(".gitignore korumalı dizini kapsamıyor: %s" % d)
        except (OSError, subprocess.SubprocessError):
            probe_ok = None
            break
    if probe_ok is not None:
        rep.check(probe_ok, ".gitignore bütün korumalı dizinleri kapsıyor")


def check_doc_links(rep: Report) -> None:
    """Belge bağları — iki ayrı denetim.

    ① KIRIK BAĞ      — hedef dosya var mı
    ② DEPO SINIRI    — bağ deponun DIŞINA çıkıyor mu

    ② NEDEN AYRI: `../PAZAR-RAPORU.html` kurucunun çalışma dizininde VARDIR
    ama depoyu klonlayan kimsede YOKTUR — yani yerelde yeşil, CI'da kırmızı.
    Depo sınırı denetimi bu ayrışmayı ortadan kaldırır."""
    print("\n── belge bağları ──")
    broken: list[str] = []
    escaped: list[str] = []
    root_abs = os.path.realpath(ROOT)

    scan = list(REQUIRED_FILES)
    for extra in ("02_MANUSCRIPT/README.md", "01_SOURCE/solutions/README.md",
                  "06_REPORTS/tracked/PHASE_1_REPORT.md"):
        if os.path.isfile(os.path.join(ROOT, extra)):
            scan.append(extra)

    for rel in scan:
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
            resolved = os.path.realpath(os.path.join(base, target))
            if not (resolved == root_abs or resolved.startswith(root_abs + os.sep)):
                escaped.append("%s → %s" % (rel, target))
                continue
            if not os.path.exists(resolved):
                broken.append("%s → %s" % (rel, target))

    rep.check(not escaped,
              "hiçbir bağ deponun dışına çıkmıyor" +
              ("" if not escaped else
               " — SINIR İHLALİ (künyeye çevirin): %s" % escaped[:5]))
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
    print("  DEPO, BELGE VE ÇÖZÜM KORUMASI")
    print("=" * 74)

    rep = Report(args.verbose)
    files = tracked_files(rep)

    check_files(rep, files)
    check_gate_file(rep)
    check_embedded(rep, files)
    check_manuscript_leak(rep, files)
    check_secrets(rep, files)
    check_solution_leak(rep, files)
    check_contract_sync(rep)
    check_doc_links(rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
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
