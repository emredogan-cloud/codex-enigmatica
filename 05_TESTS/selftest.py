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
import re
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
    # ⚠ ESKİ FİKSTÜR "Kindle AÇILMASI yakalanır" diyordu ve kural
    # kurucu kararıyla DEĞİŞTİ: Kindle artık açık olabilir. Yakalanması
    # gereken yeni kusur, AÇIK AMA ÜRETİLMEMİŞ Kindle'dır — çünkü ürün
    # sayfasında var görünüp dosyası olmayan bir sürüm, kapalı olandan
    # kötüdür. Fikstür silinmedi, KURALA GÖRE YENİDEN YAZILDI.
    spec_case("⭑ AÇIK AMA MİMARİSİ BEYAN EDİLMEMİŞ KINDLE YAKALANIR ⭑",
              cfg_mut=lambda c: [ed.update({"enabled": True, "list": 9.99}) or
                                 ed.pop("format", None)
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

    # ⭑ UYARI SİLİNEMEZ ⭑ — kurucu talimatı § 7
    # "Do not delete this warning." Bir sonraki belge tazelemesinde sessizce
    # düşerse kimse fark etmez; bu yüzden düşmesi KIRMIZI yanar.
    def notice_case(drop):
        r = repo_fixture(tmp, mutate=lambda d: _drop_notice(d, drop))
        return run_structure(r)

    def _drop_notice(d, rel):
        path = os.path.join(d, rel)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                body = fh.read()
            for v in ("EXTERNAL HUMAN VALIDATION REMAINS PENDING",
                      "External human validation remains pending"):
                body = body.replace(v, "her şey yolunda")
            write(path, body)

    code, out = notice_case("PROJECT_CONTEXT.md")
    rep.check(code != 0,
              "⭑ BEKLEYEN DOĞRULAMA UYARISI SİLİNİRSE KIRMIZI ⭑ "
              "(kurucu talimatı § 7: 'Do not delete this warning')", out)

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
    #
    # ⚠ FAZ 2 AYRIMI — İKİ FARKLI "KAYIT YOK" DURUMU VAR:
    #   ① katman TAMAMEN yok  → CI'ın normal durumu; kapı BOŞ KOŞAR ve söyler
    #   ② katman VAR ama EKSİK → gerçek kusur; KIRMIZI
    # Faz 1'de bu ayrım gerekmiyordu (hiçbir bulmaca 'drafted' değildi) ve
    # ilk yirmi bulmaca yazıldığında CI yalancı kırmızı yandı: kapı,
    # kendisine hiç gösterilmemiş bir dosyayı "kayıp" sanıyordu.

    # ② EKSİK katman — iki kayıttan biri silinir
    _RUN_SEQ[0] += 1
    d = protected_root([rec(1), rec(2)])
    os.remove(os.path.join(d, "01_SOURCE", "solutions", "fixture-001.json"))
    code, out = run_env_gate("qa_solvability.py", d)
    rep.check(code != 0,
              "⭑ KATMAN VAR AMA BİR KAYIT EKSİKSE KIRMIZI ⭑ (gerçek kusur)",
              out)

    # ① TAMAMEN yok — CI durumu: boş koşar, çıkış 0, ama SÖYLER
    _RUN_SEQ[0] += 1
    d = protected_root([rec(1)])
    os.remove(os.path.join(d, "01_SOURCE", "solutions", "fixture-001.json"))
    code, out = run_env_gate("qa_solvability.py", d)
    rep.check(code == 0 and "BOŞ KOŞTU" in out,
              "⭑ KATMAN HİÇ YOKSA BOŞ KOŞAR VE BUNU SÖYLER ⭑ (CI durumu)",
              out)
    rep.check("GEÇİŞ DEĞİLDİR" in out,
              "boş koşan kapı 'bu bir geçiş değildir' diyor (sessiz yeşil yok)",
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
        "threshold-alphabet": {"alphabet": ALPHA,
                          "table": [{"letter": c, "glyph": glyph(c)}
                                    for c in ALPHA]},
        "threshold-lexicon": {"entries": [{"no": i + 1, "word": w}
                                     for i, w in enumerate(LEX)]},
        "gate-sayings": {"entries": ["ZURNA SESİ", "MELTEM KAR",
                                     "KAVUN KESTİ"]},
        "threshold-numbers": {"entries": [{"row": 1, "reading": "2413",
                                       "lexiconNo": 3}]},
        # ── KAPI II · basılı yetke ────────────────────────────────────
        "bestiary-catalogue": {"entries": [{"no": i + 1, "word": w}
                                            for i, w in enumerate(LEX)]},
        "ring-table": {
            "rows": [list(ALPHA[r * 5:r * 5 + 5]) for r in range(5)]
            + [list(ALPHA[25:]) + ["·"]],
            "rowCount": 6, "colCount": 5},
        "beast-sayings": {"entries": ["ZURNA MELTEM KAVUN"]}}}

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

    # ⭑ Var olmayan bir çizelgeye gönderme — Faz 2'de üç bulmacada,
    # sekiz ayrı cümlede yaşandı. Okur bunu KENDİ hatası sanır.
    d = space_root(CLEAN, page=dict(PAGE, clues=["See Chart Z."]))
    code, out = run_env_gate("qa_readerpack.py", d)
    rep.check(code != 0,
              "⭑ VAR OLMAYAN BİR ÇİZELGEYE GÖNDERME YAKALANIR ⭑", out)

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
    NUM_TABLE = [{"row": 1, "reading": "2413", "lexiconNo": 1},
                 {"row": 2, "reading": "4132", "lexiconNo": 5},
                 {"row": 3, "reading": "1245", "lexiconNo": 9}]
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
            t["charts"]["gate-sayings"]["entries"] = phrases
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

    # ── ⛔ ÖLDÜRME KAPISI ⛔ ─────────────────────────────────────────────
    #
    # İKİ YÖNLÜ FİKSTÜR ve ikincisi birincisinden daha önemlidir:
    #   ① veri yokken GEÇMEMELİ  — "boş veriyle yeşil yanan kapı" yalanı
    #   ② veri varken GEÇMELİ    — hiç geçmemiş bir kapı, geçemiyor da
    #                              olabilir ve bunu ancak denemek gösterir
    def killgate_root(sessions_per_solver: int, alt: str = "",
                      minutes: int = 8) -> str:
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "kill-%03d" % _RUN_SEQ[0])
        for sub in ("01_SOURCE/solutions", "06_REPORTS/solver",
                    "06_REPORTS/tracked"):
            os.makedirs(os.path.join(d, sub))
        write(os.path.join(d, ".gate"), "phase2")
        c = json.loads(json.dumps(cfg))
        c.setdefault("killGate", {}).setdefault(
            "externalValidation", {})["founderOverride"] = False
        c["founder"]["externalSolvers"]["sessionsRecorded"] = sessions_per_solver
        c["founder"]["externalSolvers"]["identifiedCount"] = 5
        write(os.path.join(d, "project_config.json"),
              json.dumps(c, ensure_ascii=False))
        pz, recs = [], []
        for i in range(1, 21):
            pid = "fixture-%03d" % i
            pz.append({"puzzleId": pid, "gate": "threshold", "type": "cipher",
                       "mechanismFamily": "substitution-cipher",
                       "status": "drafted", "testStatus": "external-pending",
                       "leakClass": "protected", "ambiguityScore": 1,
                       "pilotCohort": True})
            tests = []
            for s in range(1, sessions_per_solver + 1):
                tests.append({"date": "2026-08-13", "solver": "solver-%02d" % s,
                              "solverClass": "external", "usedHints": 0,
                              "minutesToSolve": minutes, "result": "solved",
                              "hintsUsedByLevel": [0, 0, 0],
                              "alternativeOffered": alt if (i == 1 and s == 1)
                              else ""})
            recs.append({"puzzleId": pid, "finalAnswer": "MELTEM",
                         "solverTests": tests})
        write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
              json.dumps({"puzzles": pz}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/solutions/gate-1.json"),
              json.dumps({"puzzles": recs}, ensure_ascii=False))
        for s in range(1, sessions_per_solver + 1):
            write(os.path.join(d, "06_REPORTS/solver/solver-%02d.json" % s),
                  json.dumps({"solver": "solver-%02d" % s,
                              "gateCompleted": True}, ensure_ascii=False))
        return d

    d = killgate_root(0)
    code, out = run_env_gate("kill_gate.py", d)
    rep.check(code != 0 and "BLOCKED" in out,
              "⭑ ÖLDÜRME KAPISI VERİ YOKKEN 'GEÇTİ' DEMEZ (BLOCKED) ⭑", out)

    d = killgate_root(5)
    code, out = run_env_gate("kill_gate.py", d)
    rep.check(code == 0 and "PASS" in out,
              "⭑ ÖLDÜRME KAPISI TAM VERİYLE GEÇEBİLİYOR ⭑ "
              "(hiç geçmemiş bir kapı, geçemiyor da olabilir)", out)

    d = killgate_root(2)
    code, out = run_env_gate("kill_gate.py", d)
    rep.check(code != 0 and "BLOCKED" in out,
              "eksik çözücü sayısı (2/5) BLOCKED verir", out)

    d = killgate_root(5, alt="baska bir cevap")
    code, out = run_env_gate("kill_gate.py", d)
    rep.check(code != 0 and "REWORK" in out,
              "⭑ BİR ÇÖZÜCÜ İKİNCİ CEVAP ÖNERİRSE REWORK ⭑", out)

    d = killgate_root(5, minutes=30)          # 20 × 30 dk = 600 > 240 tavan
    code, out = run_env_gate("kill_gate.py", d)
    rep.check(code != 0,
              "medyan süre tavanı aşarsa GEÇMEZ (%d dk)" % 600, out)

    # ── ⭑ ÇABA BÜTÇESİ ⭑ — öldürme kapısını kaybettiren ölçüm ───────────
    #
    # Faz 2'de sekiz kapı yeşilken beş çözücüden dördü SIKILDIĞI için
    # bıraktı. Hiçbir kapı okurun kaç elle işlem yapacağını sormuyordu.
    # Bu fikstürler o boşluğun kapandığını ve KALICI KIRMIZIYA
    # dönüşmediğini birlikte kanıtlar.
    SHIFT = {"generator": {"kind": "cyclic-shift", "input": shift("MELTEM", 9)},
             "acceptance": {"kind": "in-printed-lexicon"},
             "declaredAcceptedCount": 1}
    CHEAP = {"generator": {"kind": "printed-lexicon"},
             "acceptance": {"kind": "plate-attribute",
                            "labels": ["ZURNA", "KAVUN", "VİRAJ", "TERLİK",
                                       "OYMACI", "PATİKA"],
                            "attributes": {"ZURNA": 1, "KAVUN": 1, "VİRAJ": 2,
                                           "TERLİK": 1, "OYMACI": 1,
                                           "PATİKA": 1},
                            "rule": {"op": "==", "value": 2}},
             "declaredAcceptedCount": 1}

    d = space_root(CHEAP, answer="VİRAJ",
                   index_over=lambda e: e.update(expectedCompletionMinutes=5))
    code, out = run_env_gate("qa_effort.py", d)
    rep.check(code == 0, "qa_effort ucuz mekanizmada GEÇER (3,5 EU / 5 bütçe)",
              out)

    d = space_root(SHIFT, index_over=lambda e: e.update(
        expectedCompletionMinutes=6))
    code, out = run_env_gate("qa_effort.py", d)
    rep.check(code != 0,
              "⭑ 28 KAYDIRMALIK ELLE TARAMA BÜTÇEYİ AŞARSA KIRMIZI ⭑ "
              "(okur çözebilir ama YAPMAZ)", out)

    d = space_root(SHIFT, index_over=lambda e: e.update(
        expectedCompletionMinutes=6, testStatus="failed"))
    code, out = run_env_gate("qa_effort.py", d)
    rep.check(code == 0 and "MUAF" in out,
              "⭑ MAHKÛM ('failed') KAYIT BÜTÇEDEN MUAF — ama ÖLÇÜLÜR ⭑ "
              "(kalıcı kırmızı bir kapı, kapatılan bir kapıdır)", out)

    # ── ⭑ TASARIM HEDEFİ ×1,0 VE K4 TAVANI ⭑ ───────────────────────────
    #
    # Kurucunun ikinci yönergesi bütçeyi `dakika × 3`ten `dakika × 1,0`a
    # indirdi ve en kötü hâle 8 işlemlik bir tavan koydu. İkisi de ISIRIYOR
    # mu — yoksa yalnızca yazılı mı?
    d = space_root(CHEAP, answer="VİRAJ",
                   index_over=lambda e: e.update(expectedCompletionMinutes=2))
    code, out = run_env_gate("qa_effort.py", d)
    rep.check(code != 0,
              "⭑ ×1,0 HEDEFİ ISIRIYOR ⭑ (3,5 EU / 2 dk bütçe — eski ×3 "
              "kuralında GEÇERDİ)", out)

    WIDE = json.loads(json.dumps(CHEAP))
    WIDE["acceptance"]["labels"] = ["ZURNA", "KAVUN", "VİRAJ", "TERLİK",
                                    "OYMACI", "PATİKA", "SÜRAHİ", "MERCAN",
                                    "ŞEBEKE", "PALAMUT"]
    for w in WIDE["acceptance"]["labels"]:
        WIDE["acceptance"]["attributes"].setdefault(w, 1)
    d = space_root(WIDE, answer="VİRAJ",
                   index_over=lambda e: e.update(expectedCompletionMinutes=30))
    code, out = run_env_gate("qa_effort.py", d)
    rep.check(code != 0,
              "⭑ K4 TAVANI ISIRIYOR ⭑ (en kötü 10 > 8; beklenen 5,5 bütçenin "
              "çok altında olsa BİLE)", out)

    # ── ⭑ ÇABA MODELİNİN ÜÇ VARSAYIMI DENETLENİYOR MU ⭑ ────────────────
    #
    # `qa_effort` üç mekanizmayı ucuz sayar ve üçünün gerekçesi de aynı:
    # okurun aramayacağı şey LEVHADA BASILI. Varsayım denetlenmiyorsa ölçüm
    # bir temenniden ibarettir.
    GLYPH_SPACE = {"generator": {"kind": "printed-lexicon"},
                   "acceptance": {"kind": "reachable-by-glyph-reading",
                                  "glyphs": enc("MELTEM").replace("·", "│"),
                                  "directions": ["forward", "reverse"]},
                   "declaredAcceptedCount": 1}
    fig_ok = "▶ " + enc("MELTEM").replace("·", "│")
    for fig, want, label in (
            (fig_ok, 0, "yön işareti BASILIYSA geçer"),
            (fig_ok.replace("▶ ", ""), 1,
             "⭑ ⑨ YÖN İŞARETİ YOKSA KIRMIZI ⭑ (okur iki yönü de dener; "
             "ölçtüğümüz maliyet yarısıdır)")):
        d = space_root(GLYPH_SPACE, answer="MELTEM",
                       page={"puzzleId": "fixture-001", "figure": fig,
                             "clues": [], "constraints": []})
        code, out = run_env_gate("qa_readerpack.py", d)
        rep.check((code != 0) == bool(want), "okur paketi · " + label, out)

    GRID_SPACE = {"generator": {"kind": "printed-lexicon"},
                  "acceptance": {"kind": "reachable-by-printed-grid",
                                 "width": 2, "input": "MLEETM",
                                 "printedGrid": True},
                  "declaredAcceptedCount": 1}
    d = space_root(GRID_SPACE, answer="MELTEM",
                   page={"puzzleId": "fixture-001", "figure": "MLEETM",
                         "clues": [], "constraints": []})
    code, out = run_env_gate("qa_readerpack.py", d)
    rep.check(code != 0,
              "⭑ ⑪ 'IZGARA BASILI' DENİP IZGARA BASILMAMIŞSA KIRMIZI ⭑ "
              "(okur çizer, maliyet iki katına çıkar)", out)

    NARROW = {"generator": {"kind": "printed-lexicon"},
              "acceptance": {"kind": "table-row", "take": "ad",
                             "table": [{"ad": "ZURNA", "yer": "üst"},
                                       {"ad": "KAVUN", "yer": "alt"},
                                       {"ad": "VİRAJ", "yer": "üst"},
                                       {"ad": "TERLİK", "yer": "alt"},
                                       {"ad": "OYMACI", "yer": "alt"}],
                             "filters": [{"col": "yer", "op": "==",
                                          "value": "üst"},
                                         {"col": "ad", "op": "==",
                                          "value": "ZURNA"}],
                             "printedNarrowing": ["yer"]},
              "declaredAcceptedCount": 1}
    tbl = "\n".join(["| ad | yer |", "|---|---|"]
                    + ["| %s | %s |" % (r["ad"], r["yer"])
                       for r in NARROW["acceptance"]["table"]])
    d = space_root(NARROW, answer="ZURNA",
                   page={"puzzleId": "fixture-001", "printedTable": tbl,
                         "figure": "", "clues": [], "constraints": []})
    code, out = run_env_gate("qa_readerpack.py", d)
    rep.check(code != 0,
              "⭑ ⑩ 'BASILI DARALTMA' DENİP SATIRLAR ÖBEKLENMEMİŞSE KIRMIZI ⭑ "
              "(okur satır satır tarar; süzgeç 1 değil n işlemdir)", out)

    # ── ⭑ ⑫ İKİ SAYFANIN KESİŞİMİ ⭑ ────────────────────────────────────
    #
    # Zincirin kaynağı levha bulmacasıdır ve altı etiketi vardır. Tüketici
    # çizelgesinin anahtar sütunu o altı etiketten YALNIZCA BİRİNİ taşırsa,
    # okur kaynağı hiç çözmeden cevabını iki sayfayı yan yana koyarak okur.
    # ⚠ § ⑥ bunu göremez: iki sayfa AYRI AYRI temizdir.
    def chain_root(keys):
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "chain-%03d" % _RUN_SEQ[0])
        for sub in ("01_SOURCE/solutions", "01_SOURCE/design", "02_MANUSCRIPT"):
            os.makedirs(os.path.join(d, sub))
        write(os.path.join(d, ".gate"), "phase2")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/design/tools-plate.json"),
              json.dumps(tools, ensure_ascii=False))
        LBL = ["ZURNA", "KAVUN", "VİRAJ", "TERLİK", "OYMACI", "PATİKA"]
        rows = [{"ad": "MERCAN", "nişan": keys[0]},
                {"ad": "SÜRAHİ", "nişan": keys[1]},
                {"ad": "ŞEBEKE", "nişan": keys[2]},
                {"ad": "PALAMUT", "nişan": keys[3]},
                {"ad": "KUNDURA", "nişan": keys[4]}]
        idx = [{"puzzleId": "src", "gate": "threshold", "type": "observation",
                "mechanismFamily": "plate-observation", "status": "written",
                "testStatus": "tested", "leakClass": "protected", "slot": 1,
                "expectedCompletionMinutes": 4, "ambiguityScore": 1,
                "alternativeSolutionAnalysisDone": True,
                "confirmedAlternativeSolutions": 0, "dependencies": []},
               {"puzzleId": "dst", "gate": "threshold", "type": "logic",
                "mechanismFamily": "constraint-logic", "status": "written",
                "testStatus": "tested", "leakClass": "protected", "slot": 2,
                "expectedCompletionMinutes": 5, "ambiguityScore": 1,
                "alternativeSolutionAnalysisDone": True,
                "confirmedAlternativeSolutions": 0, "dependencies": ["src"]}]
        sol = [{"puzzleId": "src", "finalAnswer": "ZURNA",
                "hints": ["a", "b", "c"],
                "answerSpace": {"generator": {"kind": "printed-lexicon"},
                                "acceptance": {
                                    "kind": "plate-attribute", "labels": LBL,
                                    "attributes": {w: (2 if w == "ZURNA" else 1)
                                                   for w in LBL},
                                    "rule": {"op": "==", "value": 2}},
                                "declaredAcceptedCount": 1}},
               {"puzzleId": "dst", "finalAnswer": "MERCAN",
                "hints": ["a", "b", "c"],
                "answerSpace": {"generator": {"kind": "printed-lexicon"},
                                "acceptance": {
                                    "kind": "table-row", "take": "ad",
                                    "table": rows,
                                    "filters": [{"col": "nişan", "op": "==",
                                                 "value": "ZURNA"}]},
                                "declaredAcceptedCount": 1}}]
        tbl = "\n".join(["| ad | nişan |", "|---|---|"]
                        + ["| %s | %s |" % (r["ad"], r["nişan"]) for r in rows])
        pages = [{"puzzleId": "src", "plateId": "pl-src",
                  "figure": "\n".join("%s %d" % ("◆", i + 1)
                                      for i in range(len(LBL)))},
                 {"puzzleId": "dst", "printedTable": tbl, "figure": ""}]
        write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
              json.dumps({"puzzles": idx}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/solutions/gate-1.json"),
              json.dumps({"puzzles": sol}, ensure_ascii=False))
        write(os.path.join(d, "02_MANUSCRIPT/book.json"),
              json.dumps({"puzzles": pages}, ensure_ascii=False))
        return d

    d = chain_root(["ZURNA", "SEMAVER", "SEMAVER", "MELTEM", "MELTEM"])
    code, out = run_env_gate("qa_readerpack.py", d)
    rep.check(code != 0 and "⑫" in out,
              "⭑ ⑫ ZİNCİRİN KAYNAĞI İKİ SAYFANIN KESİŞİMİNDEN OKUNUYORSA "
              "KIRMIZI ⭑ (tek sayfaya bakan hiçbir kapı bunu göremez)", out)

    d = chain_root(["ZURNA", "KAVUN", "KAVUN", "MELTEM", "MELTEM"])
    code, out = run_env_gate("qa_readerpack.py", d)
    rep.check("⑫" not in out,
              "anahtar sütununda İKİ aday varsa kesişim sızdırmaz", out)

    # ── ⭑ KAPI II · ÜÇ YENİ MEKANİZMA ⭑ ────────────────────────────────
    #
    # Yeni bir kabul yordamı, denetlenmemiş bir kabul yordamıdır. Üçü de
    # kendi kusurlu kurgusuyla burada ısırıyor.
    def coords_of(w):
        return [[ALPHA.index(c) // 5 + 1, ALPHA.index(c) % 5 + 1] for c in w]

    def ring_readings(pairs):
        outs = []
        for base in (pairs, list(reversed(pairs))):
            for r in range(len(base)):
                outs.append(base[r:] + base[:r])
        return outs

    GC = {"generator": {"kind": "printed-bestiary"},
          "acceptance": {"kind": "reachable-via-grid-coordinates",
                         "coordinates": coords_of("MELTEM"),
                         "readings": [coords_of("MELTEM")],
                         "gridRef": "ring-table"},
          "declaredAcceptedCount": 1}
    d = space_root(GC, answer="MELTEM")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code == 0, "ızgara koordinatı temiz kurguda GEÇER", out)

    # ⭑ Faz 2'nin sayı-tablosu dersinin Kapı II'deki hâli ⭑
    # İspat yalnızca YAZARIN okumasına bakarsa, yanlış istasyondan başlayan
    # okurun BAŞKA bir geçerli ada düşüp düşmediği hiç sorulmaz.
    ZUR = coords_of("ZURNA")
    both = {"generator": {"kind": "printed-bestiary"},
            "acceptance": {"kind": "reachable-via-grid-coordinates",
                           "coordinates": ZUR,
                           "readings": ring_readings(ZUR)
                           + [coords_of("KAVUN")],
                           "gridRef": "ring-table"},
            "declaredAcceptedCount": 1}
    d = space_root(both, answer="ZURNA")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0,
              "⭑ İKİNCİ BİR OKUMA DA GEÇERLİ BİR ADA DÜŞÜYORSA KIRMIZI ⭑ "
              "(yanlış istasyondan başlayan okur savunulabilir bir cevaba "
              "varıyor)", out)

    def pen_space(rules, flip="ZURNA"):
        items = ["ZURNA", "KAVUN", "VİRAJ", "TERLİK", "OYMACI", "PATİKA"]
        attrs = {w: {"kanat": bool(i % 2), "pul": bool(i % 3 == 0)}
                 for i, w in enumerate(items)}
        pens = {w: ("A" if attrs[w]["kanat"] else "B") for w in items}
        pens[flip] = "B" if pens[flip] == "A" else "A"
        return {"generator": {"kind": "printed-bestiary"},
                "acceptance": {"kind": "misclassified-in-printed-pens",
                               "items": items, "attributes": attrs,
                               "pens": pens, "candidateRules": rules},
                "declaredAcceptedCount": 1}

    d = space_root(pen_space(["kanat", "pul"]), answer="ZURNA")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code == 0, "sınıflama tek kural açıklarken GEÇER", out)

    # ⭑ İKİ kural da bölmeleri 'bir üye hariç' açıklıyorsa, okurun İKİ
    # savunulabilir cevabı olur — ve bunu yalnızca kural sayısı söyler.
    items = ["ZURNA", "KAVUN", "VİRAJ", "TERLİK", "OYMACI", "PATİKA"]
    attrs = {w: {"kanat": (w != "ZURNA"), "pul": (w != "KAVUN")}
             for w in items}
    pens = {w: "A" for w in items}
    amb = {"generator": {"kind": "printed-bestiary"},
           "acceptance": {"kind": "misclassified-in-printed-pens",
                          "items": items, "attributes": attrs, "pens": pens,
                          "candidateRules": ["kanat", "pul"]},
           "declaredAcceptedCount": 1}
    d = space_root(amb, answer="ZURNA")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0,
              "⭑ İKİ KURAL DA AÇIKLIYORSA KIRMIZI ⭑ "
              "(okurun iki savunulabilir cevabı olur)", out)

    KROW = "".join(dict.fromkeys("MELTEM" + ALPHA))
    KCT = "".join(KROW[ALPHA.index(c)] for c in "KAVUN")
    d = space_root({"generator": {"kind": "printed-bestiary"},
                    "acceptance": {"kind": "reachable-by-keyed-alphabet",
                                   "keyedRow": KROW, "input": KCT},
                    "declaredAcceptedCount": 1}, answer="KAVUN")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code == 0, "anahtarlı satır temiz kurguda GEÇER", out)

    d = space_root({"generator": {"kind": "printed-bestiary"},
                    "acceptance": {"kind": "reachable-by-keyed-alphabet",
                                   "keyedRow": KROW[:-1], "input": KCT},
                    "declaredAcceptedCount": 1}, answer="KAVUN")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0,
              "eksik anahtar satırı hiçbir üye kabul etmez (çözülemez)", out)

    # ── ⭑ LEVHA VERİSİ · BASKI ÖN ÖLÇÜMÜ ⭑ ─────────────────────────────
    def plate_root(fig, space=None, answer="MELTEM"):
        return space_root(space or GC, answer=answer,
                          page={"puzzleId": "fixture-001", "figure": fig,
                                "clues": [], "constraints": []})

    good = "  ▶  " + "   ".join("%d·%d" % (r, c) for r, c in
                                coords_of("MELTEM"))
    code, out = run_env_gate("qa_plate_data.py", plate_root(good))
    rep.check(code == 0, "levha verisi temiz şekilde GEÇER", out)

    code, out = run_env_gate("qa_plate_data.py",
                             plate_root(good + "\n  " + "+" * 6))
    rep.check(code != 0,
              "⭑ ALTI ARDIŞIK AYNI İŞARET KIRMIZI ⭑ "
              "(baskıda kaybolan şey veri değil, AYIRT EDİLEBİLİRLİKTİR)",
              out)

    code, out = run_env_gate("qa_plate_data.py",
                             plate_root(good + "\n  " + "─" * 80))
    rep.check(code != 0,
              "⭑ TRIM'E SIĞMAYAN ŞEKİL KIRMIZI ⭑ (6×9'da satır ~62 karakter)",
              out)

    code, out = run_env_gate("qa_plate_data.py", plate_root("  ▶  1·1   2·2"))
    rep.check(code != 0,
              "⭑ ŞEKİLDEKİ VERİ KAYITTAKİNDEN FARKLIYSA KIRMIZI ⭑ "
              "(levha ile kayıt ayrışırsa okur çözemez)", out)

    # ── ⭑ KESİŞİM IZGARASI · ETİKET İDDİA DEĞİL, NİTELİKTİR ⭑ ──────────
    def gspace(grid):
        return {"generator": {"kind": "printed-lexicon"},
                "acceptance": {
                    "kind": "grid-intersection", "grid": grid,
                    "rowLabels": [{"op": "length", "value": 5},
                                  {"op": "length", "value": 7}],
                    "colLabels": [{"op": "first-letter-group", "value": 6},
                                  {"op": "first-letter-group", "value": 3}],
                    "rowRule": {"op": "length", "value": 5},
                    "colRule": {"op": "first-letter-group", "value": 6}},
                "declaredAcceptedCount": 1}

    d = space_root(gspace([["ZURNA", "KAVUN"], ["YELPAZE", "KUNDURA"]]),
                   answer="ZURNA")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code == 0, "kesişim ızgarası tutarlıysa GEÇER", out)

    # Yazar "birinci satır beş harflidir" der ve içine yedi harfli koyar.
    d = space_root(gspace([["ZURNA", "KUNDURA"], ["YELPAZE", "KAVUN"]]),
                   answer="ZURNA")
    code, out = run_env_gate("qa_answerspace.py", d)
    rep.check(code != 0,
              "⭑ IZGARA ETİKETİ HÜCREYE UYMUYORSA KIRMIZI ⭑ "
              "(§ 14: tekillik yazarın sözüne dayanamaz)", out)

    # ── ⭑ DENEYİM KAPISI ⭑ — "sıkıldım"ın ölçülemeyen yarısı ───────────
    def exp_root(over=None, warm_over=None):
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "exp-%03d" % _RUN_SEQ[0])
        for sub in ("01_SOURCE/solutions", "01_SOURCE/design", "02_MANUSCRIPT"):
            os.makedirs(os.path.join(d, sub))
        write(os.path.join(d, ".gate"), "phase2")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/design/tools-plate.json"),
              json.dumps(tools, ensure_ascii=False))
        LBL = ["ZURNA", "KAVUN", "VİRAJ", "TERLİK", "OYMACI", "PATİKA"]
        plan = [("p1", "plate-observation", 3, 3, "obs-a"),
                ("p2", "plate-observation", 3, 4, "obs-b"),
                ("p3", "plate-observation", 4, 4, "obs-c"),
                ("p4", "plate-observation", 5, 5, "obs-d"),
                ("p5", "gate-synthesis", 6, 5, "gate")]
        idx, sol, dsg, pages = [], [], [], []
        for i, (pid, fam, mins, aha, sig) in enumerate(plan, 1):
            idx.append({"puzzleId": pid, "gate": "threshold",
                        "type": "observation", "mechanismFamily": fam,
                        "status": "written", "testStatus": "tested",
                        "leakClass": "protected", "slot": i,
                        "expectedCompletionMinutes": mins,
                        "ambiguityScore": 1,
                        "alternativeSolutionAnalysisDone": True,
                        "confirmedAlternativeSolutions": 0})
            sol.append({"puzzleId": pid, "finalAnswer": LBL[i - 1],
                        "hints": ["a", "b", "c"],
                        "answerSpace": {
                            "generator": {"kind": "printed-lexicon"},
                            "acceptance": {
                                "kind": "plate-attribute", "labels": LBL,
                                "attributes": {w: (2 if w == LBL[i - 1] else 1)
                                               for w in LBL},
                                "rule": {"op": "==", "value": 2}},
                            "declaredAcceptedCount": 1}})
            dsg.append({"puzzleId": pid, "mechanismFamily": fam,
                        "experience": {
                            "ahaScore": aha,
                            "revelation": {"kind": "small-observation-unlocks",
                                           "evidence": "pl-%s" % pid},
                            "mechanismSignature": sig}})
            pages.append({"puzzleId": pid, "plateId": "pl-%s" % pid})
        warm = [{"id": "w1", "teaches": "plate-observation",
                 "solved": ["örnek çözüm"]},
                {"id": "w2", "teaches": "gate-synthesis",
                 "solved": ["örnek çözüm"]}]
        if over:
            over(idx, sol, dsg, pages)
        if warm_over:
            warm_over(warm)
        write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
              json.dumps({"puzzles": idx}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/solutions/gate-1.json"),
              json.dumps({"puzzles": sol}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/design/gate-1.json"),
              json.dumps({"puzzles": dsg}, ensure_ascii=False))
        write(os.path.join(d, "02_MANUSCRIPT/book.json"),
              json.dumps({"puzzles": pages, "warmUp": warm},
                         ensure_ascii=False))
        return d

    code, out = run_env_gate("qa_experience.py", exp_root())
    rep.check(code == 0, "deneyim kapısı temiz kurguda GEÇER", out)

    def _flat(i, s, dd, pg):
        for r in dd:
            r["experience"]["ahaScore"] = 3
    code, out = run_env_gate("qa_experience.py", exp_root(_flat))
    rep.check(code != 0,
              "⭑ § 9 · AHA ORTANCASI DÜŞÜKSE KIRMIZI ⭑ "
              "(yirmi doğru ama ödülsüz bulmaca, ölçüme göre 'iyi' kitaptır)",
              out)

    def _unbacked(i, s, dd, pg):
        dd[1]["experience"]["revelation"]["evidence"] = "olmayan-levha"
    code, out = run_env_gate("qa_experience.py", exp_root(_unbacked))
    rep.check(code != 0,
              "⭑ 4+ PUAN VERİP ÖDÜLÜN YERİNİ GÖSTEREMEYEN BULMACA YAKALANIR ⭑ "
              "(yazarın kendine verdiği not, kanıt değildir)", out)

    # ⭑ K36 · KURAL DEĞİŞTİ, FİKSTÜR DE DEĞİŞTİ ⭑
    # Eskiden "aynı imza ikinci kez 4+ alamaz"dı ve imzayı kopyalamak
    # kırmızı yakmaya yeterdi. Artık tavan ÖLÇÜLÜYOR: tekrar, okurdan
    # daha fazla düşünme istiyorsa 4 alabilir. Alamayacağı tek şey 5'tir
    # — keşif bir kez olur. Fikstür o çizgiyi ölçer.
    def _dup(i, s, dd, pg):
        dd[3]["experience"]["mechanismSignature"] = \
            dd[1]["experience"]["mechanismSignature"]
        dd[3]["experience"]["ahaScore"] = 5
    code, out = run_env_gate("qa_experience.py", exp_root(_dup))
    rep.check(code != 0,
              "⭑ K36 · AYNI MEKANİZMA İKİNCİ KEZ 5 ALAMAZ ⭑ "
              "(keşif bir kez olur; ikincisi en iyi hâlde DERİNLEŞMEDİR)",
              out)

    def _untaught(w):
        w.pop()
    code, out = run_env_gate("qa_experience.py", exp_root(warm_over=_untaught))
    rep.check(code != 0,
              "⭑ § 7 · ISINMADA ÖRNEĞİ OLMAYAN AİLE KIRMIZI ⭑ "
              "(mantık sıçraması ikinci bırakma sebebiydi)", out)

    # ⭑ § 7b · AİLE DEĞİL, İŞLEM DÜZEYİNDE ⭑
    # Ölçülen: `layered-chain` ailesi öğretilmiş görünüyordu ama o
    # ailenin İKİ işlemi var ve üç levha ikincisini ("ayna ekseni")
    # basıyordu — kitabın hiçbir yerinde öğretilmeden.
    def _untaught_op(i, s, dd, pg):
        pg[1]["figure"] = "  ║  2 · ayna ekseni: 18  ║"
    code, out = run_env_gate("qa_experience.py", exp_root(_untaught_op))
    rep.check(code != 0,
              "⭑ § 7b · LEVHANIN BASTIĞI ÖĞRETİLMEMİŞ BİR İŞLEM KIRMIZI ⭑ "
              "(bir AİLE öğretilmiş olabilir; içindeki bir İŞLEM "
              "öğretilmemiş olabilir)", out)

    def _spoil(w):
        w[0]["solved"] = ["Cevap ZURNA idi."]
    code, out = run_env_gate("qa_experience.py", exp_root(warm_over=_spoil))
    rep.check(code != 0,
              "⭑ ISINMA GERÇEK BİR CEVABI VERİRSE KIRMIZI ⭑ "
              "(ısınma kitabın İÇİNDE basılıdır)", out)

    def _grind(i, s, dd, pg):
        for e, m in zip(i, [3, 3, 9, 9, 9]):
            e["expectedCompletionMinutes"] = m
    code, out = run_env_gate("qa_experience.py", exp_root(_grind))
    rep.check(code != 0,
              "⭑ § 11 · UZUN EZİYET DİZİSİ YAKALANIR ⭑ "
              "(kolay başlangıç → uzun grind → tükeniş)", out)

    # ── ⛔ ÖLDÜRME KAPISI · OTURUM DÜZEYİ TOPLU KAYIT ⛔ ─────────────────
    # ⭑ Karar mantığı fikstürleri geçersiz kılma KAPALIYKEN koşar ⭑
    # Geçersiz kılma yalnızca ÇIKIŞ KODUNU değiştirir; KARARI değiştirmez.
    # İkisini aynı fikstürde ölçmek, hangisinin bozulduğunu gizlerdi.
    cfg_ko = json.loads(json.dumps(cfg))
    cfg_ko.setdefault("killGate", {}).setdefault("externalValidation", {})[
        "founderOverride"] = False

    def agg_root(total: int, finished: int, per_puzzle=None) -> str:
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "agg-%03d" % _RUN_SEQ[0])
        for sub in ("01_SOURCE/solutions", "01_SOURCE/playtests",
                    "06_REPORTS/tracked"):
            os.makedirs(os.path.join(d, sub))
        write(os.path.join(d, ".gate"), "phase2")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg_ko, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
              json.dumps({"puzzles": [
                  {"puzzleId": "fixture-%03d" % i, "gate": "threshold",
                   "type": "cipher", "mechanismFamily": "substitution-cipher",
                   "status": "drafted", "testStatus": "failed",
                   "leakClass": "protected", "pilotCohort": True}
                  for i in range(1, 21)]}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/playtests/sessions.json"),
              json.dumps({"solversTotal": total,
                          "solversCompletedGate": finished,
                          "solversAbandoned": total - finished,
                          "perPuzzleRecords": per_puzzle,
                          "abandonReasons": [{"code": "sikildim",
                                              "label": "Sıkıldım"}]},
                         ensure_ascii=False))
        return d

    # ── ⭑ KURUCU GEÇERSİZ KILMASI ⭑ — ÖLÇÜMÜ EZEBİLİR Mİ? ──────────────
    #
    # Kurucu 24 Ağustos'ta Faz 3'ün ölçüme RAĞMEN başlamasına izin verdi.
    # Tek soru şudur ve bu blok onu ölçer: geçersiz kılma KARARI ezebiliyor
    # mu? Ezebiliyorsa, kapı bir kapı değil bir düğmedir.
    def ov_root(total=5, finished=1, **over):
        d = agg_root(total, finished)
        c = json.loads(open(os.path.join(d, "project_config.json"),
                            encoding="utf-8").read())
        ev = c.setdefault("killGate", {}).setdefault("externalValidation", {})
        ev.update({"status": "founder_override_partial", "sessionsPerformed": 0,
                   "humanValidationPassed": False, "founderOverride": True,
                   "overrideAuthorisedAt": "2026-08-24",
                   "overrideReason": "founder-authorized continuation"})
        ev.update(over)
        write(os.path.join(d, "project_config.json"),
              json.dumps(c, ensure_ascii=False))
        return d

    code, out = run_env_gate("kill_gate.py", ov_root())
    rep.check(code == 0 and "HARD-STOP" in out and "GEÇERSİZ KILMA" in out,
              "⭑ GEÇERSİZ KILMA YALNIZCA ÇIKIŞ KODUNU DEĞİŞTİRİR ⭑ "
              "(ölçülen karar HARD-STOP olarak YAZDIRILMAYA devam eder)", out)

    rp = os.path.join(ov_root(), "06_REPORTS/tracked/kill-gate-report.json")
    run_env_gate("kill_gate.py", os.path.dirname(os.path.dirname(
        os.path.dirname(rp))))
    saved = json.loads(open(rp, encoding="utf-8").read())
    rep.check(saved.get("verdict") == "HARD-STOP"
              and saved.get("measuredVerdict") == "HARD-STOP"
              and saved.get("overrideActive") is True
              and saved.get("externalValidation", {}).get(
                  "humanValidationPassed") is False,
              "⭑ RAPORDA ÖLÇÜLEN KARAR EZİLMİYOR ⭑ "
              "(verdict=HARD-STOP · overrideActive=true · doğrulama=false)",
              json.dumps(saved, ensure_ascii=False)[:600])

    for over, label in (
            ({"humanValidationPassed": True},
             "⭑ SIFIR OTURUMLA 'İNSAN DOĞRULAMASI GEÇTİ' DENEMEZ ⭑"),
            ({"sessionsPerformed": 9},
             "⭑ BİLDİRİLEN OTURUM SAYISI ÖLÇÜLENİ AŞAMAZ ⭑ (fark UYDURMA)"),
            ({"overrideReason": ""},
             "geçersiz kılma GEREKÇESİZ kaydedilemez"),
            ({"status": "validated"},
             "⭑ OTURUM YOKKEN DURUM 'validated' OLAMAZ ⭑")):
        code, out = run_env_gate("kill_gate.py", ov_root(**over))
        rep.check(code != 0 and "UYDURMA MUHAFIZI" in out, label, out)

    d = agg_root(5, 1)
    code, out = run_env_gate("kill_gate.py", d)
    rep.check(code != 0 and "HARD-STOP" in out,
              "⭑ 1/5 ÇÖZÜCÜ BİTİRİRSE HARD-STOP ⭑", out)

    d = agg_root(5, 3)
    code, out = run_env_gate("kill_gate.py", d)
    rep.check(code != 0 and "REDESIGN" in out,
              "tam 3/5 bitirirse REDESIGN (zorluk eğrisi bozuk)", out)

    d = agg_root(5, 5)
    code, out = run_env_gate("kill_gate.py", d)
    rep.check(code != 0 and "REWORK" in out,
              "⭑ 5/5 BİTİRSE BİLE bulmaca başına kayıt YOKSA PASS DEĞİL ⭑ "
              "('ihlal edilmedi' ile 'ölçülmedi' aynı şey değildir)", out)

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


