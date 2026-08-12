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

Dört bölüm:
  ①  temiz kurgu BÜTÜN kapılardan geçer          (yanlış pozitif yok)
  ②  her kusurlu kurgu İLGİLİ kapıda yakalanır   (körlük yok)
  ③  kapı seviyeleri gerçekten kilitliyor        (kapsam kapıları)
  ④  her muafiyet en az bir kez DEVREYE GİRİYOR  (ölü kural yok)

④ doğrudan Bestiarium'un üç ölü kuralına ve World Myths'in K14 kararına
cevaptır: takip edilmeyen bir dosya için yazılmış muafiyet ÖLÜ MUAFİYETTİR
ve sessizce yanlış güven verir.

Çıkış kodları:  0 = geçti   1 = KÖRLÜK BULUNDU
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "04_BUILD")

VALIDATE_SPEC = os.path.join(BUILD, "validate_spec.py")
VALIDATE_STRUCTURE = os.path.join(BUILD, "validate_structure.py")
CONFIG = os.path.join(ROOT, "project_config.json")


# ---------------------------------------------------------------------------
# Kurgu üreteci — GERÇEK envanterden bağımsız, tam kontrollü veri
# ---------------------------------------------------------------------------
def clean_config() -> dict:
    with open(CONFIG, encoding="utf-8") as fh:
        return json.load(fh)


def clean_games(cfg: dict, n: int = 140, status: str = "candidate") -> dict:
    """Şemaya uyan, kusursuz kurgu envanter — PUBLIC KATMAN.

    ⚠ Kurgu kayıtlar ÇÖZÜM ALANI TAŞIMAZ. Taşısalardı temiz kurgu bile
    çözüm sızıntısı kapısında takılırdı — ki § ②(f) tam olarak bunu
    test eder."""
    gates_ = [g["id"] for g in cfg["scope"]["gateStructure"]]
    types = ["observation", "cipher", "logic", "spatial", "self-referential"]
    puzzles = []
    for i in range(n):
        puzzles.append({
            "puzzleId": "fixture-%03d" % i,
            "gate": gates_[i % len(gates_)],
            "type": types[i % len(types)],
            "status": status,
            "difficulty": 1 + (i % 3),
            "ambiguityScore": 1,
            "dependencies": [],
        })
    return {"puzzles": puzzles}


def run(script: str, *extra: str, gate: str | None = None,
        index: str | None = None) -> tuple[int, str]:
    cmd = [sys.executable, script, *extra]
    if gate:
        cmd += ["--gate", gate]
    env = dict(os.environ)
    if index:
        env["WORLDGAMES_GAME_INDEX"] = index
    out = subprocess.run(cmd, capture_output=True, text=True, env=env,
                         timeout=120, cwd=ROOT)
    return out.returncode, out.stdout + out.stderr


_RUN_SEQ = [0]


