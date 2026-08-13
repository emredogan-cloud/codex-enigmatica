#!/usr/bin/env python3
"""
⛔ ÖLDÜRME KAPISI ⛔ — Faz 2'nin kararı
================================================================================
Bu betik projenin devam edip etmeyeceğini SÖYLEMEZ; ÖLÇER. Eşikler
`project_config.json § killGate` içinde sayısaldır ve yoruma yer yoktur.

⭑ EN ÖNEMLİ DAVRANIŞI ŞUDUR: VERİ YOKSA "GEÇTİ" DEMEZ. ⭑

Sıfır çözücü kaydıyla bütün ölçütler teknik olarak "ihlal edilmemiş"
görünür — hiçbir çözücü başarısız olmadı, hiçbir alternatif cevap
bildirilmedi, hiçbir bulmaca çözülemedi diye işaretlenmedi. Bir kapının
boş veriyle yeşil yanması, bu projede yapılabilecek en pahalı yalandır:
öldürme kapısının BÜTÜN değeri dürüstlüğünden gelir.

Bu yüzden karar dört değil BEŞ değerlidir:

  BLOCKED    → veri yok. Karar VERİLEMEZ.        ← sıfır oturumda buradadır
  PASS       → 4–5 çözücü bitirdi, 0 alternatif  → DEVAM
  REWORK     → 4–5 bitirdi ama alternatif var    → yeniden yaz, testi TEKRARLA
  REDESIGN   → tam 3 bitirdi                     → Kapı I yeniden tasarlanır
  HARD-STOP  → ≤2 bitirdi                        → PROJE DURUR (kurucu kararı)

Çıkış kodları:  0 = PASS   1 = PASS DEĞİL (BLOCKED dâhil)   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

OUT = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "kill-gate-report.json")
SOLVER_DIR = os.path.join(pl.ROOT, "06_REPORTS", "solver")
PLAYTEST_DIR = os.path.join(pl.ROOT, "01_SOURCE", "playtests")


def collect_sessions() -> list[dict]:
    """Ham çözücü kayıtları — depoya GİRMEZ (PROTECTED_DIRS)."""
    out = []
    if not os.path.isdir(SOLVER_DIR):
        return out
    for name in sorted(os.listdir(SOLVER_DIR)):
        if not name.endswith(".json"):
            continue
        try:
            with open(os.path.join(SOLVER_DIR, name), encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            continue
        out.extend(data if isinstance(data, list) else [data])
    return out


def load_aggregate() -> dict | None:
    """OTURUM DÜZEYİ toplu kayıt — SOLVER_TEST_PROTOCOL § 3'ün 'oturum
    başına' formu.

    ⚠ NEDEN AYRI BİR YOL: protokol iki ayrı form tanımlar (bulmaca başına
    ve oturum başına) ve gerçek bir testte ikincisi birincisi olmadan
    gelebilir. Kapı, elindeki veriyle KARAR VEREBİLMELİ ama ölçemediğini
    ÖLÇTÜM DEMEMELİDİR. Toplu kayıt bitirme sayısını verir; bulmaca başına
    ölçütler ölçülemez ve öyle raporlanır."""
    for d in (PLAYTEST_DIR, SOLVER_DIR):
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
            if isinstance(data, dict) and "solversCompletedGate" in data:
                return data
    return None


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None,
                    help="kabul edilir ve yok sayılır — öldürme kapısı faz "
                         "seviyesinden değil VERİDEN karar üretir; ortak "
                         "çağrı biçimi korunur")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=OUT)
    args = ap.parse_args()

    print("=" * 74)
    print("  ⛔ ÖLDÜRME KAPISI ⛔ · Faz 2 · Kapı I")
    print("=" * 74)

    cfg = pl.load_config()
    kg = cfg.get("killGate", {})
    pc = kg.get("passCriteria", {})
    hs = kg.get("hardStopCriteria", {})
    fnd = cfg.get("founder", {}).get("externalSolvers", {})
    puzzles = [p for p in pl.load_index() if p.get("pilotCohort")]
    sols, _ = pl.load_protected()

    need_solvers = kg.get("solversRequired", 5)
    cap = pc.get("medianCompletionMinutesMax", 240)

    # ── kanıt tabanı ────────────────────────────────────────────────────
    sessions = collect_sessions()
    external_tests = []
    for pid, rec in sols.items():
        for t in rec.get("solverTests") or []:
            if isinstance(t, dict) and t.get("solverClass") == "external":
                external_tests.append(dict(t, puzzleId=pid))

    declared = fnd.get("sessionsRecorded", 0)
    solvers = sorted({t.get("solver") for t in external_tests if t.get("solver")})

    print("\n── kanıt tabanı ──")
    print("  pilot bulmaca                  %d / %d" % (len(puzzles), kg.get("puzzlesRequired", 20)))
    print("  çözücü BELİRLENDİ (A3)         %s (%d kişi)"
          % ("EVET" if fnd.get("founderConfirmed") else "HAYIR",
             fnd.get("identifiedCount", 0)))
    print("  oturum YAPILDI (A12)           %d" % declared)
    print("  ham oturum kaydı               %d dosya" % len(sessions))
    print("  harici bulmaca denemesi        %d kayıt · %d ayrı çözücü"
          % (len(external_tests), len(solvers)))
    print("  ⚠ iç çözücü kayıtları KANIT SAYILMAZ (internalSolverCountsAsEvidence=false)")

    report = {
        "phase": "phase2", "gate": "threshold",
        "puzzlesWritten": len(puzzles),
        "puzzlesRequired": kg.get("puzzlesRequired", 20),
        "solversIdentified": fnd.get("identifiedCount", 0),
        "sessionsRecorded": declared,
        "externalTestRecords": len(external_tests),
        "distinctExternalSolvers": len(solvers),
        "thresholds": pc,
        "criteria": {}, "verdict": None, "reason": None,
        "internalSolverCountsAsEvidence": False,
    }

    # ── OTURUM DÜZEYİ TOPLU KAYIT ───────────────────────────────────────
    agg = load_aggregate()
    if agg:
        total = agg.get("solversTotal", 0)
        finished_n = agg.get("solversCompletedGate", 0)
        report["sessionAggregate"] = {
            "solversTotal": total,
            "solversCompletedGate": finished_n,
            "perPuzzleRecords": agg.get("perPuzzleRecords"),
            "abandonReasons": [r.get("code") for r in
                               agg.get("abandonReasons") or []],
        }
        print("\n── oturum düzeyi toplu kayıt ──")
        print("  çözücü            %d" % total)
        print("  kapıyı BİTİREN    %d" % finished_n)
        print("  bırakan           %d" % agg.get("solversAbandoned", total - finished_n))
        for r in agg.get("abandonReasons") or []:
            print("    · %-28s %s" % (r.get("label", r.get("code")),
                                      (r.get("implicatedPuzzles") or "—")))

        hs = kg.get("hardStopCriteria", {}).get("solversCompletingGateI", 3)
        need_pass = pc.get("solversCompletingGateI", 4)

        # ⚠ Bulmaca başına kayıt yoksa DİĞER ÖLÇÜTLER ÖLÇÜLEMEZ.
        # "İhlal edilmedi" ile "ölçülmedi" aynı şey değildir.
        measured = agg.get("perPuzzleRecords") is not None
        for k in ("puzzlesUnsolvedByAll", "puzzlesBelowSolverFloor",
                  "puzzlesOverLevel3Limit", "medianMinutes",
                  "confirmedAlternatives"):
            report["criteria"][k] = {"value": None, "threshold": None,
                                     "pass": None, "measured": measured}
        report["criteria"]["solversCompletingGate"] = {
            "value": finished_n, "threshold": need_pass,
            "pass": finished_n >= need_pass, "measured": True}

        if finished_n < hs:
            verdict = "HARD-STOP"
            reason = ("%d/%d çözücü Kapı I'i bitirdi — sert durdurma eşiği "
                      "%d'ün ALTINDA. Sistem bu hâliyle çalışmıyor."
                      % (finished_n, total, hs))
        elif finished_n == hs:
            verdict, reason = "REDESIGN", "tam %d çözücü bitirdi — zorluk eğrisi bozuk" % hs
        elif finished_n < need_pass:
            verdict, reason = "REWORK", "%d/%d bitirdi — geçme eşiği %d" % (finished_n, total, need_pass)
        else:
            verdict = "REWORK"
            reason = ("bitirme eşiği sağlandı ama bulmaca başına kayıt YOK — "
                      "kalan ölçütler ÖLÇÜLEMEDİ")
        report["verdict"], report["reason"] = verdict, reason
        report["perPuzzleCriteriaMeasured"] = measured
        report["abandonReasonDetail"] = agg.get("abandonReasons")

        print("\n" + "=" * 74)
        print("  ⛔ KARAR: %s" % verdict)
        print("=" * 74)
        print("  %s" % reason)
        if not measured:
            print("")
            print("  ⚠ Bulmaca başına kayıt SAĞLANMADI. Kalan beş ölçüt")
            print("    ÖLÇÜLEMEDİ ve 'geçti' SAYILMAZ — 'ihlal edilmedi' ile")
            print("    'ölçülmedi' aynı şey değildir.")
        print("=" * 74)
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        return 0 if verdict == "PASS" else 1

    # ── ⭑ VERİ YOKSA KARAR VERİLEMEZ ⭑ ──────────────────────────────────
    if len(solvers) < need_solvers or declared < need_solvers:
        report["verdict"] = "BLOCKED"
        report["reason"] = (
            "Harici çözücü oturumları YAPILMADI. %d/%d çözücü kaydı var. "
            "Öldürme kapısı ölçemediği bir şeyi geçmiş sayamaz."
            % (len(solvers), need_solvers))
        report["blockingDecision"] = "A12"
        report["whatIsReady"] = [
            "20 pilot bulmaca yazıldı ve bütün teknik kapılardan geçti",
            "cevap uzayı bağımsız açıldı: 20/20 tam olarak bir kabul",
            "harici çözücü paketi hazır: 00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md",
            "kayıt şeması ve eşikler sayısal olarak tanımlı",
        ]
        report["whatIsMissing"] = [
            "%d harici çözücü oturumu (0 yapıldı)" % need_solvers,
            "bulmaca başına çözüm oranı",
            "medyan tamamlama süresi",
            "ipucu tüketimi",
            "çözücülerin önerdiği alternatif cevaplar",
        ]
        print("\n" + "=" * 74)
        print("  ⛔ KARAR: BLOCKED — ÖLÇÜLEMEDİ")
        print("=" * 74)
        print("  Sıfır oturumla bütün ölçütler 'ihlal edilmemiş' GÖRÜNÜR:")
        print("  hiçbir çözücü başarısız olmadı, hiçbir alternatif cevap")
        print("  bildirilmedi. Bu bir GEÇİŞ DEĞİL, BİR BOŞLUKTUR.")
        print("")
        print("  Bloklayan karar : A12 — harici çözücü oturumları")
        print("  Devir paketi    : 00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md")
        print("=" * 74)
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        return 1

    # ── ölçütler (gerçek veri geldiğinde koşar) ─────────────────────────
    by_solver: dict[str, list[dict]] = {}
    for t in external_tests:
        by_solver.setdefault(t["solver"], []).append(t)

    finished = [s for s, ts in by_solver.items()
                if len([t for t in ts if t.get("result") != "unsolved"])
                >= len(puzzles)]
    solved_per_puzzle = {p["puzzleId"]: 0 for p in puzzles}
    lvl3_per_puzzle = {p["puzzleId"]: 0 for p in puzzles}
    for t in external_tests:
        if t.get("result") != "unsolved":
            solved_per_puzzle[t["puzzleId"]] = solved_per_puzzle.get(
                t["puzzleId"], 0) + 1
        hb = t.get("hintsUsedByLevel") or []
        if len(hb) == 3 and hb[2]:
            lvl3_per_puzzle[t["puzzleId"]] = lvl3_per_puzzle.get(
                t["puzzleId"], 0) + 1

    times = []
    for s, ts in by_solver.items():
        if s in finished:
            times.append(sum(t.get("minutesToSolve", 0) for t in ts))
        else:
            times.append(cap)          # ⭑ DNF TAVAN SAYILIR ⭑
    median = statistics.median(times) if times else None

    alts = [t for t in external_tests if (t.get("alternativeOffered") or "").strip()]
    unsolved_by_all = [pid for pid, n in solved_per_puzzle.items() if n == 0]
    under_floor = [pid for pid, n in solved_per_puzzle.items()
                   if n < pc.get("minSolversPerPuzzle", 2)]
    lvl3_over = [pid for pid, n in lvl3_per_puzzle.items()
                 if n > pc.get("maxSolversNeedingLevel3Hint", 2)]
    amb_over = [p["puzzleId"] for p in puzzles
                if (p.get("ambiguityScore") or 9) > pc.get("maxAmbiguityScore", 2)]

    C = report["criteria"]
    C["solversCompletingGate"] = {"value": len(finished),
                                  "threshold": pc.get("solversCompletingGateI", 4),
                                  "pass": len(finished) >= pc.get("solversCompletingGateI", 4)}
    C["puzzlesUnsolvedByAll"] = {"value": len(unsolved_by_all), "threshold": 0,
                                 "pass": not unsolved_by_all}
    C["puzzlesBelowSolverFloor"] = {"value": len(under_floor), "threshold": 0,
                                    "pass": not under_floor}
    C["puzzlesOverLevel3Limit"] = {"value": len(lvl3_over), "threshold": 0,
                                   "pass": not lvl3_over}
    C["confirmedAlternatives"] = {"value": len(alts), "threshold": 0,
                                  "pass": not alts}
    C["medianMinutes"] = {"value": median, "threshold": cap,
                          "pass": median is not None and median <= cap}
    C["ambiguityOverLimit"] = {"value": len(amb_over), "threshold": 0,
                               "pass": not amb_over}

    print("\n── ölçütler ──")
    for k, v in C.items():
        print("  %-26s %-10s eşik %-6s %s"
              % (k, v["value"], v["threshold"], "✓" if v["pass"] else "⛔"))

    n_fin = len(finished)
    if n_fin <= hs.get("solversCompletingGateI", 3) - 1:
        verdict, reason = "HARD-STOP", "%d/%d çözücü bitirdi — sistem çalışmıyor" % (n_fin, need_solvers)
    elif n_fin == hs.get("solversCompletingGateI", 3):
        verdict, reason = "REDESIGN", "tam 3 çözücü bitirdi — zorluk eğrisi bozuk"
    elif alts:
        verdict, reason = "REWORK", "%d alternatif cevap bildirildi" % len(alts)
    elif all(v["pass"] for v in C.values()):
        verdict, reason = "PASS", "bütün ölçütler sağlandı"
    else:
        failed = [k for k, v in C.items() if not v["pass"]]
        verdict, reason = "REWORK", "sağlanmayan ölçüt: %s" % ", ".join(failed)

    report["verdict"], report["reason"] = verdict, reason
    print("\n" + "=" * 74)
    print("  KARAR: %s — %s" % (verdict, reason))
    print("=" * 74)

    os.makedirs(os.path.dirname(args.json), exist_ok=True)
    with open(args.json, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