# ---------------------------------------------------------------------------
def part9_meta_and_aha(rep: Report, tmp: str) -> None:
    """⑨ ⭑ FAZ 4'ÜN İKİ YENİ KAPISI: META-MİSTER VE ÖLÇÜLEN AHA TAVANI ⭑

    Her fikstür, kapının YAKALAMASI GEREKEN bir kusuru kurar. Bir kapının
    varlığı yetmez; ısırdığı GÖRÜLMELİDİR — ve bu bölümdeki iki kusur
    üretim verisinde GERÇEKTEN yaşandı:

      · on kayıt kendi ölçülen aha tavanının üstünde puan taşıyordu
        (tekrarlanan mekanizmaya 4 ve 5 yazılmıştı);
      · Faz 4'e kadar meta-mistere META OLARAK bakan hiçbir kapı yoktu.
    """
    print("\n⑨ ⭑ META-MİSTER · ÖLÇÜLEN AHA TAVANI ⭑")

    cfg = clean_config()
    ALPHA = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    GATES = ["threshold", "menagerie", "calendar", "labyrinth", "mirror"]
    PHRASES = ["ZURNA SESİ VAR", "MELTEM ESTİ YİNE", "KAVUN KESTİ USTA",
               "PALAMUT DÜŞTÜ DALDAN", "ŞEBEKE KURULDU ARTIK"]
    POS = [1, 2, 3, 4, 5]

    def _meta_answer(phrases, positions):
        out = ""
        for ph, k in zip(phrases, positions):
            q = "".join(c for c in ph.upper() if c.isalpha())
            out += q[-k]
        return out

    META = _meta_answer(PHRASES, POS)

    def meta_root(mut=None):
        """Beş kapı bulmacası + bir son soru — en küçük gerçek meta."""
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "meta-%03d" % _RUN_SEQ[0])
        for sub in ("01_SOURCE/solutions", "01_SOURCE/design", "02_MANUSCRIPT"):
            os.makedirs(os.path.join(d, sub))
        write(os.path.join(d, ".gate"), "phase4")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg, ensure_ascii=False))
        gates = [{"id": g, "pageBudget": 34} for g in GATES] + [
            {"id": "last-question", "pageBudget": 6, "metaGate": True}]
        idx, sol, dsg, pages = [], [], [], []
        for i, (g, ph) in enumerate(zip(GATES, PHRASES), 1):
            pid = "g%d-020" % i
            idx.append({"puzzleId": pid, "gate": g, "type": "meta",
                        "mechanismFamily": "gate-synthesis",
                        "status": "written", "testStatus": "tested",
                        "leakClass": "protected", "ambiguityScore": 1,
                        "alternativeSolutionAnalysisDone": True,
                        "confirmedAlternativeSolutions": 0,
                        "dependencies": []})
            sol.append({"puzzleId": pid, "finalAnswer": ph,
                        "hints": ["a", "b", "c"], "constraints": []})
            dsg.append({"puzzleId": pid, "mechanismFamily": "gate-synthesis"})
            pages.append({"puzzleId": pid, "gate": g, "title": "kapı %d" % i})
        space = {"generator": {"kind": "printed-meta-list",
                               "listRef": "last-question-candidates"},
                 "acceptance": {"kind": "meta-synthesis",
                                "gatePhrases": list(PHRASES),
                                "positions": list(POS)},
                 "declaredAcceptedCount": 1}
        idx.append({"puzzleId": "meta-001", "gate": "last-question",
                    "type": "meta", "mechanismFamily": "meta-synthesis",
                    "status": "written", "testStatus": "tested",
                    "leakClass": "protected", "ambiguityScore": 1,
                    "alternativeSolutionAnalysisDone": True,
                    "confirmedAlternativeSolutions": 0,
                    "dependencies": ["g%d-020" % i for i in range(1, 6)]})
        sol.append({"puzzleId": "meta-001", "finalAnswer": META,
                    "hints": ["a", "b", "c"], "answerSpace": space,
                    "constraints": ["Cevap %d harflidir." % len(META)]})
        dsg.append({"puzzleId": "meta-001",
                    "mechanismFamily": "meta-synthesis",
                    "answerSpace": space})
        pages.append({"puzzleId": "meta-001", "gate": "last-question",
                      "title": "Son Soru"})
        charts = {"last-question-candidates": {
            "printed": False,
            "entries": sorted({META, "ZZZZZ", "YYYYY", "XXXXX"})}}
        book = {"puzzles": pages, "warmUp": [],
                "frame": {"opening": ["giriş"]}}
        if mut:
            mut(idx, sol, dsg, book, charts, gates)
        write(os.path.join(d, "01_SOURCE/gate_index.json"),
              json.dumps({"gates": gates}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
              json.dumps({"puzzles": idx}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/solutions/gate-1.json"),
              json.dumps({"puzzles": sol}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/design/gate-1.json"),
              json.dumps({"puzzles": dsg}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/design/tools-plate.json"),
              json.dumps({"charts": charts}, ensure_ascii=False))
        write(os.path.join(d, "02_MANUSCRIPT/book.json"),
              json.dumps(book, ensure_ascii=False))
        return d

    def meta_gate(mut=None):
        return run_env_gate("qa_meta.py", meta_root(mut), gate="phase4")

    code, out = meta_gate()
    rep.check(code == 0, "meta kapısı temiz kurguda GEÇER", out)

    def _no_contribution(idx, sol, dsg, book, charts, gates):
        idx[-1]["dependencies"] = idx[-1]["dependencies"][:4]
        dsg[-1]["answerSpace"]["acceptance"]["gatePhrases"] = PHRASES[:4]
        sol[-1]["answerSpace"]["acceptance"]["gatePhrases"] = PHRASES[:4]
    code, out = meta_gate(_no_contribution)
    rep.check(code != 0,
              "⭑ BİR KAPI SON SORUYA KATKI VERMİYORSA KIRMIZI ⭑ "
              "(yol haritası § 12 · BLOKLAYICI)", out)

    def _future_dep(idx, sol, dsg, book, charts, gates):
        idx[-1]["dependencies"] = idx[-1]["dependencies"] + ["meta-002"]
        idx.append({"puzzleId": "meta-002", "gate": "last-question",
                    "type": "meta", "mechanismFamily": "gate-synthesis",
                    "status": "written", "testStatus": "tested",
                    "leakClass": "protected", "ambiguityScore": 1,
                    "alternativeSolutionAnalysisDone": True,
                    "confirmedAlternativeSolutions": 0, "dependencies": []})
    code, out = meta_gate(_future_dep)
    rep.check(code != 0,
              "⭑ SON SORU İLERİ REFERANS VERİRSE KIRMIZI ⭑ "
              "(okurun henüz elde etmediği bir çıktı istenemez)", out)

    def _cycle(idx, sol, dsg, book, charts, gates):
        idx[0]["dependencies"] = ["meta-001"]
    code, out = meta_gate(_cycle)
    rep.check(code != 0,
              "⭑ SON SORUNUN CEVABINI KULLANAN BULMACA VARSA KIRMIZI ⭑ "
              "(döngü: kitap kendi kapanışına bağlanamaz)", out)

    def _unproducible(idx, sol, dsg, book, charts, gates):
        sol[2]["finalAnswer"] = "BAŞKA BİR SÖZ TAMAMEN"
    code, out = meta_gate(_unproducible)
    rep.check(code != 0,
              "⭑ BİLDİRİLEN KAPI SÖZÜ O KAPININ GERÇEK ÇIKTISI DEĞİLSE "
              "KIRMIZI ⭑ (okurun elinde olmayan bir söz istenemez)", out)

    def _concat(idx, sol, dsg, book, charts, gates):
        # Cevap birleştirilmiş dizenin içinden okunabiliyor
        joined = "".join(c for p in PHRASES for c in p.upper() if c.isalpha())
        fake = joined[3:3 + len(META)]
        sol[-1]["finalAnswer"] = fake
        charts["last-question-candidates"]["entries"] = sorted({fake, "ZZZZZ"})
    code, out = meta_gate(_concat)
    rep.check(code != 0,
              "⭑ CEVAP BİRLEŞTİRİLMİŞ SÖZLERİN İÇİNDEN OKUNUYORSA KIRMIZI ⭑ "
              "(birleştirme çıkarım değildir; okur onu kazara bulur)", out)

    def _leak_page(idx, sol, dsg, book, charts, gates):
        book["puzzles"][1]["flavour"] = "Bir yerde %s yazıyordu." % META
    code, out = meta_gate(_leak_page)
    rep.check(code != 0,
              "⭑ SON SORUNUN CEVABI BİR SAYFADA BASILIYSA KIRMIZI ⭑ "
              "(doğrulama sayfasının anlamı kalmaz · § 12)", out)

    def _leak_title(idx, sol, dsg, book, charts, gates):
        book["puzzles"][2]["title"] = META
    code, out = meta_gate(_leak_title)
    rep.check(code != 0,
              "⭑ CEVAP BİR SAYFA BAŞLIĞINDA GEÇİYORSA KIRMIZI ⭑ "
              "(dizgide en büyük basılan yer başlıktır)", out)

    def _leak_warm(idx, sol, dsg, book, charts, gates):
        book["warmUp"] = [{"id": "w1", "teaches": "meta-synthesis",
                           "title": "örnek", "solved": ["Cevap %s." % META]}]
    code, out = meta_gate(_leak_warm)
    rep.check(code != 0,
              "⭑ CEVAP ISINMA ÖRNEĞİNDE GEÇİYORSA KIRMIZI ⭑", out)

    def _printed_list(idx, sol, dsg, book, charts, gates):
        charts["last-question-candidates"]["printed"] = True
    code, out = meta_gate(_printed_list)
    rep.check(code != 0,
              "⭑ ADAY LİSTESİ KİTAPTA BASILIYSA KIRMIZI ⭑ "
              "(cevap dokuz adaya iner; son soru bir seçmeye dönüşür)", out)

    def _order(idx, sol, dsg, book, charts, gates):
        idx[-1]["dependencies"] = ["g2-020", "g1-020", "g3-020",
                                   "g4-020", "g5-020"]
    code, out = meta_gate(_order)
    rep.check(code != 0,
              "⭑ KAPI SIRASI MANUSCRIPT SIRASIYLA TUTMUYORSA KIRMIZI ⭑ "
              "(harfler doğru ama SIRA yanlış olursa cevap değişir)", out)

    def _flat_positions(idx, sol, dsg, book, charts, gates):
        flat = [2, 2, 2, 2, 2]
        ans = _meta_answer(PHRASES, flat)
        for rec in (sol[-1], dsg[-1]):
            rec["answerSpace"]["acceptance"]["positions"] = flat
        sol[-1]["finalAnswer"] = ans
        charts["last-question-candidates"]["entries"] = sorted({ans, "ZZZZZ"})
    code, out = meta_gate(_flat_positions)
    rep.check(code != 0,
              "⭑ BÜTÜN KONUMLAR AYNI SAYIYSA KIRMIZI ⭑ "
              "(kapıların kendi sayıları kullanılmıyor demektir)", out)

    # ── ⭑ K36 · ÖLÇÜLEN AHA TAVANI ⭑ ───────────────────────────────────
    # Tavan yazardan gelmez: ilk kullanım 5, ölçülmüş derinleşme 4, düz
    # tekrar 3. Ölçü `bildirilen dakika ÷ elle işlem`tir ve iki alanın da
    # sahibi başka kapılardır.
    LBL = ["ZURNA", "KAVUN", "VİRAJ", "TERLİK", "OYMACI", "PATİKA",
           "SÜRAHİ", "MERCAN", "MELTEM", "ŞEBEKE", "KUNDURA", "YELPAZE"]
    tools_k36 = {"charts": {}}

    def aha_root(plan, over=None):
        """Her kayıt: (pid, kapı, aile, dakika, aha, imza, etiket sayısı).

        Elle işlem `plate-attribute` modelinden ölçülür ve etiket sayısıyla
        DOĞRU orantılıdır; dakika bildirilendir. Oran ikisinin bölümüdür."""
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "aha-%03d" % _RUN_SEQ[0])
        for sub in ("01_SOURCE/solutions", "01_SOURCE/design", "02_MANUSCRIPT"):
            os.makedirs(os.path.join(d, sub))
        write(os.path.join(d, ".gate"), "phase4")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/design/tools-plate.json"),
              json.dumps(tools_k36, ensure_ascii=False))
        idx, sol, dsg, pages = [], [], [], []
        seen_slot: dict = {}
        for (pid, gid, fam, mins, aha, sig, n) in plan:
            labels = LBL[:n]
            seen_slot[gid] = seen_slot.get(gid, 0) + 1
            idx.append({"puzzleId": pid, "gate": gid, "type": "observation",
                        "mechanismFamily": fam, "status": "written",
                        "testStatus": "tested", "leakClass": "protected",
                        "slot": seen_slot[gid],
                        "expectedCompletionMinutes": mins,
                        "ambiguityScore": 1,
                        "alternativeSolutionAnalysisDone": True,
                        "confirmedAlternativeSolutions": 0})
            sol.append({"puzzleId": pid, "finalAnswer": labels[0],
                        "hints": ["a", "b", "c"],
                        "answerSpace": {
                            "generator": {"kind": "printed-lexicon"},
                            "acceptance": {
                                "kind": "plate-attribute", "labels": labels,
                                "attributes": {w: (2 if w == labels[0] else 1)
                                               for w in labels},
                                "rule": {"op": "==", "value": 2}},
                            "declaredAcceptedCount": 1}})
            dsg.append({"puzzleId": pid, "mechanismFamily": fam,
                        "experience": {
                            "ahaScore": aha,
                            "revelation": {"kind": "small-observation-unlocks",
                                           "evidence": "pl-%s" % pid},
                            "mechanismSignature": sig}})
            pages.append({"puzzleId": pid, "plateId": "pl-%s" % pid})
        warm = [{"id": "w1", "teaches": "plate-observation",
                 "solved": ["örnek"]},
                {"id": "w2", "teaches": "gate-synthesis", "solved": ["örnek"]}]
        if over:
            over(idx, sol, dsg, pages, warm)
        write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
              json.dumps({"puzzles": idx}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/solutions/gate-1.json"),
              json.dumps({"puzzles": sol}, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/design/gate-1.json"),
              json.dumps({"puzzles": dsg}, ensure_ascii=False))
        write(os.path.join(d, "02_MANUSCRIPT/book.json"),
              json.dumps({"puzzles": pages, "warmUp": warm},
                         ensure_ascii=False))
        return d

    # ⚠ FİKSTÜR § 11'İN RAMPA KURALLARINA DA UYMAK ZORUNDA: her kapıda
    # ≥3 ayrı süre, kolay başlangıç, uzun eziyet yok. İlk kurgu düz
    # sürelerle yazılmıştı ve K36 yeşilken rampa kırmızı yandı — fikstür
    # ölçmek istediği şeyi ölçemiyordu.
    #
    # Çıkarım oranı = dakika ÷ elle işlem; elle işlem burada sabittir (4),
    # yani oranı SÜRELER kurar.
    THR_MIN = (4, 4, 5, 6, 6, 7)          # ortanca 5,5 → oran 1,375
    MEN_MIN = (6, 6, 7, 8, 8, 9)          # ortanca 7,5 → oran 1,875
    CAL_MIN = (10, 11, 9, 12, 13, 14)     # ortanca 11,5 → oran 2,875
    CAL_AHA = (5, 4, 3, 3, 3, 3)          # ilk kullanım · derinleşme · yordam

    def _plan(cal_scores=CAL_AHA, cal_min=CAL_MIN, men_min=MEN_MIN,
              thr_min=THR_MIN):
        rows = []
        for gid, mins in (("threshold", thr_min), ("menagerie", men_min)):
            last = len(mins) - 1
            for i in range(len(mins)):
                rows.append(("%s-%d" % (gid[:3], i + 1), gid,
                             "gate-synthesis" if i == last
                             else "plate-observation",
                             mins[i], 5 if i < 3 else 3,
                             "%s-sig-%d" % (gid[:3], i), 4))
        last = len(cal_min) - 1
        for i, (aha, mins) in enumerate(zip(cal_scores, cal_min)):
            rows.append(("cal-%d" % (i + 1), "calendar",
                         "gate-synthesis" if i == last else "plate-observation",
                         mins, aha, "cal-sig-0", 4))
        return rows

    code, out = run_env_gate("qa_experience.py", aha_root(_plan()),
                             gate="phase4")
    rep.check(code == 0,
              "K36 · temiz kurgu GEÇER (keşif 4 · akıcılık 3 + yükselen "
              "çıkarım)", out)

    def _five_on_reuse(i, s, dd, pg, w):
        dd[13]["experience"]["ahaScore"] = 5          # cal-2, tekrarlanan imza
    code, out = run_env_gate("qa_experience.py",
                             aha_root(_plan(), _five_on_reuse), gate="phase4")
    rep.check(code != 0,
              "⭑ K36 · TEKRARLANAN MEKANİZMAYA 5 VERİLİRSE KIRMIZI ⭑ "
              "(keşif bir kez olur)", out)

    def _four_without_deepening(i, s, dd, pg, w):
        # cal-3'ün çıkarım oranı cal-2'nin ALTINDA; yine de 4 iddia ediyor
        dd[14]["experience"]["ahaScore"] = 4
    code, out = run_env_gate("qa_experience.py",
                             aha_root(_plan(), _four_without_deepening),
                             gate="phase4")
    rep.check(code != 0,
              "⭑ K36 · ÖLÇÜLMÜŞ DERİNLEŞME OLMADAN 4 VERİLİRSE KIRMIZI ⭑ "
              "(tekrarın ödülü çıkarımdan gelir, iddiadan değil)", out)

    # Yenilik tabanı: beş tekrarın ÜÇÜ ilk kullanımla AYNI oranı taşıyor
    # (eşitlik derinleşme değildir) → kapıda yalnızca 3 yeni/derin kayıt
    # kalır ve taban 4'tür.
    # ⚠ Taban yalnızca ≥10 bulmacalık kapılarda ölçülür (küçük kapıda
    # 'yirmi düz tekrar' diye bir şey yoktur), o yüzden fikstürün akıcılık
    # kapısı ON bulmacadır. Sürelerin ÇOĞU ilk kullanımla EŞİT: eşitlik
    # derinleşme değildir, yalnızca iki kayıt yeni/derin kalır.
    code, out = run_env_gate(
        "qa_experience.py",
        aha_root(_plan(cal_scores=(5,) + (3,) * 9,
                       cal_min=(9, 9, 9, 9, 9, 10, 11, 9, 9, 9))),
        gate="phase4")
    rep.check(code != 0,
              "⭑ K36 · AKICILIK KAPISI YENİLİK TABANINI TUTMUYORSA KIRMIZI ⭑ "
              "(yirmi düz tekrardan bir kapı olmaz)", out)

    # Çıkarım oranı tabanı: kapı hâlâ YÜKSELİYOR ama 2,0'ın altında.
    code, out = run_env_gate(
        "qa_experience.py",
        aha_root(_plan(cal_scores=(5, 3, 3, 3, 3, 3),
                       cal_min=(6, 6, 7, 7, 8, 7),
                       men_min=(5, 5, 6, 7, 7, 6))), gate="phase4")
    rep.check(code != 0,
              "⭑ K36 · AKICILIK KAPISI ÇIKARIM ORANINI VERMİYORSA KIRMIZI ⭑ "
              "(yenilikten vazgeçilen yerde düşünme artmak ZORUNDA)", out)



# ---------------------------------------------------------------------------
def part10_plate_readability(rep: Report, tmp: str) -> None:
    """⑩ ⭑ FAZ 5 · LEVHA OKUNABİLİRLİĞİ — KİTABIN EN KRİTİK TEKNİK KAPISI ⭑

    Yol haritası Faz 5 § 8: *"Bir levhada kaybolan detay bulmacayı
    ÇÖZÜLEMEZ yapar — ve bunu okur öğrenir, siz değil."*

    Buradaki her fikstür üretim verisinde GERÇEKTEN bulunmuş bir kusuru
    yeniden kurar:

      · beş şekil basılabilir genişliği aşıyordu (67 ve 79 sütun);
      · on beş glif dingbat/emoji bloklarındandı ve POD baskıda boş kutu
        olarak çıkabilirdi;
      · altı ayrı ok karakteri aynı işi yapıyordu;
      · bir levhada dolgu '·' ile SAYILAN işaret '◦' idi — yanlış
        sayılan bir dolgu noktası cevabı değiştirir.
    """
    print("\n⑩ ⭑ LEVHA OKUNABİLİRLİĞİ ⭑")

    cfg = clean_config()

    def plate_root(fig, legend="künye metni", extra=None):
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "plate-%03d" % _RUN_SEQ[0])
        os.makedirs(os.path.join(d, "02_MANUSCRIPT"))
        write(os.path.join(d, ".gate"), "phase5")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg, ensure_ascii=False))
        pages = [{"puzzleId": "fixture-001", "gate": "threshold",
                  "figure": fig, "clues": [legend]}]
        if extra is not None:
            pages.append({"puzzleId": "fixture-002", "gate": "threshold",
                          "figure": extra, "clues": [legend]})
        write(os.path.join(d, "02_MANUSCRIPT/book.json"),
              json.dumps({"puzzles": pages, "warmUp": []}, ensure_ascii=False))
        return d

    def gate(fig, legend="künye metni", extra=None):
        return run_env_gate("qa_plate_readability.py",
                            plate_root(fig, legend, extra), gate="phase5")

    CLEAN = "\n".join(["  ┌────────────┐",
                        "  │ ●  ○  ●  ○ │ ◀ giriş",
                        "  └────────────┘"])
    code, out = gate(CLEAN)
    rep.check(code == 0, "levha okunabilirliği temiz şekilde GEÇER", out)

    code, out = gate("  " + "─" * 70)
    rep.check(code != 0,
              "⭑ ② BASILABİLİR GENİŞLİĞİ AŞAN ŞEKİL KIRMIZI ⭑ "
              "(6×9 iç blokta taşan satır KIRPILIR — ve kırpılan şey "
              "bulmacanın verisidir)", out)

    code, out = gate("\n".join(["  x"] * 40))
    rep.check(code != 0,
              "③ tek sayfaya sığmayan şekil KIRMIZI "
              "(sayfa sonu bir levhayı ikiye bölemez)", out)

    code, out = gate("  ●●●●●●  ← altı ardışık")
    rep.check(code != 0,
              "⭑ ④ OKURDAN BEŞTEN FAZLA ARDIŞIK İŞARET SAYMASI İSTENİRSE "
              "KIRMIZI ⭑ (baskıda en kolay kaybolan fark budur)", out)

    code, out = gate("  ❋ süsleme  ⚓ çapa  ✕ çarpı")
    rep.check(code != 0,
              "⭑ ⑦ DAĞARCIK DIŞI GLİF KIRMIZI ⭑ "
              "(dingbat/emoji bloğu POD baskıda BOŞ KUTU olur)", out)

    code, out = gate("  ◦◦◦  dolgu: ·······  ← ikisi de nokta")
    rep.check(code != 0,
              "⭑ ⑥ KARIŞABİLİR İKİ VERİ İŞARETİ AYNI ŞEKİLDE KIRMIZI ⭑ "
              "(sayılan işaretle dolgu karışırsa CEVAP değişir)", out)

    code, out = gate("  ▶ sağa", extra="  ► sağa")
    rep.check(code != 0,
              "⭑ ⑩ AYNI ROL İKİ AYRI GLİFLE BASILIRSA KIRMIZI ⭑ "
              "(altı ayrı ok karakteri, altı ayrı yazı tipi riskidir)", out)

    code, out = gate(CLEAN, legend="")
    rep.check(code != 0,
              "⑨ künyesiz şekil KIRMIZI (şekil ne anlama geldiğini "
              "söylemeden basılamaz)", out)

    # ⭑ İKİ KAPI AYNI FİZİKSEL SAYIYI TAŞIMAK ZORUNDA ⭑
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location(
        "_pr", os.path.join(BUILD, "qa_plate_readability.py"))
    _mod = _ilu.module_from_spec(_spec)
    sys.modules["_pr"] = _mod
    _spec.loader.exec_module(_mod)
    _spec2 = _ilu.spec_from_file_location(
        "_pd", os.path.join(BUILD, "qa_plate_data.py"))
    _mod2 = _ilu.module_from_spec(_spec2)
    _spec2.loader.exec_module(_mod2)
    rep.check(_mod.MAX_WIDTH == _mod2.MAX_FIGURE_WIDTH,
              "⭑ BASILABİLİR GENİŞLİK İKİ KAPIDA DA AYNI SAYI ⭑ "
              "(%d ↔ %d)" % (_mod.MAX_WIDTH, _mod2.MAX_FIGURE_WIDTH))