def run_spec_with(cfg: dict, games: dict | None, gate: str,
                  tmp: str) -> tuple[int, str]:
    """validate_spec'i kurgu dosyalarla koşturur.

    Betik yolları sabit okuduğu için kurgu bir PROJE KÖKÜ kurulur:
    gerçek depo asla değiştirilmez.

    ⚠ HER KOŞU KENDİ KÖKÜNÜ ALIR. Tek bir kök paylaşılırsa önceki testin
    yazdığı game_index.json sonraki testte HÂLÂ ORADA olur ve
    "envantersiz phase1 kırmızı yanmalı" testi sessizce anlamsızlaşır —
    yani testin kendisi kör olur. Bu kusur selftest'in ilk koşusunda
    yakalandı ve bu satır onun düzeltmesidir."""
    _RUN_SEQ[0] += 1
    fake_root = os.path.join(tmp, "root-%03d" % _RUN_SEQ[0])
    os.makedirs(os.path.join(fake_root, "01_SOURCE"), exist_ok=True)
    os.makedirs(os.path.join(fake_root, "04_BUILD"), exist_ok=True)

    with open(os.path.join(fake_root, "project_config.json"), "w",
              encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False)
    if games is not None:
        with open(os.path.join(fake_root, "01_SOURCE", "puzzle_index.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(games, fh, ensure_ascii=False)
    with open(os.path.join(fake_root, ".gate"), "w", encoding="utf-8") as fh:
        fh.write(gate)

    # Betiği kurgu köke kopyala: ROOT'u kendi konumundan türetiyor.
    import shutil
    shutil.copy2(VALIDATE_SPEC, os.path.join(fake_root, "04_BUILD",
                                             "validate_spec.py"))
    out = subprocess.run(
        [sys.executable, os.path.join(fake_root, "04_BUILD", "validate_spec.py"),
         "--gate", gate],
        capture_output=True, text=True, timeout=120)
    return out.returncode, out.stdout + out.stderr


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
    games = clean_games(cfg)
    code, out = run_spec_with(cfg, games, "phase1", tmp)
    rep.check(code == 0, "temiz kurgu + phase1 → geçer", out)


def part2_flaws_caught(rep: Report, tmp: str) -> None:
    print("\n② her kusurlu kurgu ilgili kapıda yakalanır (körlük yok)")

    base = clean_config()

    # (a) yinelenen bulmaca kimliği
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    g["puzzles"][7]["puzzleId"] = g["puzzles"][3]["puzzleId"]
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "yinelenen puzzleId YAKALANIR", out)

    # (b) tanımsız kapı
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    g["puzzles"][11]["gate"] = "uydurma-kapi"
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "tanımsız kapı YAKALANIR", out)

    # (c) geçersiz durum alanı
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    g["puzzles"][5]["status"] = "belki"
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "geçersiz status YAKALANIR", out)

    # (d) geçersiz bulmaca tipi
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    g["puzzles"][8]["type"] = "uydurma-tip"
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "geçersiz bulmaca tipi YAKALANIR", out)

    # (e) kapı bulmaca toplamı hedefe eşit değil
    cfg = copy.deepcopy(base)
    cfg["scope"]["gateStructure"][0]["puzzles"] = 5
    code, out = run_spec_with(cfg, clean_games(base), "phase1", tmp)
    rep.check(code != 0, "kapı toplamı ↔ hedef çelişkisi YAKALANIR", out)

    # (f) ⭑ VAROLUŞSAL: PUBLIC KATMANDA ÇÖZÜM ⭑
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    g["puzzles"][3]["solution"] = "THE RAVEN AT DAWN"
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "⭑ PUBLIC KATMANDA ÇÖZÜM YAKALANIR ⭑", out)

    # (f2) çözüm başka bir alan adıyla gizlenmiş
    cfg = copy.deepcopy(base)
    g = clean_games(cfg)
    g["puzzles"][9]["answerKey"] = "XYZ"
    code, out = run_spec_with(cfg, g, "phase1", tmp)
    rep.check(code != 0, "⭑ answerKey ile gizlenmiş çözüm YAKALANIR ⭑", out)

    # (g) belirsizlik eşiğini aşan DOĞRULANMIŞ bulmaca
    cfg = copy.deepcopy(base)
    g = clean_games(cfg, status="written")
    g["puzzles"][2]["ambiguityScore"] = 3
    code, out = run_spec_with(cfg, g, "phase2", tmp)
    rep.check(code != 0, "BELİRSİZLİK EŞİĞİ AŞIMI YAKALANIR", out)

    # (h) zorluk eğrisi geriye düşüyor
    cfg = copy.deepcopy(base)
    cfg["scope"]["gateStructure"][4]["difficulty"] = 1
    code, out = run_spec_with(cfg, clean_games(base), "phase1", tmp)
    rep.check(code != 0, "ZORLUK EĞRİSİ DÜŞÜŞÜ YAKALANIR", out)

    # (i) ⭑ ÇÖZÜLEBİLİRLİK SÖZLEŞMESİNİN GEVŞETİLMESİ ⭑
    for field in ("uniqueSolutionRequired", "alternativeSolutionAnalysisRequired",
                  "hintMustNotContainAnswer", "dependencyGraphMustBeAcyclic"):
        cfg = copy.deepcopy(base)
        cfg["solvability"][field] = False
        code, out = run_spec_with(cfg, clean_games(base), "phase1", tmp)
        rep.check(code != 0,
                  "⭑ SÖZLEŞME GEVŞETMESİ YAKALANIR: %s ⭑" % field, out)

    # (j) ⭑ ÖLDÜRME KAPISI EŞİĞİNİN DÜŞÜRÜLMESİ ⭑
    cfg = copy.deepcopy(base)
    cfg["killGate"]["passCriteria"]["solversCompletingGateI"] = 1
    code, out = run_spec_with(cfg, clean_games(base), "phase1", tmp)
    rep.check(code != 0, "⭑ ÖLDÜRME KAPISI EŞİĞİ DÜŞÜRÜLMESİ YAKALANIR ⭑", out)

    # (k) çözüm alan listesi config ile betik arasında ayrışmış
    cfg = copy.deepcopy(base)
    cfg["contentProtection"]["solutionFieldNames"] = ["solution"]
    code, out = run_spec_with(cfg, clean_games(base), "phase1", tmp)
    rep.check(code != 0, "ÇÖZÜM ALAN LİSTESİ AYRIŞMASI YAKALANIR", out)

    # (l) ekonomik olarak imkânsız fiyat → negatif telif
    cfg = copy.deepcopy(base)
    for ed in cfg["production"]["editionsHypothesis"]:
        if ed["id"] == "paperback":
            ed["list"] = 2.99          # 208 sayfa normal trim: baskı 3,50 $
    code, out = run_spec_with(cfg, clean_games(base), "phase1", tmp)
    rep.check(code != 0, "NEGATİF TELİF yakalanır (fiyat < baskı maliyeti)", out)

    # (m) Kindle açılmış (görsel şifre koruması delinmiş)
    cfg = copy.deepcopy(base)
    for ed in cfg["production"]["editionsHypothesis"]:
        if ed["id"] == "kindle":
            ed["enabled"] = True
            ed["list"] = 9.99
    code, out = run_spec_with(cfg, clean_games(base), "phase1", tmp)
    rep.check(code != 0, "KINDLE AÇILMASI YAKALANIR (görsel şifre koruması)", out)


