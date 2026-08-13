#!/usr/bin/env python3
"""
KAPILARIN KENDİ TESTİ — bu hattın EN ÖNEMLİ testi
================================================================================
Metin yokken yeşil kalan bir hat, KUSUR GELDİĞİNDE DE YEŞİL KALABİLİR.

Bu test o riski kapatır: her kapı için TAM BİR KUSUR taşıyan kurgu bir veri
seti çalıştırılır ve kapının o kusuru YAKALADIĞI kanıtlanır.

Bu projede kritiklik iki katına çıkar, çünkü iki kapı VAROLUŞSALDIR:

  · ÇÖZÜM SIZINTISI  — bir çözüm public depoya girerse ürün yayımlanmadan
                       değersizleşir ve hata GERİ ALINAMAZ (git geçmişi)
  · ÇÖZÜLEBİLİRLİK   — sözleşmenin gevşetilmesi, bozuk bir bulmaca
                       sisteminin sessizce kabul edilmesi demektir

Bir kapının "var olması" yetmez. Kusuru YAKALADIĞI kanıtlanmalıdır.

────────────────────────────────────────────────────────────────────────
⚠ FAZ 1'DE BULUNAN KÖRLÜK — bu dosyanın kendi kusuruydu.

Bu test, `validate_structure.py`'nin BEŞ denetiminden HİÇBİRİNİ
koşturmuyordu. Betiğin yolu bir sabite bağlanmış ve hiç çağrılmamıştı;
bütün fikstürler yalnızca `validate_spec.py`'yi hedefliyordu. Yani deponun
en çok süslenen kapısı — ÇÖZÜM SIZINTISI — ısırdığını hiç kanıtlamamıştı.

İkinci körlük daha kötüydü: § ④ bir muafiyetin "gerekli" olduğunu, muaf
dosyada bir çözüm işareti ARAYARAK doğruluyordu. Yani yeni bir muafiyeti
meşrulaştırmanın yolu, o dosyaya bir çözüm işareti koymaktı. Test,
saldırganın kontrol listesiydi.

Artık yedi bölüm var ve üçü Faz 1'de doğdu:

  ①  temiz kurgu BÜTÜN kapılardan geçer            (yanlış pozitif yok)
  ②  her kusurlu kurgu İLGİLİ kapıda yakalanır     (şema ve kapsam)
  ③  kapı seviyeleri gerçekten kilitliyor
  ④  muafiyet listeleri DONDURULMUŞ ve canlı
  ⑤  ⭑ DEPO KAPISI — gerçek bir git deposunda sızıntı fikstürleri ⭑
  ⑥  ⭑ KANARYA — cevabın kendisi dosyaya, ada, commit mesajına konur ⭑
  ⑦  ⭑ KORUMALI KATMAN — bozuk çözüm, ipucu ve tekillik kayıtları ⭑

Çıkış kodları:  0 = geçti   1 = KÖRLÜK BULUNDU
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "04_BUILD")

VALIDATE_SPEC = os.path.join(BUILD, "validate_spec.py")
VALIDATE_STRUCTURE = os.path.join(BUILD, "validate_structure.py")
CONFIG = os.path.join(ROOT, "project_config.json")
SCHEMA = os.path.join(ROOT, "01_SOURCE", "puzzle.schema.json")
GATE_INDEX = os.path.join(ROOT, "01_SOURCE", "gate_index.json")

# ⚠ Kurgu cevaplar ÜRETİLİR, yazılmaz. Bu dosya public'tir ve içine elle
# yazılmış "gerçekçi" bir cevap dizesi, depoyu okuyan biri için bir
# cevaptan ayırt edilemez.
FIXTURE_WORDS = ["ALPHA", "BRAVO", "CHARLIE", "DELTA", "ECHO", "FOXTROT"]


def fixture_answer(i: int) -> str:
    return "FIXTURE %s %s" % (FIXTURE_WORDS[i % len(FIXTURE_WORDS)],
                              FIXTURE_WORDS[(i + 2) % len(FIXTURE_WORDS)])


# ---------------------------------------------------------------------------
# Kurgu üreteci — GERÇEK envanterden bağımsız, tam kontrollü veri
# ---------------------------------------------------------------------------
def clean_config() -> dict:
    with open(CONFIG, encoding="utf-8") as fh:
        return json.load(fh)


def clean_gate_index() -> dict:
    with open(GATE_INDEX, encoding="utf-8") as fh:
        return json.load(fh)


def clean_games(cfg: dict, n: int = 140, status: str = "candidate") -> dict:
    """Şemaya uyan, kusursuz kurgu envanter — PUBLIC KATMAN.

    ⚠ Kurgu kayıtlar ÇÖZÜM ALANI TAŞIMAZ. Taşısalardı temiz kurgu bile
    çözüm sızıntısı kapısında takılırdı."""
    gates_ = [g["id"] for g in cfg["scope"]["gateStructure"]]
    fams = ["plate-observation", "substitution-cipher", "constraint-logic",
            "script-decoding", "transposition-cipher"]
    types = ["observation", "cipher", "logic", "cipher", "cipher"]
    fmts = ["word", "word", "word", "word", "word"]
    puzzles = []
    for i in range(n):
        rec = {
            "puzzleId": "fixture-%03d" % i,
            "gate": gates_[i % len(gates_)],
            "type": types[i % len(fams)],
            "mechanismFamily": fams[i % len(fams)],
            "status": status,
            "testStatus": "untested",
            "leakClass": "protected",
            "difficulty": 1,
            "ambiguityScore": 1,
            "answerFormat": fmts[i % len(fams)],
            "dependencies": [],
        }
        if status in ("validated", "written"):
            # Kazanılmış bir 'tested' kaydı: temiz kurgu geçmeli.
            rec["testStatus"] = "tested"
            rec["solverTestCount"] = 5
            rec["solverSolvedCount"] = 4
            rec["alternativeSolutionAnalysisDone"] = True
            rec["confirmedAlternativeSolutions"] = 0
        puzzles.append(rec)
    return {"puzzles": puzzles}


def confirmed_solver_config(cfg: dict) -> dict:
    """'tested' iddiası için kurucu onayı gerekir; kapsam fikstürlerinde
    o kilidi açık tutarız, § ② onu ayrıca test eder."""
    c = copy.deepcopy(cfg)
    c["founder"]["externalSolvers"]["founderConfirmed"] = True
    return c


_RUN_SEQ = [0]


def fake_root(tmp: str) -> str:
    """HER KOŞU KENDİ KÖKÜNÜ ALIR.

    Tek bir kök paylaşılırsa önceki testin yazdığı envanter sonraki testte
    HÂLÂ ORADA olur ve "envantersiz phase1 kırmızı yanmalı" testi sessizce
    anlamsızlaşır — yani testin kendisi kör olur."""
    _RUN_SEQ[0] += 1
    p = os.path.join(tmp, "root-%03d" % _RUN_SEQ[0])
    os.makedirs(os.path.join(p, "01_SOURCE"), exist_ok=True)
    os.makedirs(os.path.join(p, "04_BUILD"), exist_ok=True)
    return p


def run_spec_with(cfg: dict, games: dict | None, gate: str, tmp: str,
                  gate_index: dict | None = None) -> tuple[int, str]:
    fr = fake_root(tmp)
    with open(os.path.join(fr, "project_config.json"), "w",
              encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False)
    if games is not None:
        with open(os.path.join(fr, "01_SOURCE", "puzzle_index.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(games, fh, ensure_ascii=False)
    with open(os.path.join(fr, "01_SOURCE", "gate_index.json"), "w",
              encoding="utf-8") as fh:
        json.dump(gate_index or clean_gate_index(), fh, ensure_ascii=False)
    shutil.copy2(SCHEMA, os.path.join(fr, "01_SOURCE", "puzzle.schema.json"))
    with open(os.path.join(fr, ".gate"), "w", encoding="utf-8") as fh:
        fh.write(gate)
    shutil.copy2(VALIDATE_SPEC, os.path.join(fr, "04_BUILD",
                                             "validate_spec.py"))
    out = subprocess.run(
        [sys.executable, os.path.join(fr, "04_BUILD", "validate_spec.py"),
         "--gate", gate],
        capture_output=True, text=True, timeout=120)
    return out.returncode, out.stdout + out.stderr


# ── depo fikstürü: GERÇEK bir git deposu ───────────────────────────────
def repo_fixture(tmp: str, mutate=None, commit_message: str = "fikstür",
                 add_all: bool = True, force: tuple = ()) -> str:
    """Deponun tam bir kopyasını kurar ve git ile takip ettirir.

    Sızıntı denetimleri `git ls-files` okur — yani gerçek bir depo olmadan
    TEST EDİLEMEZLER. Faz 1'e kadar hiç test edilmemiş olmalarının sebebi
    tam olarak buydu."""
    _RUN_SEQ[0] += 1
    dst = os.path.join(tmp, "repo-%03d" % _RUN_SEQ[0])
    shutil.copytree(ROOT, dst,
                    ignore=shutil.ignore_patterns(".git", "__pycache__",
                                                  "*.pyc", ".venv"))
    if mutate:
        mutate(dst)
    env = dict(os.environ,
               GIT_AUTHOR_NAME="selftest", GIT_AUTHOR_EMAIL="s@e.local",
               GIT_COMMITTER_NAME="selftest", GIT_COMMITTER_EMAIL="s@e.local")
    subprocess.run(["git", "init", "-q"], cwd=dst, env=env, timeout=60)
    if add_all:
        subprocess.run(["git", "add", "-A"], cwd=dst, env=env, timeout=60)
        # ⚠ `git add -f`: .gitignore bir dosyayı DIŞLAR ama YASAKLAMAZ.
        # Aceleci bir `-f`, korunduğu sanılan bir dizini takip listesine
        # sokabilir — kapının var olma sebebi tam olarak budur.
        for p in force:
            subprocess.run(["git", "add", "-f", p], cwd=dst, env=env, timeout=60)
        subprocess.run(["git", "commit", "-q", "-m", commit_message],
                       cwd=dst, env=env, timeout=60)
    return dst


def run_structure(repo: str) -> tuple[int, str]:
    out = subprocess.run(
        [sys.executable, os.path.join(repo, "04_BUILD",
                                      "validate_structure.py")],
        capture_output=True, text=True, timeout=120, cwd=repo)
    return out.returncode, out.stdout + out.stderr


def run_env_gate(script: str, root: str, gate: str = "phase2",
                 extra: list | None = None) -> tuple[int, str]:
    """ENIGMATICA_ROOT kancasıyla koşan kapılar (korumalı katman + kanarya)."""
    env = dict(os.environ, ENIGMATICA_ROOT=root)
    out = subprocess.run(
        [sys.executable, os.path.join(BUILD, script), "--gate", gate]
        + (extra or []),
        capture_output=True, text=True, timeout=120, env=env)
    return out.returncode, out.stdout + out.stderr


def write(path: str, body: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.failed: list[str] = []
        self.passed = 0

    def check(self, ok: bool, label: str, detail: str = "") -> None:
        if ok:
            self.passed += 1
            if self.verbose:
                print("  ✓ %s" % label)
        else:
            self.failed.append(label)
            print("  ✗ %s" % label)
            if detail:
                print("      %s" % detail.strip()[:400])


# ---------------------------------------------------------------------------
def part1_clean_passes(rep: Report, tmp: str) -> None:
    print("\n① temiz kurgu bütün kapılardan geçer (yanlış pozitif yok)")
    cfg = clean_config()
    code, out = run_spec_with(cfg, clean_games(cfg), "phase1", tmp)
    rep.check(code == 0, "temiz kurgu + phase1 → geçer", out)
    code, out = run_spec_with(confirmed_solver_config(cfg),
                              clean_games(cfg, 140, "written"), "phase2", tmp)
    rep.check(code == 0, "KAZANILMIŞ 'tested' kurgusu phase2'den geçer", out)


def part2_flaws_caught(rep: Report, tmp: str) -> None:
    print("\n② her kusurlu kurgu ilgili kapıda yakalanır (körlük yok)")

    base = clean_config()

    def spec_case(label, cfg_mut=None, games_mut=None, gate="phase1",
                  n=140, status="candidate", gi_mut=None):
        cfg = copy.deepcopy(base)
        if cfg_mut:
            cfg_mut(cfg)
        g = clean_games(cfg, n, status)
        if games_mut:
            games_mut(g)
        gi = clean_gate_index()
        if gi_mut:
            gi_mut(gi)
        code, out = run_spec_with(cfg, g, gate, tmp, gate_index=gi)
        rep.check(code != 0, label, out)

    # ── kimlik ve şema ──────────────────────────────────────────────────
    spec_case("yinelenen puzzleId YAKALANIR",
              games_mut=lambda g: g["puzzles"][7].__setitem__(
                  "puzzleId", g["puzzles"][3]["puzzleId"]))
    spec_case("tanımsız kapı YAKALANIR",
              games_mut=lambda g: g["puzzles"][11].__setitem__(
                  "gate", "uydurma-kapi"))
    spec_case("geçersiz status YAKALANIR",
              games_mut=lambda g: g["puzzles"][5].__setitem__("status", "belki"))
    spec_case("geçersiz bulmaca tipi YAKALANIR",
              games_mut=lambda g: g["puzzles"][8].__setitem__(
                  "type", "uydurma-tip"))
    spec_case("kimlik kalıbına uymayan puzzleId YAKALANIR",
              games_mut=lambda g: g["puzzles"][2].__setitem__(
                  "puzzleId", "BÜYÜK HARFLİ KİMLİK"))
    spec_case("zorunlu alan eksikliği YAKALANIR (leakClass silindi)",
              games_mut=lambda g: g["puzzles"][4].pop("leakClass"))
    # ⭑ ŞEMA İZİN LİSTESİ: akla gelmemiş bir alan adı da reddedilmeli.
    spec_case("⭑ ŞEMADA TANIMSIZ ALAN YAKALANIR (izin listesi) ⭑",
              games_mut=lambda g: g["puzzles"][6].__setitem__(
                  "uydurma_alan", "x"))

    # ── ⭑ VAROLUŞSAL: public katmanda çözüm ⭑ ───────────────────────────
    for i, field in enumerate(("solution", "answerKey", "finalAnswer",
                               "hints", "title", "clues", "explanation",
                               "designIntent")):
        spec_case("⭑ PUBLIC KATMANDA '%s' YAKALANIR ⭑" % field,
                  games_mut=lambda g, f=field, i=i: g["puzzles"][i].__setitem__(
                      f, fixture_answer(i)))
    spec_case("⭑ İÇ İÇE GİZLENMİŞ ÇÖZÜM YAKALANIR ⭑",
              games_mut=lambda g: g["puzzles"][9].__setitem__(
                  "dependencies", [{"solution": fixture_answer(1)}]))

    # ── ⭑ TEST DURUMU: 'tested' KAZANILIR ⭑ ─────────────────────────────
    def tested(g, i=0, **over):
        p = g["puzzles"][i]
        p.update({"status": "written", "testStatus": "tested",
                  "solverTestCount": 5, "solverSolvedCount": 4,
                  "alternativeSolutionAnalysisDone": True,
                  "confirmedAlternativeSolutions": 0, "ambiguityScore": 1})
        p.update(over)

    confirm = lambda c: c["founder"]["externalSolvers"].__setitem__(
        "founderConfirmed", True)

    spec_case("⭑ KURUCU ONAYI OLMADAN 'tested' YAKALANIR ⭑",
              games_mut=lambda g: tested(g), gate="phase2", status="candidate")
    spec_case("⭑ 'written' AMA 'untested' YAKALANIR ⭑",
              cfg_mut=confirm, gate="phase2",
              games_mut=lambda g: g["puzzles"][0].update(
                  {"status": "written", "testStatus": "untested"}))
    spec_case("⭑ Kapı I'de 5'ten AZ çözücüyle 'tested' YAKALANIR ⭑",
              cfg_mut=confirm, gate="phase2",
              games_mut=lambda g: tested(g, 0, solverTestCount=2,
                                         solverSolvedCount=2))
    spec_case("⭑ ÇÖZEN SAYISI EŞİĞİN ALTINDA 'tested' YAKALANIR ⭑",
              cfg_mut=confirm, gate="phase2",
              games_mut=lambda g: tested(g, 0, solverSolvedCount=1))
    spec_case("⭑ ALTERNATİF ANALİZİ YAPILMADAN 'tested' YAKALANIR ⭑",
              cfg_mut=confirm, gate="phase2",
              games_mut=lambda g: tested(
                  g, 0, alternativeSolutionAnalysisDone=False))
    spec_case("⭑ ONAYLANMIŞ ALTERNATİFLE 'tested' YAKALANIR ⭑",
              cfg_mut=confirm, gate="phase2",
              games_mut=lambda g: tested(g, 0, confirmedAlternativeSolutions=1))
    spec_case("⭑ BELİRSİZLİK 3 İLE 'tested' YAKALANIR ⭑",
              cfg_mut=confirm, gate="phase2",
              games_mut=lambda g: tested(g, 0, ambiguityScore=3))
    spec_case("⭑ BELİRSİZLİK ALANI SİLİNEREK KAPI KAPATILAMAZ ⭑",
              cfg_mut=confirm, gate="phase2",
              games_mut=lambda g: (tested(g, 0),
                                   g["puzzles"][0].pop("ambiguityScore")))
    spec_case("'internal-only' iddiası harici sayaçla ÇELİŞİRSE YAKALANIR",
              games_mut=lambda g: g["puzzles"][0].update(
                  {"testStatus": "internal-only", "solverTestCount": 3}))
    spec_case("UYDURMA çözücü sayacı YAKALANIR (havuzdan büyük)",
              cfg_mut=confirm, gate="phase2",
              games_mut=lambda g: tested(g, 0, solverTestCount=40,
                                         solverSolvedCount=40))
    spec_case("çözen > deneyen ÇELİŞKİSİ YAKALANIR",
              games_mut=lambda g: g["puzzles"][0].update(
                  {"solverTestCount": 1, "solverSolvedCount": 5}))

    # ── config sözleşmesi ───────────────────────────────────────────────
    spec_case("kapı toplamı ↔ hedef çelişkisi YAKALANIR",
              cfg_mut=lambda c: c["scope"]["gateStructure"][0].__setitem__(
                  "puzzles", 5))
    spec_case("ZORLUK EĞRİSİ DÜŞÜŞÜ YAKALANIR",
              cfg_mut=lambda c: c["scope"]["gateStructure"][4].__setitem__(
                  "difficulty", 1))
    for field in ("uniqueSolutionRequired", "alternativeSolutionAnalysisRequired",
                  "hintMustNotContainAnswer", "dependencyGraphMustBeAcyclic"):
        spec_case("⭑ SÖZLEŞME GEVŞETMESİ YAKALANIR: %s ⭑" % field,
                  cfg_mut=lambda c, f=field: c["solvability"].__setitem__(f, False))
    spec_case("⭑ İÇ ÇÖZÜCÜNÜN KANIT SAYILMASI YAKALANIR ⭑",
              cfg_mut=lambda c: c["solvability"]["testStatusRequirements"]
              .__setitem__("internalSolverCountsAsEvidence", True))
    spec_case("⭑ ÖLDÜRME KAPISI EŞİĞİ DÜŞÜRÜLMESİ YAKALANIR ⭑",
              cfg_mut=lambda c: c["killGate"]["passCriteria"].__setitem__(
                  "solversCompletingGateI", 1))
    spec_case("BULMACA BAŞINA ÇÖZÜCÜ TABANININ KALDIRILMASI YAKALANIR",
              cfg_mut=lambda c: c["killGate"]["passCriteria"].pop(
                  "minSolversPerPuzzle"))
    spec_case("MEDYAN TANIMININ BELİRSİZLEŞTİRİLMESİ YAKALANIR",
              cfg_mut=lambda c: c["killGate"]["passCriteria"].__setitem__(
                  "medianDefinition", "belirsiz"))
    spec_case("ÇÖZÜM ALAN LİSTESİ AYRIŞMASI YAKALANIR",
              cfg_mut=lambda c: c["contentProtection"].__setitem__(
                  "solutionFieldNames", ["solution"]))
    spec_case("YASAK PUBLIC ALAN LİSTESİNİN DARALTILMASI YAKALANIR",
              cfg_mut=lambda c: c["contentProtection"].__setitem__(
                  "forbiddenPublicFields", ["solution"]))
    spec_case("NEGATİF TELİF yakalanır (fiyat < baskı maliyeti)",
              cfg_mut=lambda c: [ed.__setitem__("list", 2.99)
                                 for ed in c["production"]["editionsHypothesis"]
                                 if ed["id"] == "paperback"])
    spec_case("KINDLE AÇILMASI YAKALANIR (görsel şifre koruması)",
              cfg_mut=lambda c: [ed.update({"enabled": True, "list": 9.99})
                                 for ed in c["production"]["editionsHypothesis"]
                                 if ed["id"] == "kindle"])
    spec_case("gate_index'te EKSİK kapı YAKALANIR",
              gi_mut=lambda gi: gi["gates"].pop(0))
    spec_case("gate_index ↔ config zorluk AYRIŞMASI YAKALANIR",
              gi_mut=lambda gi: gi["gates"][0].__setitem__("difficulty", 3))
    spec_case("gate_index'te İŞARETSİZ fazla kapı YAKALANIR",
              gi_mut=lambda gi: gi["gates"].append(
                  {"id": "kacak-kapi", "difficulty": 1, "puzzles": 20}))


def part3_gates_lock(rep: Report, tmp: str) -> None:
    print("\n③ kapı seviyeleri gerçekten kilitliyor")

    cfg = clean_config()
    ok = confirmed_solver_config(cfg)

    code, out = run_spec_with(cfg, None, "phase0", tmp)
    rep.check(code == 0, "phase0 envantersiz geçer", out)

    code, out = run_spec_with(cfg, None, "phase1", tmp)
    rep.check(code != 0, "phase1 envantersiz KIRMIZI", out)

    code, out = run_spec_with(cfg, clean_games(cfg, 100), "phase1", tmp)
    rep.check(code != 0, "phase1 yetersiz adayla KIRMIZI (100 < 130)", out)

    code, out = run_spec_with(cfg, clean_games(cfg, 140, "candidate"),
                              "phase2", tmp)
    rep.check(code != 0,
              "⭑ phase2 (ÖLDÜRME KAPISI) doğrulanmış bulmaca olmadan KIRMIZI ⭑",
              out)

    g = clean_games(ok, 140, "candidate")
    for i in range(20):
        g["puzzles"][i].update({
            "status": "written", "testStatus": "tested",
            "solverTestCount": 5, "solverSolvedCount": 4,
            "alternativeSolutionAnalysisDone": True,
            "confirmedAlternativeSolutions": 0, "ambiguityScore": 1})
    code, out = run_spec_with(ok, g, "phase2", tmp)
    rep.check(code == 0, "phase2 20 KAZANILMIŞ bulmacayla geçer", out)

    code, out = run_spec_with(ok, g, "phase4", tmp)
    rep.check(code != 0, "phase4 eksik manuscript ile KIRMIZI", out)


def part4_exemptions(rep: Report) -> None:
    print("\n④ muafiyet listeleri DONDURULMUŞ ve canlı")

    sys.path.insert(0, BUILD)
    import validate_structure as vs   # noqa: E402

    # ⭑ TAM KÜME EŞİTLİĞİ. Eski test "muafiyet gerekli mi" diye sorup
    # dosyada bir çözüm işareti ARIYORDU — yani yeni bir muafiyeti
    # meşrulaştırmanın yolu, o dosyaya bir çözüm işareti koymaktı.
    rep.check(vs.SOLUTION_SCAN_SKIP == frozenset({
        "01_SOURCE/puzzle.schema.json",
        "00_CONTEXT/CONTENT_PROTECTION.md"}),
        "⭑ çözüm taraması muafiyeti DONDURULMUŞ (tam küme eşitliği) ⭑")

    for rel in sorted(vs.SOLUTION_SCAN_SKIP | vs.LEAK_SCAN_SKIP
                      | vs.EMBED_SCAN_SKIP):
        if rel.startswith("06_REPORTS/"):
            continue          # üretilen dosya; yokluğu ölü muafiyet değildir
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "muafiyet canlı: %s" % rel)

    import re                        # noqa: E402
    for rel in sorted(vs.LEAK_SCAN_SKIP):
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            body = fh.read()
        hits = sum(1 for pat in vs.LEAK_MARKERS if re.search(pat, body))
        rep.check(hits >= vs.LEAK_MIN_HITS,
                  "muafiyet GEREKLİ (yoksa yakalanırdı): %s [%d işaret]"
                  % (rel, hits))

    # ⭑ PROTECTED_DIRS — yanlış yazılmış bir yol, HİÇ koruma demektir.
    for d in vs.PROTECTED_DIRS:
        rep.check(os.path.isdir(os.path.join(ROOT, d)),
                  "korumalı dizin diskte var: %s" % d)
        probe = os.path.join(d, "leak-probe.json")
        r = subprocess.run(["git", "check-ignore", "-q", probe],
                           cwd=ROOT, capture_output=True, timeout=15)
        rep.check(r.returncode == 0,
                  ".gitignore korumalı dizini kapsıyor: %s" % d)

    # Muafiyet TAM YOL olmalı: temel ad muafiyeti her alt dizine bir
    # bedava dosya verirdi.
    rep.check(all("/" in p for p in vs.PROTECTED_DIR_ALLOW),
              "korumalı dizin muafiyetleri TAM YOL (temel ad değil)")
    rep.check(all("/" in p for p in vs.MANUSCRIPT_ALLOW),
              "manuscript muafiyetleri TAM YOL")


def part5_repo_gate(rep: Report, tmp: str) -> None:
    print("\n⑤ ⭑ DEPO KAPISI — gerçek git deposunda sızıntı fikstürleri ⭑")

    base = repo_fixture(tmp)
    code, out = run_structure(base)
    rep.check(code == 0, "temiz depo kopyası GEÇER (yanlış pozitif yok)", out)

    # ⭑ KAPALI BAŞARISIZLIK: .git var ama hiçbir şey takip edilmiyor.
    # Eskiden bu durumda bütün sızıntı denetimleri boş koşup YEŞİL yanardı.
    empty = repo_fixture(tmp, add_all=False)
    code, out = run_structure(empty)
    rep.check(code != 0,
              "⭑ TAKİP LİSTESİ BOŞKEN KAPI KAPANIR (fail-closed) ⭑", out)

    def case(label, mutate, force=()):
        r = repo_fixture(tmp, mutate=mutate, force=force)
        code, out = run_structure(r)
        rep.check(code != 0, label, out)

    ans = fixture_answer(0)

    case("⭑ takip edilen .json içinde çözüm ALANI YAKALANIR ⭑",
         lambda d: write(os.path.join(d, "01_SOURCE", "leak.json"),
                         '{"solutionPath": ["x"]}'))
    # Büyük harfli uzantı — eski süzgeç bunu görmüyordu.
    case("⭑ BÜYÜK HARFLİ UZANTI (.JSON) YAKALANIR ⭑",
         lambda d: write(os.path.join(d, "01_SOURCE", "LEAK.JSON"),
                         '{"answerKey": "x"}'))
    # Taranmayan uzantılar — eski süzgeç yalnızca beş uzantıya bakıyordu.
    for ext in ("yml", "py", "svg", "tex"):
        case("⭑ .%s içinde etiketli CEVAP YAKALANIR ⭑" % ext,
             lambda d, e=ext: write(os.path.join(d, "01_SOURCE", "leak." + e),
                                    "SOLUTION: %s\n" % ans))
    # Uzantısız dosya.
    case("⭑ UZANTISIZ dosyada etiketli cevap YAKALANIR ⭑",
         lambda d: write(os.path.join(d, "01_SOURCE", "ANSWERKEY"),
                         "SOLUTION: %s\n" % ans))
    # Türkçe etiket — belgelerin dili Türkçe ve kalıplar İngilizceydi.
    case("⭑ TÜRKÇE etiketli cevap YAKALANIR ⭑",
         lambda d: write(os.path.join(d, "BOOK_STATS.md"),
                         "# stats\n\nCEVAP: %s\n" % ans))
    # Temel ad muafiyeti — her alt dizine bedava bir dosya veriyordu.
    case("⭑ korumalı dizinde ALT DİZİN README'si YAKALANIR ⭑",
         lambda d: write(os.path.join(d, "01_SOURCE", "solutions", "gate-1",
                                      "README.md"),
                         "ÇÖZÜM: %s\n" % ans),
         force=("01_SOURCE/solutions/gate-1/README.md",))
    case("⭑ manuscript ALT DİZİN README'si YAKALANIR ⭑",
         lambda d: write(os.path.join(d, "02_MANUSCRIPT", "gate-1",
                                      "README.md"),
                         "What you seek is here. The plate conceals it.\n"),
         force=("02_MANUSCRIPT/gate-1/README.md",))
    case("manuscript prozası YAKALANIR (iki kural işareti)",
         lambda d: write(os.path.join(d, "06_REPORTS", "tracked", "x.md"),
                         "What you seek. The plate conceals what repeats.\n"))
    case("bulmaca BAŞLIĞI tek başına YAKALANIR",
         lambda d: write(os.path.join(d, "06_REPORTS", "tracked", "t.md"),
                         "Enigma XIV: bir başlık\n"))
    case("sır benzeri dize YAKALANIR",
         lambda d: write(os.path.join(d, "06_REPORTS", "tracked", "s.md"),
                         "token: ghp_%s\n" % ("a" * 36)))
    # ⚠ Değer LİTERAL yazılmaz: bu dosya public'tir ve tek doğruluk kaynağı
    # kuralı kendisi için de geçerlidir. Kaynağından okunur.
    sys.path.insert(0, BUILD)
    import validate_structure as _vs   # noqa: E402
    case("gömülü kurucu değeri YAKALANIR",
         lambda d: write(os.path.join(d, "04_BUILD", "kacak.py"),
                         "PUBLISHER = %r\n" % _vs.SINGLE_SOURCE_VALUES[1]))
    case("zorunlu dosya EKSİKLİĞİ YAKALANIR",
         lambda d: os.remove(os.path.join(d, "00_CONTEXT", "HINT_LADDER.md")))
    # ⭑ KLON GERÇEĞİ: dizin diskte durabilir ama takip edilen dosyası yoksa
    # klonda YOKTUR. Bu tam olarak Faz 1'de CI'ı kırmızı yakan kusurdur.
    case("⭑ TAKİP EDİLMEYEN zorunlu dizin YAKALANIR (klonda yok) ⭑",
         lambda d: os.remove(os.path.join(d, "06_REPORTS", "solver", ".gitkeep")))
    case("çözüm alan listesi config ↔ betik AYRIŞMASI YAKALANIR",
         lambda d: _mutate_json(
             os.path.join(d, "project_config.json"),
             lambda c: c["contentProtection"].__setitem__(
                 "solutionFieldNames", ["solution"])))
    case("korumalı dizin listesi AYRIŞMASI YAKALANIR",
         lambda d: _mutate_json(
             os.path.join(d, "project_config.json"),
             lambda c: c["contentProtection"].__setitem__(
                 "protectedDirs", ["01_SOURCE/solutions/"])))


def _mutate_json(path: str, fn) -> None:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    fn(data)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def part6_canary(rep: Report, tmp: str) -> None:
    print("\n⑥ ⭑ KANARYA — cevabın kendisi aranıyor ⭑")

    ans = fixture_answer(3)

    def canary_root(leak_where=None, message="temiz fikstür"):
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "canary-%03d" % _RUN_SEQ[0])
        os.makedirs(os.path.join(d, "01_SOURCE", "solutions"))
        os.makedirs(os.path.join(d, "06_REPORTS", "tracked"))
        write(os.path.join(d, ".gate"), "phase2")
        write(os.path.join(d, "01_SOURCE", "solutions", "gate-1.json"),
              json.dumps({"puzzleId": "fixture-001", "finalAnswer": ans,
                          "hints": ["a", "b", "c"]}, ensure_ascii=False))
        write(os.path.join(d, "README.md"), "# kurgu depo\n")
        name = "notes.md"
        if leak_where == "file":
            write(os.path.join(d, "notes.md"),
                  "bir cümle icinde %s gecmektedir\n" % ans)
        elif leak_where == "filename":
            name = "%s.md" % ans.lower().replace(" ", "-")
            write(os.path.join(d, name), "# bos\n")
        else:
            write(os.path.join(d, "notes.md"), "temiz\n")
        env = dict(os.environ, GIT_AUTHOR_NAME="s", GIT_AUTHOR_EMAIL="s@e.l",
                   GIT_COMMITTER_NAME="s", GIT_COMMITTER_EMAIL="s@e.l")
        subprocess.run(["git", "init", "-q"], cwd=d, env=env, timeout=60)
        subprocess.run(["git", "add", "-A", "-f"], cwd=d, env=env, timeout=60)
        subprocess.run(["git", "commit", "-q", "-m", message], cwd=d, env=env,
                       timeout=60)
        return d

    d = canary_root()
    code, out = run_env_gate("qa_solution_leak.py", d)
    rep.check(code == 0, "kanarya temiz fikstürde GEÇER (kip A)", out)

    d = canary_root(leak_where="file")
    code, out = run_env_gate("qa_solution_leak.py", d)
    rep.check(code != 0,
              "⭑ ETİKETSİZ PROZA İÇİNDEKİ CEVAP YAKALANIR ⭑", out)

    d = canary_root(leak_where="filename")
    code, out = run_env_gate("qa_solution_leak.py", d)
    rep.check(code != 0, "⭑ DOSYA ADINDAKİ cevap YAKALANIR ⭑", out)

    d = canary_root(message="g1-007 duzeltme: kapi kelimesi %s" % ans)
    code, out = run_env_gate("qa_solution_leak.py", d)
    rep.check(code != 0,
              "⭑ COMMIT MESAJINDAKİ cevap YAKALANIR (geri alınamaz) ⭑", out)

    # KİP C — korumalı katman da tuz da yok.
    _RUN_SEQ[0] += 1
    bare = os.path.join(tmp, "canary-bare-%03d" % _RUN_SEQ[0])
    os.makedirs(bare)
    write(os.path.join(bare, ".gate"), "phase2")
    env = dict(os.environ)
    env.pop("ENIGMATICA_CANARY_SALT", None)
    out = subprocess.run(
        [sys.executable, os.path.join(BUILD, "qa_solution_leak.py"),
         "--gate", "phase2"],
        capture_output=True, text=True, timeout=120,
        env=dict(env, ENIGMATICA_ROOT=bare))
    rep.check(out.returncode != 0,
              "⭑ KANARYA KOŞMAZSA phase2 KIRMIZI (sessiz yeşil yok) ⭑",
              out.stdout + out.stderr)
    out = subprocess.run(
        [sys.executable, os.path.join(BUILD, "qa_solution_leak.py"),
         "--gate", "phase1"],
        capture_output=True, text=True, timeout=120,
        env=dict(env, ENIGMATICA_ROOT=bare))
    rep.check(out.returncode == 0,
              "kanarya phase1'de boş koşabilir (henüz korunacak cevap yok)",
              out.stdout + out.stderr)


def part7_protected_gates(rep: Report, tmp: str) -> None:
    print("\n⑦ ⭑ KORUMALI KATMAN — çözüm, tekillik ve ipucu kapıları ⭑")

    cfg = clean_config()

    def rec(i=1, **over):
        ans = fixture_answer(i)
        r = {
            "puzzleId": "fixture-%03d" % i,
            "title": "kurgu",
            "objective": "Dizeyi kısa bir talimatla bul.",
            "readerAction": "Levhadaki dizi soldan saga okunur.",
            "input": "levha",
            "clues": ["ilk ipucu metni", "ikinci ipucu metni"],
            "constraints": ["dizi tek yonde okunur", "baslangic isaretli"],
            "intendedSolution": ans,
            "finalAnswer": ans,
            "explanation": "Dizi cevirisi sonucu.",
            "solutionPath": [
                {"step": "dizi sayilir", "usesOnlyBookKnowledge": True,
                 "sourceInBook": "araclar levhasi"},
                {"step": "harfler cevrilir", "usesOnlyBookKnowledge": True,
                 "sourceInBook": "araclar levhasi"},
                {"step": "kelime okunur", "usesOnlyBookKnowledge": True,
                 "sourceInBook": "sayfa"},
            ],
            "hints": ["Kenar susu tekrar etmiyor.",
                      "Tekrar etmeyen dizi bir alfabe olabilir; araclar "
                      "levhasina donun.",
                      "Harfleri soldan saga cevirin; dizi sayilir ve "
                      "harfler cevrilir."],
            "alternativeSolutionsConsidered": [
                {"candidate": "aday bir", "rejected": True,
                 "reason": "metin disliyor", "reasonStrength": "mechanical"},
                {"candidate": "aday iki", "rejected": True,
                 "reason": "uzunluk tutmuyor", "reasonStrength": "mechanical"},
                {"candidate": "aday uc", "rejected": True,
                 "reason": "yon sabit", "reasonStrength": "textual"},
            ],
            "ambiguityPoints": [
                {"point": "okuma yonu", "resolution": "metin sabitliyor",
                 "residualRisk": 1}],
            "solverTests": [],
        }
        r.update(over)
        return r

    def protected_root(records, index_over=None):
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "prot-%03d" % _RUN_SEQ[0])
        os.makedirs(os.path.join(d, "01_SOURCE", "solutions"))
        write(os.path.join(d, ".gate"), "phase2")
        with open(os.path.join(d, "project_config.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(cfg, fh, ensure_ascii=False)
        entries = []
        for r in records:
            e = {"puzzleId": r["puzzleId"], "gate": "threshold",
                 "type": "cipher", "mechanismFamily": "substitution-cipher",
                 "status": "written", "testStatus": "tested",
                 "leakClass": "protected", "ambiguityScore": 1,
                 "alternativeSolutionAnalysisDone": True,
                 "confirmedAlternativeSolutions": 0}
            if index_over:
                index_over(e)
            entries.append(e)
        with open(os.path.join(d, "01_SOURCE", "puzzle_index.json"), "w",
                  encoding="utf-8") as fh:
            json.dump({"puzzles": entries}, fh, ensure_ascii=False)
        for r in records:
            with open(os.path.join(d, "01_SOURCE", "solutions",
                                   "%s.json" % r["puzzleId"]), "w",
                      encoding="utf-8") as fh:
                json.dump(r, fh, ensure_ascii=False)
        return d

    for script in ("qa_solvability.py", "qa_uniqueness.py", "qa_hints.py"):
        d = protected_root([rec(1)])
        code, out = run_env_gate(script, d)
        rep.check(code == 0, "%s temiz kayıtta GEÇER" % script, out)

    def case(script, label, mutate=None, index_over=None, records=None):
        recs = records or [rec(1)]
        if mutate:
            mutate(recs[0])
        d = protected_root(recs, index_over)
        code, out = run_env_gate(script, d)
        rep.check(code != 0, label, out)

    # ── kayıp kayıt ─────────────────────────────────────────────────────
    _RUN_SEQ[0] += 1
    d = protected_root([rec(1)])
    os.remove(os.path.join(d, "01_SOURCE", "solutions", "fixture-001.json"))
    code, out = run_env_gate("qa_solvability.py", d)
    rep.check(code != 0, "⭑ yazılmış bulmacanın KORUMALI KAYDI YOKSA KIRMIZI ⭑",
              out)

    # ── çözülebilirlik ──────────────────────────────────────────────────
    case("qa_solvability.py", "⭑ DIŞ BİLGİ GEREKTİREN ADIM YAKALANIR ⭑",
         lambda r: r["solutionPath"][1].__setitem__(
             "usesOnlyBookKnowledge", False))
    case("qa_solvability.py", "çözüm yolu YOKSA yakalanır",
         lambda r: r.__setitem__("solutionPath", []))
    case("qa_solvability.py", "⭑ KISITSIZ BULMACA YAKALANIR ⭑",
         lambda r: r.__setitem__("constraints", []))
    case("qa_solvability.py", "boş yapısal alan YAKALANIR",
         lambda r: r.__setitem__("explanation", ""))
    case("qa_solvability.py", "20 kelimeyi aşan TALİMAT YAKALANIR",
         lambda r: r.__setitem__("readerAction", " ".join(["kelime"] * 25)))
    case("qa_solvability.py", "⭑ BELİRSİZLİK PUANI GEREKÇESİYLE ÇELİŞİRSE ⭑",
         lambda r: r.__setitem__("ambiguityPoints", [
             {"point": "a", "resolution": "x", "residualRisk": 1},
             {"point": "b", "resolution": "y", "residualRisk": 1}]))
    case("qa_solvability.py", "ÇÖZÜMSÜZ belirsizlik noktası YAKALANIR",
         lambda r: r.__setitem__("ambiguityPoints", [
             {"point": "a", "resolution": "", "residualRisk": 1}]))
    case("qa_solvability.py", "belirsizlik EŞİK AŞIMI yakalanır",
         index_over=lambda e: e.__setitem__("ambiguityScore", 4))

    # ── tekillik ────────────────────────────────────────────────────────
    case("qa_uniqueness.py", "ÜÇTEN AZ alternatif aday YAKALANIR",
         lambda r: r["alternativeSolutionsConsidered"].pop())
    case("qa_uniqueness.py", "⭑ 'ZORLAMA' GEREKÇE YAKALANIR ⭑",
         lambda r: r["alternativeSolutionsConsidered"][0].__setitem__(
             "reasonStrength", "forced"))
    case("qa_uniqueness.py", "⭑ ONAYLANMIŞ ALTERNATİF ÇÖZÜM YAKALANIR ⭑",
         lambda r: r["alternativeSolutionsConsidered"][0].__setitem__(
             "rejected", False))
    case("qa_uniqueness.py", "gerekçesiz aday YAKALANIR",
         lambda r: r["alternativeSolutionsConsidered"][1].__setitem__(
             "reason", ""))
    case("qa_uniqueness.py", "⭑ ÇÖZÜCÜNÜN ÖNERDİĞİ İKİNCİ CEVAP YAKALANIR ⭑",
         lambda r: r.__setitem__("solverTests", [
             {"date": "2026-08-13", "solver": "solver-02", "usedHints": 1,
              "result": "solved", "alternativeOffered": "baska bir dize"}]))
    case("qa_uniqueness.py", "public sayaç ↔ kayıt ÇELİŞKİSİ YAKALANIR",
         index_over=lambda e: e.__setitem__("confirmedAlternativeSolutions", 2))
    case("qa_uniqueness.py", "analiz İŞARETSİZ ise yakalanır",
         index_over=lambda e: e.__setitem__(
             "alternativeSolutionAnalysisDone", False))
    case("qa_uniqueness.py", "⭑ İKİ BULMACA AYNI CEVABI VERİRSE YAKALANIR ⭑",
         records=[rec(1), rec(2, puzzleId="fixture-002",
                              finalAnswer=fixture_answer(1),
                              intendedSolution=fixture_answer(1))])

    # ── ipucu ───────────────────────────────────────────────────────────
    ans = fixture_answer(1)
    case("qa_hints.py", "İKİ KADEMELİ ipucu YAKALANIR",
         lambda r: r.__setitem__("hints", r["hints"][:2]))
    case("qa_hints.py", "BOŞ kademe YAKALANIR",
         lambda r: r["hints"].__setitem__(1, ""))
    case("qa_hints.py", "⭑ İPUCU CEVABI DÜZ İÇERİRSE YAKALANIR ⭑",
         lambda r: r["hints"].__setitem__(1, "Cevap %s olabilir." % ans))
    case("qa_hints.py", "⭑ BOŞLUKSUZ gizlenmiş cevap YAKALANIR ⭑",
         lambda r: r["hints"].__setitem__(
             1, "Bakiniz %s." % ans.replace(" ", "")))
    case("qa_hints.py", "⭑ TERS BASILMIŞ cevap YAKALANIR (ayna baskı) ⭑",
         lambda r: r["hints"].__setitem__(
             1, "Bakiniz %s." % ans.replace(" ", "")[::-1]))
    # Cevabın kelimeleri dağıtılmış: düz alt dize araması bunu göremez.
    case("qa_hints.py", "⭑ DAĞITILMIŞ kelimelerle cevap YAKALANIR ⭑",
         lambda r: r["hints"].__setitem__(
             1, "Once %s dusunun, sonra %s ve nihayet %s."
                % (ans.split()[2], ans.split()[0], ans.split()[1])))
    case("qa_hints.py", "AYNI iki kademe YAKALANIR",
         lambda r: r["hints"].__setitem__(0, r["hints"][1]))
    case("qa_hints.py", "40 kelimeyi aşan ipucu YAKALANIR",
         lambda r: r["hints"].__setitem__(2, " ".join(["kelime"] * 45)))
    case("qa_hints.py", "⭑ 3. KADEME SON ADIMI VERİRSE YAKALANIR ⭑",
         lambda r: r["hints"].__setitem__(
             2, "Kelime okunur ve harfler cevrilir; kelime okunur."))


def part8_answerspace(rep: Report, tmp: str) -> None:
    """⑧ FAZ 2'NİN ÜÇ YENİ KAPISI + TÜRKÇE KATLAMASI.

    Her fikstür Faz 2'de GERÇEKTEN YAŞANMIŞ bir kusuru yeniden kurar.
    Bunlar hayalî senaryolar değil; kapılar bu kusurları üretim verisinde
    yakaladı ve fikstürler o yakalayışın tekrarlanabilir kanıtıdır."""
    print("\n⑧ ⭑ CEVAP UZAYI · DEVİR · OKUR PAKETİ · TÜRKÇE KATLAMASI ⭑")

    cfg = clean_config()
    ALPHA = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    # ⚠ FİKSTÜR SÖZLÜĞÜ GERÇEK SÖZLÜKLE HİÇBİR ÜYE PAYLAŞMAZ.
    # İlk yazımda paylaşıyordu ve KANARYA BU DOSYAYI SIZINTI OLARAK YAKALADI
    # — haklı olarak: bir fikstür cevabı gerçek bir cevapla aynıysa, o cevap
    # public depoda düz metin olarak durur. Kanaryanın kendi test dosyasını
    # yakalaması, kapının çalıştığının en temiz kanıtıdır.
    LEX = ["ZURNA", "MELTEM", "KAVUN", "SEMAVER", "YELPAZE", "KUNDURA",
           "PALAMUT", "ŞEBEKE", "TERLİK", "VİRAJ", "OYMACI", "PATİKA",
           "SÜRAHİ", "MERCAN"]

    def glyph(c):
        i = ALPHA.index(c)
        return "',+/\\x"[i // 5] * (i % 5 + 1)

    def enc(w):
        return "·".join(glyph(c) for c in w)

    def shift(w, k):
        return "".join(ALPHA[(ALPHA.index(c) + k) % 29] for c in w)

    tools = {"charts": {
        "esik-alfabesi": {"alphabet": ALPHA,
                          "table": [{"letter": c, "glyph": glyph(c)}
                                    for c in ALPHA]},
        "esik-sozlugu": {"entries": [{"no": i + 1, "word": w}
                                     for i, w in enumerate(LEX)]},
        "kapi-sozleri": {"entries": ["ZURNA SESİ", "MELTEM KAR",
                                     "KAVUN KESTİ"]},
        "esik-sayilari": {"entries": [{"sira": 1, "dortlu": "2413",
                                       "sozlukNo": 3}]}}}

    def space_root(space, answer="MELTEM", page=None, index_over=None):
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "space-%03d" % _RUN_SEQ[0])
        for sub in ("01_SOURCE/solutions", "01_SOURCE/design", "02_MANUSCRIPT"):
            os.makedirs(os.path.join(d, sub))
        write(os.path.join(d, ".gate"), "phase2")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/design/tools-plate.json"),
              json.dumps(tools, ensure_ascii=False))
        e = {"puzzleId": "fixture-001", "gate": "threshold", "type": "cipher",
             "mechanismFamily": "substitution-cipher", "status": "written",
             "testStatus": "tested", "leakClass": "protected",
             "ambiguityScore": 1, "alternativeSolutionAnalysisDone": True,
             "confirmedAlternativeSolutions": 0}
        if index_over:
            index_over(e)
        write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
              json.dumps({"puzzles": [e]}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/solutions/gate-1.json"),
              json.dumps({"puzzles": [{
                  "puzzleId": "fixture-001", "finalAnswer": answer,
                  "hints": ["birinci kademe metni", "ikinci kademe metni",
                            "ucuncu kademe metni"],
                  "answerSpace": space}]}, ensure_ascii=False))
        if page is not None:
            write(os.path.join(d, "02_MANUSCRIPT/book.json"),
                  json.dumps({"puzzles": [page]}, ensure_ascii=False))
        return d

    CLEAN = {"generator": {"kind": "cyclic-shift", "input": shift("MELTEM", 9)},
             "acceptance": {"kind": "in-printed-lexicon"},
             "declaredAcceptedCount": 1}

    d = space_root(CLEAN)
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code == 0, "qa_answerspace temiz kayıtta GEÇER", out)

    # ⭑ Faz 2'de GERÇEKTEN olan kusur: üç koşul ÜÇ cevap bırakıyordu.
    d = space_root({"generator": {"kind": "printed-lexicon"},
                    "acceptance": {"kind": "satisfies-printed-constraints",
                                   "constraints": [{"op": "length", "value": 5}]},
                    "declaredAcceptedCount": 1}, answer="ZURNA")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0, "⭑ İKİNCİ CEVABI OLAN BULMACA YAKALANIR ⭑", out)

    # Alan hiçbir üye kabul etmiyorsa bulmaca ÇÖZÜLEMEZ.
    d = space_root({"generator": {"kind": "cyclic-shift", "input": "ZZZZZZ"},
                    "acceptance": {"kind": "in-printed-lexicon"},
                    "declaredAcceptedCount": 1})
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0, "⭑ HİÇBİR ÜYE KABUL EDİLMİYORSA (ÇÖZÜLEMEZ) KIRMIZI ⭑",
              out)

    # ⭑ Faz 2'de GERÇEKTEN olan kusur: mekanizma alanı iki üyeliydi.
    d = space_root({"generator": {"kind": "glyph-chart-reading",
                                  "glyphs": enc("MELTEM"),
                                  "directions": ["forward", "reverse"]},
                    "acceptance": {"kind": "in-printed-lexicon"},
                    "declaredAcceptedCount": 1}, answer="MELTEM")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0, "⭑ SAYIM ALANI ÇOK KÜÇÜKSE (ispat değil) KIRMIZI ⭑",
              out)

    # 'yazar öyle diyor' — totolojinin adı.
    d = space_root({"generator": {"kind": "printed-lexicon"},
                    "acceptance": {"kind": "author-asserted"},
                    "declaredAcceptedCount": 1})
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0, "⭑ 'YAZAR ÖYLE DİYOR' KABUL YORDAMI YAKALANIR ⭑", out)

    # Bildirilen sayaç ölçümle ayrışıyorsa.
    d = space_root(dict(CLEAN, declaredAcceptedCount=0))
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0, "bildirilen kabul sayısı AYRIŞIRSA yakalanır", out)

    # Kabul edilen üye yazarın cevabı değilse.
    d = space_root(CLEAN, answer="ZURNA")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0, "⭑ KABUL EDİLEN ÜYE CEVAPTAN FARKLIYSA KIRMIZI ⭑", out)

    # ── OKUR PAKETİ — Faz 2'nin en pahalı bulgusu ───────────────────────
    PAGE = {"puzzleId": "fixture-001", "objective": "Dizeyi cozun.",
            "input": "Sayfada basili dize: %s" % shift("MELTEM", 9),
            "clues": [], "constraints": []}
    d = space_root(CLEAN, page=PAGE)
    code, out = run_env_gate("qa_readerpack.py", d)
    rep.check(code == 0, "qa_readerpack temiz okur sayfasında GEÇER", out)

    # ⭑ Şifreli dize okurun elinde YOKSA bulmaca çözülemez.
    d = space_root(CLEAN, page=dict(PAGE, input="Sayfada bir dize var."))
    code, out = run_env_gate("qa_readerpack.py", d)
    rep.check(code != 0,
              "⭑ ŞİFRELİ DİZE OKUR SAYFASINDA YOKSA KIRMIZI ⭑", out)

    # ⭑ GERÇEK FAZ 2 KUSURU: levha verisi yalnızca cevap anahtarındaydı.
    PLATE_SPACE = {"generator": {"kind": "printed-lexicon"},
                   "acceptance": {"kind": "plate-attribute",
                                  "labels": ["ZURNA", "KAVUN", "VİRAJ",
                                             "TERLİK", "OYMACI", "PATİKA"],
                                  "attributes": {"ZURNA": 1, "KAVUN": 1,
                                                 "VİRAJ": 2, "TERLİK": 1,
                                                 "OYMACI": 1, "PATİKA": 1},
                                  "rule": {"op": "==", "value": 2}},
                   "declaredAcceptedCount": 1}
    d = space_root(PLATE_SPACE, answer="VİRAJ",
                   page={"puzzleId": "fixture-001", "objective": "Levhaya bak.",
                         "input": "Levha: alti kemer.", "clues": [],
                         "constraints": []})
    code, out = run_env_gate("qa_readerpack.py", d)
    rep.check(code != 0,
              "⭑ LEVHA VERİSİ YALNIZCA CEVAP ANAHTARINDAYSA KIRMIZI ⭑ "
              "(bulmaca okur paketinde ÇÖZÜLEMEZ)", out)

    # Şekil var ama etiket künyeleri yok → kör şekil.
    d = space_root(PLATE_SPACE, answer="VİRAJ",
                   page={"puzzleId": "fixture-001", "objective": "Levhaya bak.",
                         "input": "Levha.", "figure": "◆ ◆◆ ◆ ◆ ◆ ◆",
                         "clues": [], "constraints": []})
    code, out = run_env_gate("qa_readerpack.py", d)
    rep.check(code != 0, "⭑ ETİKET KÜNYESİ TAŞIMAYAN KÖR ŞEKİL YAKALANIR ⭑", out)

    # Cevap sayfada BEDAVA duruyorsa (akransız).
    d = space_root(CLEAN, page=dict(PAGE, objective="Cevap MELTEM degil mi."))
    code, out = run_env_gate("qa_readerpack.py", d)
    rep.check(code != 0, "⭑ CEVABI KENDİ SAYFASINDA BEDAVA DURAN BULMACA ⭑", out)

    # ── SAYI TABLOSU — Faz 2'nin EN AĞIR bulgusunun fikstürü ────────────
    #
    # Levha içi şifrede okur dört kenarı okur; başlangıç köşesi ve yön
    # yanlışsa SEKİZ farklı dörtlü çıkar. Tasarım "yanlış okuma tabloda
    # yoktur, yani hata tespit edilir" diyordu.
    #
    # ÖLÇÜLDÜĞÜNDE sekiz okumanın BEŞİ tablodaydı: her levha bulmacasının
    # beş ulaşılabilir cevabı vardı. Kapı bunu GÖRMEMİŞTİ çünkü kabul
    # yordamı yalnızca YAZARIN SEÇTİĞİ okumaya bakıyordu — K21'in öldürmeye
    # çalıştığı totolojinin ta kendisi, bu kez kapının kendi içinde.
    NUM_TABLE = [{"sira": 1, "dortlu": "2413", "sozlukNo": 1},
                 {"sira": 2, "dortlu": "4132", "sozlukNo": 5},
                 {"sira": 3, "dortlu": "1245", "sozlukNo": 9}]
    ALL8 = ["2413", "4132", "1324", "3241", "2314", "3142", "1423", "4231"]

    d = space_root({"generator": {"kind": "printed-lexicon"},
                    "acceptance": {"kind": "reachable-via-number-table",
                                   "readings": ["2413"],
                                   "table": NUM_TABLE},
                    "declaredAcceptedCount": 1}, answer="ZURNA")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code == 0, "sayı tablosu · TEK okuma bildirildiğinde geçer "
                         "(eski, totolojik kurgu)", out)

    d = space_root({"generator": {"kind": "printed-lexicon"},
                    "acceptance": {"kind": "reachable-via-number-table",
                                   "readings": ALL8, "table": NUM_TABLE},
                    "declaredAcceptedCount": 1}, answer="ZURNA")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0,
              "⭑ SEKİZ OKUMANIN İKİSİ TABLODAYSA KIRMIZI ⭑ "
              "(yanlış köşeden başlayan okur GEÇERLİ bir cevaba varıyor)",
              out)

    # ── DEVİR — hata tespiti olmayan kapı bulmacası ─────────────────────
    def gate_root(acc, handoff, phrases=None):
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "handoff-%03d" % _RUN_SEQ[0])
        for sub in ("01_SOURCE/solutions", "01_SOURCE/design"):
            os.makedirs(os.path.join(d, sub))
        write(os.path.join(d, ".gate"), "phase2")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg, ensure_ascii=False))
        t = json.loads(json.dumps(tools))
        if phrases is not None:
            t["charts"]["kapi-sozleri"]["entries"] = phrases
        write(os.path.join(d, "01_SOURCE/design/tools-plate.json"),
              json.dumps(t, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/gate_index.json"),
              json.dumps(clean_gate_index(), ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
              json.dumps({"puzzles": [
                  {"puzzleId": "fixture-g20", "gate": "threshold",
                   "type": "gate", "mechanismFamily": "gate-synthesis",
                   "status": "written", "testStatus": "tested",
                   "leakClass": "protected", "ambiguityScore": 1,
                   "dependencies": []}]}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/solutions/gate-1.json"),
              json.dumps({"puzzles": [{
                  "puzzleId": "fixture-g20", "finalAnswer": "ZURNA SESİ",
                  "hints": ["a", "b", "c"],
                  "answerSpace": {"generator": {"kind": "printed-phrase-list"},
                                  "acceptance": acc,
                                  "declaredAcceptedCount": 1}}]},
                         ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/design/gate-1.json"),
              json.dumps({"puzzles": [{"puzzleId": "fixture-g20",
                                       "handoff": handoff}]},
                         ensure_ascii=False))
        return d

    # Kaynak/konum çifti HEDEFTEN TÜRETİLİR: elle yazılmış bir çift,
    # fikstürü sessizce geçersiz kılabilir.
    _target = [c for c in "ZURNA SESİ" if c in ALPHA]
    _src, _pos = [], []
    for _ch in _target:
        _w = next(w for w in LEX if _ch in w)
        _src.append(_w)
        _pos.append(_w.index(_ch) + 1)
    GOOD_ACC = {"kind": "matches-positional-extraction",
                "sources": _src, "positions": _pos}
    GOOD_HO = {"recoveryPath": "Grup isaretiyle karsilastirin.",
               "nonDestructiveProgression": True,
               "diagnosticMarks": [
                   {"slot": i + 1,
                    "group": ALPHA.index(s[p - 1]) // 5 + 1}
                   for i, (s, p) in enumerate(zip(GOOD_ACC["sources"],
                                                  GOOD_ACC["positions"]))]}
    d = gate_root(GOOD_ACC, GOOD_HO)
    code, out = run_env_gate("qa_handoff.py", d)
    rep.check(code == 0, "qa_handoff temiz kapı bulmacasında GEÇER", out)

    d = gate_root({"kind": "in-printed-lexicon"}, GOOD_HO)
    code, out = run_env_gate("qa_handoff.py", d)
    rep.check(code != 0,
              "⭑ HATA TESPİTİ OLMAYAN KAPI BULMACASI YAKALANIR (sessiz yanlış) ⭑",
              out)

    bad = dict(GOOD_HO, diagnosticMarks=[dict(m, group=1)
                                          for m in GOOD_HO["diagnosticMarks"]])
    d = gate_root(GOOD_ACC, bad)
    code, out = run_env_gate("qa_handoff.py", d)
    rep.check(code != 0,
              "⭑ TEŞHİS İŞARETİ BAĞIMSIZ HESAPLA AYRIŞIRSA KIRMIZI ⭑", out)

    d = gate_root(GOOD_ACC, dict(GOOD_HO, recoveryPath=""))
    code, out = run_env_gate("qa_handoff.py", d)
    rep.check(code != 0, "kurtarma yolu YOKSA yakalanır", out)

    # ⭑ Basılı liste hata TESPİT ETMİYORSA — iki ifade bir harf uzaklıkta.
    d = gate_root(GOOD_ACC, GOOD_HO,
                  phrases=["ZURNA SESİ", "ZURNA SESE", "MELTEM KAR"])
    code, out = run_env_gate("qa_handoff.py", d)
    rep.check(code != 0,
              "⭑ HATA TESPİT LİSTESİ BİR HARF UZAKLIKTA İFADE TAŞIRSA ⭑ "
              "(tek hata GİZLENİR, tespit edilmez)", out)

    # ── TÜRKÇE KATLAMASI — pilot dilinin ölçüm makinesini kırdığı yer ──
    sys.path.insert(0, BUILD)
    import _protected_layer as _pl                             # noqa: E402
    import qa_solution_leak as _leak                           # noqa: E402
    rep.check(_pl.squeeze("IŞIK") == _pl.squeeze("ışık") == "isik",
              "⭑ TÜRKÇE KATLAMASI: 'IŞIK' ile 'ışık' AYNI dizeye iniyor ⭑",
              "%r vs %r" % (_pl.squeeze("IŞIK"), _pl.squeeze("ışık")))
    rep.check(_leak.squeeze("IŞIK") == _pl.squeeze("ışık"),
              "kanarya ile korumalı katman AYNI katlamayı kullanıyor",
              "%r vs %r" % (_leak.squeeze("IŞIK"), _pl.squeeze("ışık")))
    rep.check(_pl.squeeze("GÖLGE") == "golge" and _pl.squeeze("ÇAKIL") == "cakil",
              "Türkçe aksanlar normalize ediliyor (ö→o · ç→c · ş→s · ğ→g)")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  KAPILARIN KENDİ TESTİ · Codex Enigmatica")
    print("=" * 74)

    rep = Report(args.verbose)
    with tempfile.TemporaryDirectory() as tmp:
        part1_clean_passes(rep, tmp)
        part2_flaws_caught(rep, tmp)
        part3_gates_lock(rep, tmp)
        part4_exemptions(rep)
        part5_repo_gate(rep, tmp)
        part6_canary(rep, tmp)
        part7_protected_gates(rep, tmp)
        part8_answerspace(rep, tmp)

    print("\n" + "=" * 74)
    if rep.failed:
        print("  ⛔ %d KÖRLÜK BULUNDU (%d denetim geçti)"
              % (len(rep.failed), rep.passed))
        for f in rep.failed:
            print("     · %s" % f)
        print("=" * 74)
        print("\n  Bir kapı kusuru yakalamıyorsa, o kapı YOK demektir.")
        return 1
    print("  ✅ %d denetim yeşil — bütün kapılar ısırıyor" % rep.passed)
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