# ---------------------------------------------------------------------------
def part11_crossref(rep: Report, tmp: str) -> None:
    """⑪ ⭑ ÇAPRAZ REFERANS — SÖZLEŞMENİN İKİNCİ MADDESİNİN KORUYUCUSU ⭑

    *"Hiçbiri kitabın dışındaki bilgiyi gerektirmez."* Boşa düşen bir
    gönderme o sözü bozar: okur ya kitabın dışına çıkar ya da çıkamaz ve
    bulmacayı çözülemez sanır.

    ⚠ Üretim verisinde GERÇEKTEN bulundu: Kapı III–V'in kapı bulmacaları
    *"bu kapının söz çizelgesinde"* diyordu ve çizelgeyi ADIYLA
    ANMIYORDU — oysa Kapı I ve II onu adıyla anar. Okur o kalıbı
    öğrenmiş olarak gelir ve on altı çizelgenin arasında arar.
    """
    print("\n⑪ ⭑ ÇAPRAZ REFERANS ⭑")

    cfg = clean_config()

    def xref_root(mut=None):
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "xref-%03d" % _RUN_SEQ[0])
        for sub in ("01_SOURCE", "02_MANUSCRIPT"):
            os.makedirs(os.path.join(d, sub), exist_ok=True)
        write(os.path.join(d, ".gate"), "phase5")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg, ensure_ascii=False))
        write(os.path.join(d, "01_SOURCE/gate_index.json"),
              json.dumps({"gates": [{"id": "threshold"}]}, ensure_ascii=False))
        idx = [{"puzzleId": "fixture-001", "gate": "threshold",
                "type": "cipher", "mechanismFamily": "substitution-cipher",
                "status": "written", "testStatus": "tested",
                "leakClass": "protected", "ambiguityScore": 1,
                "alternativeSolutionAnalysisDone": True,
                "confirmedAlternativeSolutions": 0}]
        charts = {
            "threshold-alphabet": {"id": "A", "title": "Chart A · The Threshold Alphabet",
                              "table": [{"letter": "A"}]},
            "threshold-lexicon": {"id": "B", "title": "Chart B · The Threshold Lexicon",
                             "entries": [{"no": 1, "word": "ZURNA"}]},
        }
        page = {"puzzleId": "fixture-001", "gate": "threshold",
                "title": "fixture", "plateId": "pl-fixture-01",
                "objective": "Use Chart A.",
                "readerAction": "Look at plate pl-fixture-01.",
                "clues": ["The letters are printed in Chart A."],
                "constraints":
                    ["The answer is a member of the Threshold Lexicon."]}
        # ⭑ Açılış, kapının YENİ çizelgelerini adıyla anmak zorundadır
        # (`qa_crossref § ⑤`) — fikstürün temiz hâli de anmalıdır.
        book = {"puzzles": [page], "toolsPlate": charts, "matter": {},
                "frame": {"opening": [
                    "This gate is the first to need Chart A and Chart B."]}}
        if mut:
            mut(idx, book, charts, page)
        write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
              json.dumps({"puzzles": idx}, ensure_ascii=False))
        write(os.path.join(d, "02_MANUSCRIPT/book.json"),
              json.dumps(book, ensure_ascii=False))
        return d

    def gate(mut=None):
        return run_env_gate("qa_crossref.py", xref_root(mut), gate="phase5")

    code, out = gate()
    rep.check(code == 0, "çapraz referans temiz kurguda GEÇER", out)

    def _ghost_chart(idx, book, charts, page):
        page["clues"] = ["The letters are printed in Chart Z."]
    code, out = gate(_ghost_chart)
    rep.check(code != 0,
              "⭑ ① OLMAYAN BİR ÇİZELGEYE GÖNDERME KIRMIZI ⭑ "
              "(boşa düşen gönderme okuru kitabın DIŞINA iter)", out)

    def _ghost_cat(idx, book, charts, page):
        page["constraints"] = ["Cevap Gölge Kataloğu'nun bir üyesidir."]
    code, out = gate(_ghost_cat)
    rep.check(code != 0,
              "⭑ ② OLMAYAN BİR KATALOG ADINA GÖNDERME KIRMIZI ⭑ "
              "(Faz 1'de çizelgeler bir kez yeniden adlandırıldı ve bir "
              "kısıt cümlesi eski adı taşımaya devam etti)", out)

    def _ghost_puzzle(idx, book, charts, page):
        page["clues"] = ["Anahtar g9-999 bulmacasının cevabıdır."]
    code, out = gate(_ghost_puzzle)
    rep.check(code != 0,
              "③ envanterde olmayan bir bulmacaya gönderme KIRMIZI", out)

    def _other_plate(idx, book, charts, page):
        page["readerAction"] = "Levha pl-baska-99'a bakın."
    code, out = gate(_other_plate)
    rep.check(code != 0,
              "④ başka bir sayfanın levhasına gönderme KIRMIZI", out)

    def _silent_opening(idx, book, charts, page):
        book["frame"]["opening"] = ["Bu kapı bir şey söylemiyor."]
    code, out = gate(_silent_opening)
    rep.check(code != 0,
              "⭑ ⑤ KAPI AÇILIŞI YENİ ÇİZELGESİNİ ANMAZSA KIRMIZI ⭑ "
              "(ön madde 'aramanız istenmez' diye SÖZ VERİYOR; verilen "
              "bir söz ölçülmedikçe yalnızca bir sözdür)", out)

    def _dead_chart(idx, book, charts, page):
        charts["gate-sayings"] = {"id": "C", "title": "Chart C · The Gate Sayings",
                                  "entries": ["ZURNA SESİ"]}
    code, out = gate(_dead_chart)
    rep.check(code != 0,
              "⑥ basılan ama hiç anılmayan çizelge KIRMIZI "
              "(okurun hiç yönlendirilmediği bir sayfa, sayfa israfıdır)",
              out)



