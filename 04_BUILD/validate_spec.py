#!/usr/bin/env python3
"""
VERİ BÜTÜNLÜĞÜ VE KAPSAM KAPISI — Codex Enigmatica
================================================================================
Bu kapı dört soruyu sorar:

  ① project_config.json kendi içinde tutarlı mı
  ② puzzle_index.json şemaya uyuyor mu, kimlikler tekil mi
  ③ .gate seviyesinin GEREKTİRDİĞİ kapsam sağlanmış mı
  ④ PUBLIC KATMANDA ÇÖZÜM VAR MI

④ bu projeye özgüdür ve sert bir kuraldır: `puzzle_index.json` bulmacaların
PUBLIC kaydıdır ve içinde ÇÖZÜM ALANI BULUNAMAZ. Bir çözüm public katmana
yazılırsa ürün yayımlanmadan değersizleşir.

Ayrıca öldürme kapısı eşikleri (Faz 2) burada doğrulanır: eşikler SAYISALDIR
ve config'de durur — yoruma yer yoktur.

TASARIM: yalnızca Python standart kütüphanesi. Üçüncü taraf paket YOK —
yazım fazlarında günde onlarca push olur ve iki dakikalık kurulum beklemek
disiplini öldürür. (World Myths kararı K7.)

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
PUZZLE_INDEX = os.path.join(ROOT, "01_SOURCE", "puzzle_index.json")
GATE_INDEX = os.path.join(ROOT, "01_SOURCE", "gate_index.json")

VALID_GATES = ["phase0", "phase1", "phase2", "phase3", "phase4", "phase5", "release"]
VALID_STATUS = ["candidate", "drafted", "validated", "written", "dropped"]
VALID_PUZZLE_TYPE = ["observation", "cipher", "logic", "spatial",
                     "self-referential", "gate", "meta"]

# ④ PUBLIC KATMANDA BULUNAMAYACAK ALAN ADLARI.
# Bu liste project_config.json § contentProtection.solutionFieldNames
# ile senkron olmak ZORUNDADIR; check_config bunu denetler.
FORBIDDEN_PUBLIC_FIELDS = ["solution", "intendedSolution", "answer",
                          "answerKey", "solutionPath", "hints"]


class Report:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.facts: dict = {}

    def ok(self, label: str) -> None:
        self.checks += 1
        if self.verbose:
            print("  ✓ %s" % label)

    def fail(self, label: str) -> None:
        self.checks += 1
        self.errors.append(label)
        print("  ✗ %s" % label)

    def warn(self, label: str) -> None:
        self.warnings.append(label)
        print("  ! %s" % label)

    def check(self, cond: bool, label: str) -> bool:
        if cond:
            self.ok(label)
        else:
            self.fail(label)
        return cond


def load_json(path: str, rep: Report, required: bool = True):
    if not os.path.exists(path):
        if required:
            rep.fail("dosya yok: %s" % os.path.relpath(path, ROOT))
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        rep.fail("JSON bozuk: %s — %s" % (os.path.relpath(path, ROOT), exc))
        return None


def read_gate() -> str:
    path = os.path.join(ROOT, ".gate")
    if not os.path.exists(path):
        return "phase0"
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()


# ---------------------------------------------------------------------------
def check_config(cfg: dict, rep: Report) -> None:
    print("\n── yapılandırma bütünlüğü ──")

    for key in ("project", "founder", "audience", "scope", "solvability",
                "killGate", "contentProtection", "production", "gates", "style"):
        rep.check(key in cfg, "config bloğu var: %s" % key)

    scope = cfg.get("scope", {})
    gates_ = scope.get("gateStructure", [])
    rep.check(len(gates_) == scope.get("gates", -1),
              "kapı sayısı yapıyla uyuşuyor (%d)" % len(gates_))

    total = sum(g.get("puzzles", 0) for g in gates_)
    puzzles = scope.get("puzzles", 0)
    rep.check(total == puzzles,
              "kapı bulmaca toplamı (%d) hedefe (%d) EŞİT" % (total, puzzles))

    ids = [g.get("id") for g in gates_]
    rep.check(len(ids) == len(set(ids)), "kapı kimlikleri tekil")

    # Zorluk eğrisi monoton artmalı: bir kapı öncekinden KOLAY olamaz.
    diffs = [g.get("difficulty", 0) for g in gates_]
    rep.check(all(diffs[i] <= diffs[i + 1] for i in range(len(diffs) - 1)),
              "zorluk eğrisi monoton artıyor %s" % diffs)

    # ÇÖZÜLEBİLİRLİK SÖZLEŞMESİ — gevşetilmesi yakalanmalı
    sol = cfg.get("solvability", {})
    rep.check(sol.get("deterministicSolutionRequired") is True,
              "deterministik çözüm şartı duruyor")
    rep.check(sol.get("uniqueSolutionRequired") is True,
              "tek çözüm şartı duruyor")
    rep.check(sol.get("alternativeSolutionAnalysisRequired") is True,
              "alternatif çözüm analizi şartı duruyor")
    rep.check(sol.get("hintMustNotContainAnswer") is True,
              "ipucu cevabı içeremez şartı duruyor")
    rep.check(sol.get("maxAcceptableAmbiguityScore", 99) <= 2,
              "belirsizlik eşiği ≤2")
    rep.check(sol.get("dependencyGraphMustBeAcyclic") is True,
              "DAG döngüsüzlük şartı duruyor")

    # ÖLDÜRME KAPISI — eşikler sayısal olmalı
    kg = cfg.get("killGate", {})
    rep.check(kg.get("phase") == "phase2", "öldürme kapısı Faz 2'de")
    pc_ = kg.get("passCriteria", {})
    hs = kg.get("hardStopCriteria", {})
    rep.check(pc_.get("solversCompletingGateI", 0) >= 4,
              "öldürme kapısı geçme eşiği ≥4/5 çözücü")
    rep.check(pc_.get("confirmedAlternativeSolutions", 99) == 0,
              "onaylanmış alternatif çözüm eşiği = 0")
    rep.check(hs.get("solversCompletingGateI", 99) <= 3,
              "sert durdurma eşiği ≤3/5 çözücü")

    # GİZLİLİK SÖZLEŞMESİ — iki liste senkron olmalı
    cp = cfg.get("contentProtection", {})
    rep.check(set(cp.get("solutionFieldNames", [])) == set(FORBIDDEN_PUBLIC_FIELDS),
              "çözüm alan adları config ile betik arasında SENKRON")

    # Üretim ekonomisi: KDP formülünün kendisi burada doğrulanır.
    prod = cfg.get("production", {})
    pc = prod.get("kdpPrintCost", {})
    pages = scope.get("pageTarget", 0)
    for ed in prod.get("editionsHypothesis", []):
        if not ed.get("enabled") or ed.get("list") is None:
            continue
        eid, lst = ed["id"], ed["list"]
        if eid == "paperback":
            band = pc.get("paperbackRegularTrimBW", {})
        elif eid == "hardcover":
            band = pc.get("hardcoverRegularTrimBW", {})
        else:
            continue
        cost = band.get("fixed", 0) + pages * band.get("perPage", 0)
        rate = (pc.get("royaltyRateAtOrAbove999", 0.6) if lst >= 9.99
                else pc.get("royaltyRateBelow999", 0.5))
        royalty = lst * rate - cost
        rep.facts["royalty_%s" % eid] = round(royalty, 2)
        rep.facts["printcost_%s" % eid] = round(cost, 2)
        rep.check(royalty > 0,
                  "%s telifi pozitif: %.2f $ (baskı %.2f $ @ %d sayfa)"
                  % (eid, royalty, cost, pages))

    # Kindle bu projede ÜRETİLMEZ (görsel şifreler e-okuyucuda bozulur).
    kindle = [e for e in prod.get("editionsHypothesis", [])
              if e.get("id") == "kindle"]
    rep.check(not kindle or not kindle[0].get("enabled"),
              "Kindle devre dışı (görsel şifre koruması)")

    fnd = cfg.get("founder", {})
    isbn = fnd.get("isbn", {})
    rep.check(isbn.get("strategy") in ("kdp-free", "own"),
              "ISBN stratejisi geçerli")


def check_games(cfg: dict, games, fams, gate: str, rep: Report) -> None:
    print("\n── bulmaca envanteri (public katman) ──")

    if games is None:
        if gate == "phase0":
            rep.warn("puzzle_index.json yok — phase0'da beklenen (Faz 1 üretir)")
            rep.facts["games_total"] = 0
            return
        rep.fail("puzzle_index.json yok ama kapı %s" % gate)
        return

    entries = games.get("puzzles", []) if isinstance(games, dict) else games
    rep.facts["games_total"] = len(entries)

    ids = [p.get("puzzleId") for p in entries]
    rep.check(len(ids) == len(set(ids)), "bulmaca kimlikleri tekil (%d)" % len(ids))
    rep.check(all(ids), "her bulmacanın puzzleId'si var")

    gate_ids = set()
    if fams:
        gentries = fams.get("gates", []) if isinstance(fams, dict) else fams
        gate_ids = {g.get("id") for g in gentries}
    if not gate_ids:
        gate_ids = {g["id"] for g in cfg["scope"]["gateStructure"]}

    bad_gate = [p["puzzleId"] for p in entries if p.get("gate") not in gate_ids]
    rep.check(not bad_gate,
              "her bulmaca tanımlı bir kapıya ait" +
              ("" if not bad_gate else " — ihlal: %s" % bad_gate[:5]))

    bad_status = [p["puzzleId"] for p in entries
                  if p.get("status") not in VALID_STATUS]
    rep.check(not bad_status,
              "durum alanları geçerli" +
              ("" if not bad_status else " — ihlal: %s" % bad_status[:5]))

    bad_type = [p["puzzleId"] for p in entries
                if p.get("type") not in VALID_PUZZLE_TYPE]
    rep.check(not bad_type,
              "bulmaca tipleri geçerli" +
              ("" if not bad_type else " — ihlal: %s" % bad_type[:5]))

    # ④ ⭑ PUBLIC KATMANDA ÇÖZÜM OLAMAZ ⭑
    leaked = []
    for p in entries:
        for field in FORBIDDEN_PUBLIC_FIELDS:
            if field in p:
                leaked.append("%s.%s" % (p.get("puzzleId"), field))
    rep.check(not leaked,
              "⭑ PUBLIC KATMANDA ÇÖZÜM YOK ⭑" +
              ("" if not leaked else " — SIZINTI: %s" % leaked[:5]))

    # Belirsizlik eşiği: validated bulmacalar eşiği aşamaz.
    maxamb = cfg["solvability"]["maxAcceptableAmbiguityScore"]
    over = [p["puzzleId"] for p in entries
            if p.get("status") in ("validated", "written")
            and isinstance(p.get("ambiguityScore"), (int, float))
            and p["ambiguityScore"] > maxamb]
    rep.check(not over,
              "doğrulanmış bulmacalarda belirsizlik ≤ %d" % maxamb +
              ("" if not over else " — AŞAN: %s" % over[:5]))

    rep.facts["cultures_total"] = len({p.get("gate") for p in entries})
    for st in VALID_STATUS:
        rep.facts["games_%s" % st] = sum(1 for p in entries
                                         if p.get("status") == st)


def check_gate_scope(cfg: dict, gate: str, rep: Report) -> None:
    print("\n── kapı seviyesi kapsam denetimi (%s) ──" % gate)

    req = cfg.get("gates", {}).get("requirements", {}).get(gate)
    if req is None:
        rep.fail("kapı seviyesi config'de tanımsız: %s" % gate)
        return

    total = rep.facts.get("games_total", 0)
    validated = (rep.facts.get("games_validated", 0)
                 + rep.facts.get("games_written", 0))
    written = rep.facts.get("games_written", 0)

    rep.check(total >= req["puzzlesCandidate"],
              "aday bulmaca ≥ %d (ölçülen %d)" % (req["puzzlesCandidate"], total))
    rep.check(validated >= req["puzzlesValidated"],
              "doğrulanmış bulmaca ≥ %d (ölçülen %d)"
              % (req["puzzlesValidated"], validated))
    rep.check(written >= req["puzzlesWritten"],
              "yazılmış bulmaca ≥ %d (ölçülen %d)" % (req["puzzlesWritten"], written))

    if cfg["scope"].get("locked") and gate in ("phase4", "phase5", "release"):
        rep.check(total >= cfg["scope"]["puzzles"], "kilitli kapsam sağlanıyor")


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None, help="kapı seviyesi (yoksa .gate okunur)")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None, help="rapor çıktısı")
    args = ap.parse_args()

    gate = args.gate or read_gate()
    if gate not in VALID_GATES:
        print("HATA: geçersiz kapı seviyesi: %s" % gate, file=sys.stderr)
        return 2

    print("=" * 74)
    print("  VERİ BÜTÜNLÜĞÜ VE KAPSAM · kapı: %s" % gate)
    print("=" * 74)

    rep = Report(args.verbose)

    cfg = load_json(CONFIG, rep)
    if cfg is None:
        print("\n⛔ project_config.json okunamadı — başka hiçbir şey denetlenemez")
        return 1

    check_config(cfg, rep)
    games = load_json(PUZZLE_INDEX, rep, required=(gate != "phase0"))
    fams = load_json(GATE_INDEX, rep, required=False)
    check_games(cfg, games, fams, gate, rep)
    check_gate_scope(cfg, gate, rep)

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · kapı: %s" % (rep.checks, gate))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "gate": gate, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