def part3_gates_lock(rep: Report, tmp: str) -> None:
    print("\n③ kapı seviyeleri gerçekten kilitliyor")

    cfg = clean_config()

    # phase0: envanter yokken geçmeli (Faz 1 henüz üretmedi)
    code, out = run_spec_with(cfg, None, "phase0", tmp)
    rep.check(code == 0, "phase0 envantersiz geçer", out)

    # phase1: envanter yoksa KIRMIZI
    code, out = run_spec_with(cfg, None, "phase1", tmp)
    rep.check(code != 0, "phase1 envantersiz KIRMIZI", out)

    # phase1: 130'un altında aday → KIRMIZI
    code, out = run_spec_with(cfg, clean_games(cfg, 100), "phase1", tmp)
    rep.check(code != 0, "phase1 yetersiz adayla KIRMIZI (100 < 130)", out)

    # phase2: ÖLDÜRME KAPISI — 20 doğrulanmış bulmaca yoksa KIRMIZI
    code, out = run_spec_with(cfg, clean_games(cfg, 140, "candidate"),
                              "phase2", tmp)
    rep.check(code != 0,
              "⭑ phase2 (ÖLDÜRME KAPISI) doğrulanmış bulmaca olmadan KIRMIZI ⭑",
              out)

    # phase2: 20 yazılmış varsa geçer
    g = clean_games(cfg, 140, "candidate")
    for i in range(20):
        g["puzzles"][i]["status"] = "written"
    code, out = run_spec_with(cfg, g, "phase2", tmp)
    rep.check(code == 0, "phase2 20 yazılmış bulmacayla geçer", out)

    # phase4: 100 yazılmış bulmaca yoksa KIRMIZI
    code, out = run_spec_with(cfg, g, "phase4", tmp)
    rep.check(code != 0, "phase4 eksik manuscript ile KIRMIZI", out)


def part4_no_dead_exemptions(rep: Report) -> None:
    print("\n④ her muafiyet en az bir kez devreye giriyor (ölü kural yok)")

    import re                        # noqa: E402
    sys.path.insert(0, BUILD)
    import validate_structure as vs   # noqa: E402

    # Sızıntı taraması muafiyetleri: muaf tutulan dosya GERÇEKTEN VAR OLMALI.
    # Var olmayan bir dosya için yazılmış muafiyet ÖLÜ MUAFİYETTİR ve
    # sessizce yanlış güven verir (World Myths K14 · Bestiarium D28).
    for rel in sorted(vs.LEAK_SCAN_SKIP):
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "sızıntı muafiyeti canlı: %s" % rel)

    for rel in sorted(vs.EMBED_SCAN_SKIP):
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "gömülü-değer muafiyeti canlı: %s" % rel)

    # ⑤ ⭑ ÇÖZÜM TARAMASI MUAFİYETLERİ ⭑
    # Bu liste kısadır ve KISA KALMALIDIR. Her muafiyet, çözüm sızıntısı
    # kapısında açılmış bir deliktir; gereksiz bir tanesi bile fazladır.
    for rel in sorted(vs.SOLUTION_SCAN_SKIP):
        rep.check(os.path.isfile(os.path.join(ROOT, rel)),
                  "çözüm-taraması muafiyeti canlı: %s" % rel)
    rep.check(len(vs.SOLUTION_SCAN_SKIP) <= 4,
              "çözüm taraması muafiyet listesi kısa (%d ≤ 4)"
              % len(vs.SOLUTION_SCAN_SKIP))
    for rel in sorted(vs.SOLUTION_SCAN_SKIP):
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as fh:
            body = fh.read()
        hits = sum(1 for pat in vs.SOLUTION_FIELD_MARKERS if re.search(pat, body))
        rep.check(hits >= vs.SOLUTION_MIN_HITS,
                  "çözüm muafiyeti GEREKLİ: %s [%d işaret]" % (rel, hits))

    # Muafiyet listesi gerçekten GEREKLİ mi: muaf dosya, muaf olmasaydı
    # yakalanacak mıydı? Değilse muafiyet gereksizdir ve kaldırılmalıdır.
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
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
    part4_no_dead_exemptions(rep)

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