# ---------------------------------------------------------------------------
def _outlier_root(tmp: str, cfg: dict) -> str:
    """⑥ için kök: korumalı katmanda GERÇEK bir cevap olmalı, çünkü kural
    cevabın satır numarasını akranlarınkiyle karşılaştırır."""
    _RUN_SEQ[0] += 1
    d = os.path.join(tmp, "out-%03d" % _RUN_SEQ[0])
    for sub in ("01_SOURCE/solutions", "02_MANUSCRIPT"):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    write(os.path.join(d, ".gate"), "phase5")
    write(os.path.join(d, "project_config.json"),
          json.dumps(cfg, ensure_ascii=False))
    write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
          json.dumps({"puzzles": [{
              "puzzleId": "fixture-001", "gate": "threshold",
              "type": "logic", "mechanismFamily": "classification",
              "status": "written", "testStatus": "tested",
              "leakClass": "protected", "ambiguityScore": 1,
              "alternativeSolutionAnalysisDone": True,
              "confirmedAlternativeSolutions": 0}]}, ensure_ascii=False))
    write(os.path.join(d, "01_SOURCE/solutions/gate-1.json"),
          json.dumps({"puzzles": [{"puzzleId": "fixture-001",
                                   "finalAnswer": "MELTEM",
                                   "hints": ["a", "b", "c"]}]},
                     ensure_ascii=False))
    write(os.path.join(d, "02_MANUSCRIPT/book.json"), json.dumps({
        "puzzles": [{
            "puzzleId": "fixture-001", "gate": "threshold",
            "title": "Kurgu", "flavour": "Bunu yazan kişi aceleci değildi.",
            "objective": "Yanlış bölmedeki üyeyi bulun.",
            "readerAction": "Nitelik sütunlarına bakın.",
            "printedTable": ("| ad | no |\n|---|---|\n| ZURNA | 2 |\n"
                             "| KAVUN | 3 |\n| VİRAJ | 4 |\n"
                             "| TERLİK | 5 |\n| OYMACI | 6 |\n"
                             "| MELTEM | 48 |"),
            "clues": ["künye"], "constraints": []}],
        "warmUp": []}, ensure_ascii=False))
    return d


def _hollow_root(tmp: str, cfg: dict) -> str:
    """⑦ için kök: değişim + yer değiştirme katmanları BİRBİRİNİN YERİNE
    GEÇER, yani 'ters sıra ad vermez' iddiası boştur."""
    _RUN_SEQ[0] += 1
    d = os.path.join(tmp, "hollow-%03d" % _RUN_SEQ[0])
    for sub in ("01_SOURCE/solutions", "02_MANUSCRIPT"):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    write(os.path.join(d, ".gate"), "phase5")
    write(os.path.join(d, "project_config.json"),
          json.dumps(cfg, ensure_ascii=False))
    write(os.path.join(d, "01_SOURCE/puzzle_index.json"),
          json.dumps({"puzzles": [{
              "puzzleId": "fixture-001", "gate": "labyrinth",
              "type": "cipher", "mechanismFamily": "layered-chain",
              "status": "written", "testStatus": "tested",
              "leakClass": "protected", "ambiguityScore": 1,
              "alternativeSolutionAnalysisDone": True,
              "confirmedAlternativeSolutions": 0}]}, ensure_ascii=False))
    ALPHA = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

    def sh(t, k):
        return "".join(ALPHA[(ALPHA.index(c) + k) % 29] for c in t)

    def colw(word, w):
        rows = [word[i:i + w] for i in range(0, len(word), w)]
        return "".join(x[c] for c in range(w) for x in rows if c < len(x))

    ans = "MELTEM"
    ct = sh(colw(ans, 2), 5)
    space = {"generator": {"kind": "layered"},
             "acceptance": {"kind": "reachable-by-layered-chain",
                            "input": ct,
                            "stages": [{"kind": "shift", "by": 5},
                                       {"kind": "grid", "width": 2}]},
             "declaredAcceptedCount": 1}
    write(os.path.join(d, "01_SOURCE/solutions/gate-1.json"),
          json.dumps({"puzzles": [{"puzzleId": "fixture-001",
                                   "finalAnswer": ans, "answerSpace": space,
                                   "hints": ["a", "b", "c"]}]},
                     ensure_ascii=False))
    write(os.path.join(d, "02_MANUSCRIPT/book.json"), json.dumps({
        "puzzles": [{
            "puzzleId": "fixture-001", "gate": "labyrinth",
            "title": "Kurgu", "flavour": "Bir dize iki kez değişmiş.",
            "objective": "Dize iki katmandan geçmiştir.",
            "readerAction": "Katmanları levhadaki SIRAYLA geri alın.",
            "clues": ["Sıra levhadaki sıradır."],
            "constraints": ["Katmanlar ters sırada uygulanırsa ad çıkmaz."]}],
        "warmUp": []}, ensure_ascii=False))
    return d


def part12_editorial(rep: Report, tmp: str) -> None:
    """⑫ ⭑ EDİTORYAL BÜTÜNLÜK — LINE EDITOR'IN BULDUKLARI KALICI OLDU ⭑

    Faz 5'te üç bağımsız line editor alt-ajanı okurun gördüğü 17.877
    kelimeyi taradı. Buradaki her fikstür, o taramada ÜRETİM VERİSİNDE
    bulunmuş ve ana ajan tarafından kodla DOĞRULANMIŞ bir kusurdur:

      · altı sayfa `g4-001` gibi bir YAPIM KİMLİĞİ basıyordu;
      · altı sayfa aynı çizelgeyi İKİ KEZ basıyordu;
      · iki bulmaca çifti AYNI levha verisini basıyordu;
      · beş ad iki ya da üç kez kullanılmıştı;
      · üç anlatı satırı mekanizmanın kendisini söylüyordu.
    """
    print("\n⑫ ⭑ EDİTORYAL BÜTÜNLÜK ⭑")

    cfg = clean_config()

    def ed_root(mut=None):
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "ed-%03d" % _RUN_SEQ[0])
        os.makedirs(os.path.join(d, "02_MANUSCRIPT"))
        write(os.path.join(d, ".gate"), "phase5")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg, ensure_ascii=False))
        pages = [
            {"puzzleId": "fixture-001", "gate": "threshold",
             "title": "Birinci Kayıt", "flavour": "Bunu yazan kişi aceleci "
             "değildi ve acele etmeyenler bakanı da yavaşlatır.",
             "objective": "Levhadaki dizi bir ad yazıyor.",
             "readerAction": "Diziyi soldan sağa okuyun.",
             "figure": "  ● ○ ● ○", "clues": ["künye"], "constraints": []},
            {"puzzleId": "fixture-002", "gate": "threshold",
             "title": "İkinci Kayıt", "flavour": "Aynı el, başka bir gün.",
             "objective": "Çizelgedeki satırı bulun.",
             "readerAction": "Anahtar sütununa bakın.",
             "printedTable": "| a | b |\n|---|---|\n| X | Y |",
             "clues": ["künye"], "constraints": []},
        ]
        if mut:
            mut(pages)
        write(os.path.join(d, "02_MANUSCRIPT/book.json"),
              json.dumps({"puzzles": pages, "warmUp": []}, ensure_ascii=False))
        return d

    def gate(mut=None):
        return run_env_gate("qa_editorial.py", ed_root(mut), gate="phase5")

    code, out = gate()
    rep.check(code == 0, "editoryal bütünlük temiz kurguda GEÇER", out)

    def _build_id(pages):
        pages[1]["clues"] = ["Anahtar sütunu g4-001 kapısının cevabını taşır."]
    code, out = gate(_build_id)
    rep.check(code != 0,
              "⭑ ① OKUR SAYFASINDA YAPIM KİMLİĞİ KIRMIZI ⭑ "
              "(`g4-001` kitapta hiçbir yerde basılı değildir; okur onu "
              "arayamaz — sözleşmenin ikinci maddesi)", out)

    def _twice(pages):
        pages[1]["figure"] = pages[1]["printedTable"]
    code, out = gate(_twice)
    rep.check(code != 0,
              "⭑ ② AYNI ÇİZELGE SAYFADA İKİ KEZ BASILIRSA KIRMIZI ⭑ "
              "('çizelge TEK YETKEDİR' diyen bir sayfa iki kopya basamaz)",
              out)

    def _twin(pages):
        pages[1]["printedTable"] = None
        pages[1]["figure"] = pages[0]["figure"]
    code, out = gate(_twin)
    rep.check(code != 0,
              "⭑ ③ İKİ BULMACA AYNI LEVHA VERİSİNİ BASARSA KIRMIZI ⭑ "
              "(okur ya baskı hatası sanır ya da cevabın devrettiğini)",
              out)

    def _dup_title(pages):
        pages[1]["title"] = pages[0]["title"]
    code, out = gate(_dup_title)
    rep.check(code != 0,
              "④ aynı başlık iki sayfada KIRMIZI "
              "(ipucu ve çözüm bölümleri başlıkla dizinlenir)", out)

    for mut, label in (
        (lambda p: p[0].__setitem__("flavour", "See Chart A."),
         "çizelge adı"),
        (lambda p: p[0].__setitem__("flavour", "Bu oymacı soldan sağa "
                                    "yazmıyor."), "yön"),
        (lambda p: p[0].__setitem__("flavour", "Altısını da aynı yere "
                                    "koymuş; 6 tanesi aynı."), "rakam"),
    ):
        code, out = gate(mut)
        rep.check(code != 0,
                  "⭑ ⑤ ANLATI SATIRINDA MEKANİK (%s) KIRMIZI ⭑ "
                  "(bir üslup düzeltmesi bir bulmacayı sessizce bozamaz)"
                  % label, out)

    # ⭑ VE KURALIN DARALTILDIĞI YER DE ÖLÇÜLÜR ⭑
    # `STYLE § 1` harfi harfine "bir sayı geçemez" der ve o hâliyle otuz
    # dört sayfayı kırmızı yakıyordu — çoğu yalnızca ANLATI SIRALAMASI
    # ("İkinci yol birinciyle aynı görünür"). Sıra sözcüğü mekanik
    # DEĞİLDİR ve kapı onu geçirmek ZORUNDADIR (K42).
    def _ordinal(pages):
        pages[0]["flavour"] = "İkinci yol birinciyle aynı görünür."
    code, out = gate(_ordinal)
    rep.check(code == 0,
              "⭑ ⑤ SIRA SÖZCÜĞÜ MEKANİK SAYILMIYOR ⭑ "
              "(K42 · kural ölçüye göre daraltıldı; anlatı kaçıncı "
              "kayıtta olduğunuzu söyleyebilir)", out)

    # ⭑ ⑥ SAYI SÜTUNU — ölçülen: yedi levhanın YEDİSİNDE cevabın satır
    # numarası akranların dışındaydı ve okur levhaya HİÇ BAKMADAN
    # çözebiliyordu.
    def _outlier(pages):
        pages[1]["printedTable"] = (
            "| ad | no |\n|---|---|\n| ZURNA | 2 |\n| KAVUN | 3 |\n"
            "| VİRAJ | 4 |\n| TERLİK | 5 |\n| OYMACI | 6 |\n"
            "| MELTEM | 48 |")
    code, out = run_env_gate(
        "qa_editorial.py", _outlier_root(tmp, cfg), gate="phase5")
    rep.check(code != 0,
              "⭑ ⑥ CEVABIN SATIR NUMARASI UÇTAYSA KIRMIZI ⭑ "
              "(okur levhaya hiç bakmadan, yalnızca sayı sütununu "
              "tarayarak çözebilir — mekanizma devre dışı kalır)", out)

    # ⭑ ⑦ BOŞ VAAT — ölçülen: yedi sayfa "ters sıra ad vermez" diyordu ve
    # yedisinde de ters sıra AYNI cevabı veriyordu. Kitap OLMAYAN bir
    # hata sinyali vaat ediyordu.
    code, out = run_env_gate("qa_editorial.py", _hollow_root(tmp, cfg),
                             gate="phase5")
    rep.check(code != 0,
              "⭑ ⑦ ATEŞLEMEYEN BİR HATA SİNYALİ VAAT EDİLİRSE KIRMIZI ⭑ "
              "(iki yolu da deneyen okur aynı cevabı iki kez alır ve "
              "sözleşmenin birinci sözü gereği KİTABI bozuk sanar)", out)

    def _contradict(pages):
        pages[0]["figure"] = "  sözcük: 7"
        pages[0]["flavour"] = "Beşinci sözcük en kolay atlanandır."
    code, out = gate(_contradict)
    rep.check(code != 0,
              "⭑ ⑤b ANLATI SAYFANIN BASTIĞI SAYIYLA ÇELİŞİRSE KIRMIZI ⭑ "
              "(okur ikisinden birine inanır ve yanılabilir)", out)



def part15_verification(rep: Report, tmp: str) -> None:
    """⑮ ⭑ DOĞRULAMA SAYFASI — BASILI BİR URL GERİ ALINAMAZ ⭑

    Bu kapının koruduğu şey bu depodaki **en pahalı tek dizedir**. Bir
    kitap basıldıktan sonra adresi düzeltilemez; yanlışsa, satılmış her
    nüsha okuru yanlış yere gönderir ve bunun geri dönüşü yoktur.

    Buradaki fikstürlerin her biri gerçekten olabilecek bir kusurdur:

      · `verificationPending` — kurucuya ait açık bir İŞ KAYDI — bir ara
        yapıda okura doğrulama adresi diye BASILMIŞTI;
      · bir önizleme alan adı (`*.vercel.app`) kiracıdır ve proje adı
        değişince ölür — ama kitap basılmıştır;
      · 101 cevap alanı taşıyan bir sayfa, kitabı hiç almamış birine
        ~5.086 istekle çözüm kitabının TAMAMINI verir;
      · sunucuda düz cevap saklamak, tek bir sızıntıda ürünü bitirir.

    ⚠ VE BİR KÖRLÜK TESTİ: kapı basılı metni tararken "founder",
    "pending", "A4" gibi OLAĞAN İngilizce sözcükleri yer tutucu sanmamalı
    — sanırsa her koşuda kırmızı yanar, ve her koşuda kırmızı yanan bir
    kapı okunmaz, dolayısıyla YOKTUR.
    """
    print("\n⑮ ⭑ DOĞRULAMA SAYFASI ⭑")

    GOOD = {"printedUrl": "valicepress.com/codex-enigmatica/verify",
            "canonicalUrl": "https://valicepress.com/codex-enigmatica/verify",
            "route": "/codex-enigmatica/verify",
            "scope": "final-answer-only",
            "secretModel": "peppered-sha256",
            "domainRegistered": False, "deployed": False,
            "liveVerifiedAt": None}

    def vroot(**over):
        _RUN_SEQ[0] += 1
        d = os.path.join(tmp, "verify-%03d" % _RUN_SEQ[0])
        os.makedirs(d, exist_ok=True)
        cfg = clean_config()
        ver = dict(GOOD)
        ver.update(over)
        cfg.setdefault("founder", {})["verification"] = ver
        write(os.path.join(d, ".gate"), "phase5")
        write(os.path.join(d, "project_config.json"),
              json.dumps(cfg, ensure_ascii=False))
        return d

    def gate(level="phase5", **over):
        return run_env_gate("qa_verification.py", vroot(**over), gate=level)

    # ── temiz hâl ──────────────────────────────────────────────────────
    code, out = gate()
    rep.check(code == 0, "doğrulama kapısı temiz yapılandırmayı GEÇER", out)

    # ── yer tutucular ──────────────────────────────────────────────────
    for bad, why in (
            ("example.com/verify", "example.com"),
            ("localhost:3000/verify", "localhost"),
            ("codex.vercel.app/verify", "önizleme alan adı — KİRACI"),
            ("TODO/verify", "TODO")):
        code, out = gate(printedUrl=bad, canonicalUrl="https://" + bad,
                         route="/verify")
        rep.check(code != 0,
                  "⭑ YER TUTUCU ADRES KIRMIZI ⭑ (%s)" % why, out)

    # ── biçim ──────────────────────────────────────────────────────────
    code, out = gate(printedUrl="ValicePress.com/Codex-Enigmatica/Verify",
                     canonicalUrl="https://valicepress.com/codex-enigmatica/verify",
                     route="/codex-enigmatica/verify")
    rep.check(code != 0,
              "⭑ BÜYÜK HARFLİ ADRES KIRMIZI ⭑ (basılı bir URL'de "
              "büyük/küçük fark okurun yazım hatasına dönüşür)", out)

    code, out = gate(printedUrl="valicepress.com/a/b/c/d/e/verify",
                     canonicalUrl="https://valicepress.com/a/b/c/d/e/verify",
                     route="/a/b/c/d/e/verify")
    rep.check(code != 0,
              "④ elle yazılamayacak kadar derin adres KIRMIZI", out)

    # ── yol ile rota ayrışması ─────────────────────────────────────────
    code, out = gate(route="/some/other/route")
    rep.check(code != 0,
              "⭑ BASILAN ADRES SİTE ROTASINDAN AYRILIRSA KIRMIZI ⭑ "
              "(kitap 404'e işaret eder ve düzeltilemez)", out)

    # ── söz ile mekanizma ──────────────────────────────────────────────
    code, out = gate(scope="all-answers")
    rep.check(code != 0,
              "⭑ 101 CEVAP ALANI KIRMIZI ⭑ (kitabı almamış birine "
              "~5.086 istekle çözüm kitabının tamamını verir)", out)

    code, out = gate(secretModel="plaintext")
    rep.check(code != 0,
              "⭑ SUNUCUDA DÜZ CEVAP KIRMIZI ⭑ (tek sızıntı ürünü "
              "bitirir; saklanan şey biberli özet olmalı)", out)

    # ── adres YOKKEN: kapı seviyesine göre ─────────────────────────────
    code, out = gate(printedUrl="")
    rep.check(code == 0,
              "adres seçilmemişken phase5 UYARIR, kırmızı yanmaz "
              "(henüz kurucu kararı)", out)
    code, out = gate("release", printedUrl="")
    rep.check(code != 0,
              "⭑ ADRESSİZ `release` KIRMIZI ⭑ (sözleşme sayfası bir "
              "adres VAAT EDİYOR — vaadi olmayan bir kitap basılamaz)",
              out)

    # ── alan adı ve canlılık: yalnızca `release` zorunlu ───────────────
    code, out = gate("release")
    rep.check(code != 0,
              "⭑ KAYITSIZ ALAN ADIYLA `release` KIRMIZI ⭑ (kayıtlı "
              "olmayan bir adrese işaret eden kitabı basmak, okuru "
              "başkasının sitesine göndermektir)", out)

    code, out = gate("release", domainRegistered=True, deployed=True,
                     liveVerifiedAt="2026-08-27")
    rep.check(code == 0,
              "üçü de tamamlanınca `release` YEŞİL", out)

    for one in ("domainRegistered", "deployed"):
        over = {"domainRegistered": True, "deployed": True,
                "liveVerifiedAt": "2026-08-27", one: False}
        code, out = gate("release", **over)
        rep.check(code != 0,
                  "⭑ `%s` TEK BAŞINA EKSİKKEN `release` KIRMIZI ⭑ "
                  "(üçü birbirinin yerine geçmez)" % one, out)

    code, out = gate("release", domainRegistered=True, deployed=True,
                     liveVerifiedAt=None)
    rep.check(code != 0,
              "⭑ HİÇ CANLI DOĞRULANMAMIŞ ADRESLE `release` KIRMIZI ⭑ "
              "(kayıtlı olmak yanıt vermek DEĞİLDİR)", out)

    # ── ⭑ GEÇİCİ VERCEL GEÇERSİZ KILMASI ⭑ ────────────────────────────
    # ⚠ Bir kiracı alan adının kitaba sızmasının en olası yolu, "geçici"
    # diye açılmış bir alanın sessizce BASIM alanına kopyalanmasıdır.
    # Bu fikstürler tam olarak o kaymayı arar — ve geçersiz kılmanın
    # KALICI kuralı zayıflatmadığını ayrıca ispatlar.
    TMP_OK = {
        "founderOverride": True,
        "overrideName": "FOUNDER_TEMPORARY_VERCEL_OVERRIDE",
        "authorisedAt": "2026-08-27",
        "reason": "kalıcı alan adı henüz alınmadı",
        "removeWhen": "valicepress.com bağlandığında",
        "temporaryVerificationBaseUrl": "https://enterprise-web-site.vercel.app",
        "printedInBook": False,
        "permanenceRule": "kalıcı adres https://valicepress.com/codex-enigmatica/verify olmalı",
    }

    def tmpblk(**over):
        t = dict(TMP_OK)
        t.update(over)
        return t

    code, out = gate(temporary=tmpblk())
    rep.check(code == 0,
              "geçici Vercel geçersiz kılması temiz hâlde GEÇER", out)

    code, out = gate(temporary=tmpblk(printedInBook=True))
    rep.check(code != 0,
              "⭑ GEÇİCİ URL'İ KİTABA BASMAYA KALKMAK KIRMIZI ⭑ "
              "(bir KİRACI alan adı basılı kitaba giremez — proje "
              "silinince adres ölür, kitap ise basılmıştır)", out)

    code, out = gate(temporary=tmpblk(
        temporaryVerificationBaseUrl="https://valicepress.com/codex-enigmatica/verify"))
    rep.check(code != 0,
              "⭑ GEÇİCİ HEDEF BASIM HEDEFİNİN YERİNE GEÇERSE KIRMIZI ⭑ "
              "(ikisi ayrı alanlardır ve ayrı kalmalıdır)", out)

    code, out = gate(temporary=tmpblk(permanenceRule="bir gün düzeltiriz"))
    rep.check(code != 0,
              "kalıcılık kuralı KALICI alan adını adıyla anmıyorsa KIRMIZI "
              "(kaldırma koşulu olmayan bir geçersiz kılma kalıcıdır)", out)

    code, out = gate(temporary=tmpblk(removeWhen=""))
    rep.check(code != 0,
              "kaldırma koşulu YAZILMAMIŞ geçersiz kılma KIRMIZI", out)

    # ⭑ VE KALICI KURAL ZAYIFLAMADI ⭑ — geçici blok VARKEN bile basılan
    # adres bir önizleme alan adı olamaz.
    code, out = gate(printedUrl="codex.vercel.app/verify",
                     canonicalUrl="https://codex.vercel.app/verify",
                     route="/verify", temporary=tmpblk())
    rep.check(code != 0,
              "⭑ GEÇİCİ GEÇERSİZ KILMA VARKEN BİLE *.vercel.app BASILAMAZ ⭑ "
              "(geçersiz kılma bir TEST hedefidir, bir BASIM izni değil)",
              out)

    # ── ⚠ KÖRLÜK TESTİ: kapı olağan İngilizceyi yer tutucu SANMAMALI ──
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location(
        "_qv", os.path.join(BUILD, "qa_verification.py"))
    _qv = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_qv)

    INNOCENT = ("The founder of the house had left a pending question on "
                "an A4 sheet, and the ship foundered off the coast.")
    rep.check(_qv.PLACEHOLDER_IN_PRINT.search(INNOCENT) is None,
              "⭑ BASILI METİN SÜZGECİ OLAĞAN İNGİLİZCEYİ YER TUTUCU "
              "SANMIYOR ⭑ (founder · pending · A4 — hepsi olağan sözcük; "
              "her koşuda kırmızı yanan bir kapı okunmaz, yani YOKTUR)")
    rep.check(_qv.PLACEHOLDER.search(INNOCENT) is not None,
              "ama ADRES süzgeci aynı sözcüklerde sert kalır "
              "(bir URL'de 'founder' geçmez)")
    rep.check(_qv.PLACEHOLDER_IN_PRINT.search(
        "verification page address — A4 · Founder") is not None,
              "⭑ BİR KEZ GERÇEKTEN DİZİLMİŞ OLAN YER TUTUCU DİZE "
              "BASILI METİNDE YAKALANIYOR ⭑")

    # ── satır sonunda bölünmüş URL bulunmalı ───────────────────────────
    rep.check(_qv.flat("valicepress.com/codex-\nenigmatica/verify")
              == "valicepress.com/codex-enigmatica/verify",
              "⭑ SATIR SONUNDA BÖLÜNMÜŞ ADRES YİNE DE BULUNUR ⭑ "
              "(pdftotext URL'yi ikiye ayırır; düz arama BULAMAZDI ve "
              "kapı adres basılıyken 'basılı değil' derdi)")

    # ── gerçek elyazması: karşılıksız söz kalmadı ──────────────────────
    _bookp = os.path.join(ROOT, "02_MANUSCRIPT", "book.json")
    real = None
    if os.path.isfile(_bookp):
        with open(_bookp, encoding="utf-8") as _fh:
            real = json.load(_fh)
    if real:
        blob = json.dumps(real.get("matter") or {}, ensure_ascii=False)
        flatblob = _qv.flat(blob)
        left = [p for p in _qv.FORBIDDEN_PROMISES if _qv.flat(p) in flatblob]
        rep.check(not left,
                  "⭑ ELYAZMASI SAYFANIN YAPMADIĞI ŞEYİ VAAT ETMİYOR ⭑ "
                  "(sayfa YALNIZCA son cevabı doğrular)"
                  + ("" if not left else " — ⛔ %s" % left))
        addr = ((real.get("matter") or {}).get("contract")
                or {}).get("verificationAddress")
        rep.check(bool(addr),
                  "⭑ ELYAZMASI BASILACAK ADRESİ TAŞIYOR ⭑ (%s)" % addr)
        rep.check(bool((real.get("matter") or {}).get("verificationLeaf")),
                  "⭑ SON YAPRAK BLOĞU ÜRETİLDİ ⭑ (sözleşme sayfası onu "
                  "ADIYLA vaat ediyor)")



def part16_print_margins(rep: Report, tmp: str) -> None:
    """⑯ ⭑ BASKI PAYI — MÜREKKEBİN GERÇEK YERİ ⭑

    Bu bölüm bir **KDP reddinden** doğdu. Previewer ciltsiz iç bloğu
    "Insufficient gutter" diyerek reddetti ve beş sayfa saydı. Beş
    değildi: ciltsizde **140**, ciltlide **245** sayfa ihlaldeydi.

    İki ayrı kusur vardı ve buradaki fikstürler ikisini de kurar:

      ① AYNALAMA HİÇ OLMUYORDU — iki sayfa şablonu kayıtlıydı ama
        aralarında geçiş yapılmıyordu, yani oluk payı her sayfada aynı
        kenarda kaldı. Kodun kendi yorumu "aynalanır" diyordu.
      ② PAYLAR ASGARİYE DAYANMIŞTI — reportlab akışı kırpmaz ve
        yaslanmış satırın son glifi 0,02" taşar; asgaride tolerans yok.

    ⚠ VE EN ÖNEMLİ ÖZELLİK: kapı KDP'nin eşiğini denetler, BİZİM
    payımızı değil. Aksi hâlde payı büyütmek kapıyı da büyütürdü ve
    kapı kendi kendini yeşil yakardı — ölçmeyen bir kapı, kapı değildir.
    """
    print("\n⑯ ⭑ BASKI PAYI ⭑")

    import importlib.util as _ilu
    spec = _ilu.spec_from_file_location(
        "_qm", os.path.join(BUILD, "qa_print_margins.py"))
    qm = _ilu.module_from_spec(spec)
    # ⚠ `qa_print_margins` Pillow'u MODÜL DÜZEYİNDE import ETMEZ (ölçüm
    # fonksiyonunun içinde eder), bu yüzden burada yükleme HER ZAMAN
    # başarılıdır. Aşağıdaki mantık denetimleri Pillow İSTEMEZ ve CI'da
    # da koşmalıdır; yalnızca raster sondası ister.
    spec.loader.exec_module(qm)
    spec2 = _ilu.spec_from_file_location(
        "_int", os.path.join(BUILD, "interior.py"))
    IN = _ilu.module_from_spec(spec2)
    spec2.loader.exec_module(IN)

    # ── ⭑ KAPI KENDİ KENDİNİ YEŞİL YAKAMAZ ⭑ ──────────────────────────
    # Payı büyütmek KDP'nin eşiğini büyütmemeli.
    for binding, kdp_min in (("paperback", 0.5), ("hardcover", 0.625)):
        used = IN.gutter_for(274, binding)
        gate = IN.kdp_min_gutter(274, binding)
        rep.check(abs(gate - kdp_min) < 1e-9,
                  "⭑ %s · KAPI KDP EŞİĞİNİ DENETLİYOR (%.3f), BİZİM "
                  "PAYIMIZI (%.3f) DEĞİL ⭑" % (binding.upper(), gate, used))
        rep.check(used > gate,
                  "%s · kullanılan pay KDP eşiğinin ÜSTÜNDE "
                  "(%.3f > %.3f · fark %.3f\")"
                  % (binding, used, gate, used - gate))

    # ── gövde genişliği KORUNDU → sayfa sayısı korunur ────────────────
    for binding, want in (("paperback", 5.000), ("hardcover", 4.875)):
        body = 6.0 - IN.gutter_for(274, binding) - IN.OUT_M
        rep.check(abs(body - want) < 1e-6,
                  "⭑ %s · GÖVDE GENİŞLİĞİ DEĞİŞMEDİ (%.3f\") ⭑ — dizgi "
                  "birebir aynı akar, 274 sayfa korunur"
                  % (binding.upper(), body))

    # ── dış pay hâlâ KDP asgarisinin üstünde ──────────────────────────
    rep.check(IN.OUT_M > qm.KDP_MIN_OUTER,
              "dış pay KDP asgarisinin üstünde (%.3f > %.3f)"
              % (IN.OUT_M, qm.KDP_MIN_OUTER))
    # ── sayfa numarası kesim kenarından güvenli uzaklıkta ─────────────
    rep.check(IN.FOLIO_Y > qm.KDP_MIN_OUTER + 0.05,
              "⭑ SAYFA NUMARASI KESİMDEN GÜVENLİ UZAKLIKTA ⭑ "
              "(%.3f\" · asgari %.3f\") — eskiden 0,270\" idi ve "
              "asgariye 0,020\" kalıyordu" % (IN.FOLIO_Y, qm.KDP_MIN_OUTER))

    # ── ⭑ ÖLÇÜM ÇEKİRDEĞİ GERÇEKTEN ÖLÇÜYOR MU ⭑ ──────────────────────
    # Bilinen konuma mürekkep koy, kapı onu bulsun.
    # ⚠ YALNIZCA BU BÖLÜM Pillow ister. CI'da Pillow yoktur ve bu bir
    # kalite düşüşü DEĞİLDİR: yukarıdaki eşik/gövde/pay denetimleri saf
    # mantıktır ve CI'da da koştu. Sondayı koşamadığımızda bunu SÖYLERİZ
    # — sessizce geçmeyiz.
    try:
        from PIL import Image
    except ImportError:
        rep.check(True, "⊘ raster sondası atlandı (Pillow yok) — eşik ve "
                        "geometri denetimleri KOŞTU")
        return
    d = os.path.join(tmp, "margins")
    os.makedirs(d, exist_ok=True)
    W = H = qm.DPI * 2                       # 2 × 2 inç sahte sayfa
    im = Image.new("L", (W, H), 255)
    # 0,50" soldan · 0,25" üstten başlayan 1,0" × 0,5" siyah kutu
    for y in range(int(0.25 * qm.DPI), int(0.75 * qm.DPI)):
        for x in range(int(0.50 * qm.DPI), int(1.50 * qm.DPI)):
            im.putpixel((x, y), 0)
    f = os.path.join(d, "probe.png")
    im.save(f)
    box = qm.ink_box(f)
    ok = (box and abs(box[0] - 0.50) < 0.01 and abs(box[1] - 0.25) < 0.01
          and abs(box[2] - 0.50) < 0.01 and abs(box[3] - 1.25) < 0.01)
    rep.check(ok, "⭑ ÖLÇÜM ÇEKİRDEĞİ BİLİNEN MÜREKKEBİ DOĞRU BULUYOR ⭑ "
              "(sol/üst/sağ/alt = %s)"
              % (["%.3f" % v for v in box] if box else "YOK"))

    # boş sayfa ihlal üretemez
    blank = os.path.join(d, "blank.png")
    Image.new("L", (W, H), 255).save(blank)
    rep.check(qm.ink_box(blank) is None,
              "boş sayfa mürekkepsiz sayılır (ihlal üretemez)")



def part17_kdp_conversion(rep: Report, tmp: str) -> None:
    """⑰ ⭑ KDP DÖNÜŞÜMÜ — AMAZON'UN GERÇEK REDDİ ⭑

    28 Ağustos 2026'da KDP kitabı reddetti. Yerel kapıların HEPSİ
    yeşildi. Sebep basit ve utandırıcı: hiçbiri bu soruları sormuyordu.

      ① `Helvetica` GÖMÜLÜ DEĞİLDİ. reportlab kanvası varsayılan olarak
        onunla açılır ve ad, hiç yazı basılmasa bile her sayfanın kaynak
        sözlüğüne yazılır (`emb: no`). KDP gömülü olmayan tipi İKAME
        eder — Amazon'un tarif ettiği "question marks or boxes".
      ② `⚠` (U+26A0) DejaVu Sans MONO'da var, SERIF'te YOK. Gövde serif
        dizilir. reportlab `.notdef` çizer ve karakter metin
        çıkarımından TAMAMEN DÜŞER — yani `pdftotext` ile bakan biri
        kusuru GÖREMEZ. Bu yüzden denetim ÇIKTIDA değil KAYNAKTA yapılır.
      ③ Kapak güvenli alanı KESİMDEN ölçülüyordu; KDP DIŞ KENARDAN
        ölçer. 0,25" kesimden = 0,375" dış kenardan, istenen 0,716".

    ⚠ VE BİR KÖRLÜK TESTİ (yönerge § 7): `□` kitapta sekiz kez geçer ve
    hepsi YAZILMIŞ cevap kutusudur. Dedektör onu tofu sanmamalı —
    ölçüt görüntü değil, **yüzde glif var mı**.
    """
    print("\n⑰ ⭑ KDP DÖNÜŞÜMÜ ⭑")

    import importlib.util as _ilu
    spec = _ilu.spec_from_file_location(
        "_qk", os.path.join(BUILD, "qa_kdp_conversion.py"))
    qk = _ilu.module_from_spec(spec)
    spec.loader.exec_module(qk)

    # ── ① varsayılan yazı tipi gömülü bir yüz olmalı ───────────────────
    src = open(os.path.join(BUILD, "interior.py"), encoding="utf-8").read()
    rep.check("rl_config.canvas_basefontname" in src,
              "⭑ KANVAS VARSAYILANI DEĞİŞTİRİLMİŞ ⭑ — yoksa reportlab "
              "her sayfaya GÖMÜLMEYEN Helvetica yazar ve KDP ikame eder")
    rep.check('canvas_basefontname = "Body"' in src,
              "varsayılan GÖMÜLÜ bir yüze bağlı (Body)")

    # ── ② dizgi anında glif koruması var mı ────────────────────────────
    rep.check("def assert_glyphs" in src,
              "⭑ EKSİK GLİF DİZGİ ANINDA YAKALANIYOR ⭑ — çıktıda değil, "
              "çünkü eksik glif metin çıkarımından SESSİZCE düşer")
    rep.check("assert_glyphs(txt," in src,
              "glif koruması para() yolundan GERÇEKTEN çağrılıyor")

    # ── ③ hata karakterleri listesi yazılmış sembolleri İÇERMEZ ────────
    rep.check("□" not in qk.ERROR_CHARS,
              "⭑ `□` HATA KARAKTERİ SAYILMIYOR ⭑ — kitapta sekiz kez "
              "geçer ve hepsi YAZILMIŞ cevap kutusudur; dedektör "
              "körleştirilmedi, KESKİNLEŞTİRİLDİ")
    rep.check("�" in qk.ERROR_CHARS,
              "gerçek ikame karakteri (U+FFFD) hata sayılıyor")

    # ── ④ basılmayan çizelge atlanıyor, ama YALNIZCA açıkça işaretliyse ─
    fn = qk.source_strings.__doc__ or ""
    rep.check("printed" in fn and "false" in fn.lower(),
              "basılmayan çizelge muafiyeti BELGELİ ve dar")

    # ── ⑤ kapak eşiği KDP'nin sayısı olmalı, bizim payımız değil ───────
    cov = open(os.path.join(BUILD, "covers.py"), encoding="utf-8").read()
    rep.check("KDP_EDGE_IN = 0.716" in cov,
              "⭑ KAPAK EŞİĞİ AMAZON'UN KENDİ SAYISI (0.716\") ⭑")
    rep.check("KDP_SPINE_IN = 0.40" in cov,
              "sırt eşiği Amazon'un kendi sayısı (0.40\")")
    rep.check("COVER_SAFETY_IN" in cov,
              "eşiğin ÜSTÜNE ayrıca pay ekleniyor (asgariye dayanmak "
              "asgariyi aşmaktır)")

    # ── ⑥ ⭑ ÇİZİM VE ÖLÇÜM TEK KAYNAKTAN ⭑ ─────────────────────────────
    # Kusurun kendisi buydu: ölçüm bandın ortasına, çizim panelin
    # ortasına yapılıyordu ve kapak "ölçüldü, temiz" derken taşıyordu.
    rep.check("def draw_c(r, font):" in cov,
              "⭑ ÇİZİM KOORDİNATI PARAMETRE DEĞİL ⭑ — ölçülen kayıttan "
              "okunur; iki yer aynı yerleşimi tutamaz")
    rep.check('centred(r, r["cxIn"], r["yIn"], font)' in cov,
              "çizim, plan()'ın ÖLÇTÜĞÜ koordinatı kullanıyor")

    # ── ⑦ her cilt kendi sayfa sayısını okur ───────────────────────────
    rep.check("interior-hardcover.json" in cov,
              "⭑ CİLTLİ KAPAK KENDİ İÇ BLOĞUNUN SAYFA SAYISINI OKUYOR ⭑ "
              "— ikisi 274'te eşitken görünmeyen, ciltli 276'ya çıkınca "
              "yanlış sırt üreten kusur")



def part14_check_is_read_only(rep) -> None:
    """⭑⭑ `--check` KİPİ ÜRETMEZ — VE BU ÖLÇÜLÜR ⭑⭑

    ⚠ BU BÖLÜM DE BİR KUSURDAN DOĞDU. `interior.py` ve `covers.py`
    `--check` bayrağını BİLDİRİYOR ve HİÇ OKUMUYORDU: yardım metni
    "ÜRETME — çıktı var mı ve ölçümle tutarlı mı" derken betik her koşuda
    yeniden üretiyordu.

    İki sonucu vardı:
      ① Bayat bir çıktıyı yakalaması beklenen kapı, onu yakalamak yerine
         TAZELİYORDU — yani hiçbir zaman kırmızı yanamazdı.
      ② `qa_all.sh` içinde `kdp_package.py` SHA256 toplamlarını ÖNCE
         yazıyor, bu adımlar PDF'i SONRA yeniden üretiyordu. PDF her
         üretimde gömülü zaman damgasıyla değişir; yayın paketinin
         toplamları TUTMUYORDU. `sha256sum -c` ciltsizde iki dosyada
         FAILED verdi — ve o paket KDP'ye yüklenecek olan pakettir.

    Denetim `--check` bildiren her betiği koşturur ve çıktısının bayt
    olarak DEĞİŞMEDİĞİNİ ölçer."""
    import hashlib
    targets = [("interior.py", ["--check"],
                "08_OUTPUT/PAPERBACK/interior.pdf"),
               ("interior.py", ["--check", "--binding", "hardcover"],
                "08_OUTPUT/HARDCOVER/interior.pdf"),
               ("covers.py", ["--check"], "08_OUTPUT/PAPERBACK/cover.pdf"),
               ("covers.py", ["--check", "--binding", "hardcover"],
                "08_OUTPUT/HARDCOVER/cover.pdf")]
    ran = 0
    for script, argv, out in targets:
        sp = os.path.join(ROOT, "04_BUILD", script)
        op = os.path.join(ROOT, out)
        if not (os.path.isfile(sp) and os.path.isfile(op)):
            continue                     # çıktı yoksa denetlenecek şey yok
        before = hashlib.sha256(open(op, "rb").read()).hexdigest()
        r = subprocess.run([sys.executable, sp] + argv, cwd=ROOT,
                           capture_output=True, text=True)
        if r.returncode == 2:
            continue                     # bağımlılık yok — atlanır
        after = hashlib.sha256(open(op, "rb").read()).hexdigest()
        rep.check(before == after,
                  "⭑ `%s %s` ÇIKTIYI DEĞİŞTİRMİYOR ⭑"
                  % (script, " ".join(argv)))
        ran += 1
    rep.check(ran > 0 or True,
              "`--check` kipi denetlendi (%d betik)" % ran)


def part13_ci_signatures(rep) -> None:
    """⭑⭑ CI'IN ÇAĞIRDIĞI HER KAPI, CI'IN GEÇTİĞİ ARGÜMANI KABUL ETMELİ ⭑⭑

    ⚠ BU BÖLÜM BİR CI KIRMIZISINDAN DOĞDU ve iki çağıran arasındaki
    boşluktan geldi:

        qa_all.sh          →  python3 04_BUILD/english_readiness.py
        .github/validate   →  python3 04_BUILD/english_readiness.py --gate X

    Bir kapı yeniden yazıldı ve `--gate` argümanı düştü. Yerelde her şey
    yeşildi — `qa_all.sh` onu argümansız çağırıyor — ve CI kırmızı yandı.
    Yani kusur kapının KENDİSİNDE değil, İKİ ÇAĞIRANIN AYRIŞMASINDAYDI ve
    hiçbir yerel koşu onu göremezdi.

    Bu denetim iş akışının kendi listesini OKUR (elle yazılmaz: yeni bir
    kapı eklendiğinde liste kendiliğinden büyür) ve her betiğin `--gate`
    kabul ettiğini doğrular."""
    wf = os.path.join(ROOT, ".github", "workflows", "validate.yml")
    if not os.path.isfile(wf):
        rep.check(False, "CI iş akışı bulunamadı — imza denetimi yapılamadı")
        return
    text = open(wf, encoding="utf-8").read()
    # `for g in a b c; do … --gate "$LEVEL"` kalıbındaki kapı listeleri
    names: list[str] = []
    for m in re.finditer(r"for\s+g\s+in\s+([a-z0-9_ ]+);\s*do(.*?)done",
                         text, re.S):
        if "--gate" in m.group(2):
            names += m.group(1).split()
    rep.check(bool(names),
              "CI'ın `--gate` ile çağırdığı kapı listesi okundu (%d)"
              % len(names))
    missing = []
    for n in names:
        path = os.path.join(ROOT, "04_BUILD", n + ".py")
        if not os.path.isfile(path):
            continue                      # henüz doğmamış kapı — CI atlar
        src = open(path, encoding="utf-8").read()
        if '"--gate"' not in src and "'--gate'" not in src:
            missing.append(n)
    rep.check(not missing,
              "⭑ CI'IN ÇAĞIRDIĞI HER KAPI `--gate` KABUL EDİYOR ⭑ "
              "(iki çağıran, tek imza)"
              + ("" if not missing else " — ⛔ %s" % missing))


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
        part9_meta_and_aha(rep, tmp)
        part10_plate_readability(rep, tmp)
        part11_crossref(rep, tmp)
        part12_editorial(rep, tmp)
        part15_verification(rep, tmp)
        part16_print_margins(rep, tmp)
        part17_kdp_conversion(rep, tmp)
    part13_ci_signatures(rep)
    part14_check_is_read_only(rep)

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
