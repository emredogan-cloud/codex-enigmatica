#!/usr/bin/env python3
"""
MEKANİZMA ÇEŞİTLİLİĞİ KAPISI — Codex Enigmatica
================================================================================
"Yirmi bulmaca" ile "aynı bulmacanın yirmi varyantı" arasındaki farkı bu
kapı denetler.

NEDEN ÖNEMLİ: okur bir mekanizmayı üçüncü tekrarında ÖĞRENİR. Dördüncüden
sonrası artık bulmaca değil, işlemdir. Bir kapı tek bir aileye yaslanırsa
o kapının son on bulmacası okurun gözünde ANLAMSIZLAŞIR — ve okur bunu
"tembel kitap" diye yazar.

Yedi denetim:

  ① her aile TANIMLI ve dört parçası tam (tanım · zorluk · doğrulama · örnek)
  ② her tanımlı aile en az bir kez KULLANILIYOR (ölü aile yok)
  ③ her bulmaca kapısının İZİN VERDİĞİ bir aileye ait
  ④ zorluk hem ailenin hem kapının bandına oturuyor
  ⑤ ⭑ ÇEŞİTLİLİK ⭑ — tek aile payı, ayrı aile sayısı, ardışık tekrar
  ⑥ künye gerektiren aileler kaynak taşıyor
  ⑦ levha gerektiren aileler levha kimliği taşıyor · gizlilik sınıfı zayıflatılmamış

② NEDEN VAR: kullanılmayan bir aile, taksonomiyi zenginmiş gibi gösteren
ölü bir kayıttır (Bestiarium D28 · World Myths K14: ölü kural sessizce
yanlış güven verir).

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CONFIG = os.path.join(ROOT, "project_config.json")
FAMILIES = os.path.join(ROOT, "01_SOURCE", "mechanism_families.json")
GATE_INDEX = os.path.join(ROOT, "01_SOURCE", "gate_index.json")
PUZZLE_INDEX = os.path.join(ROOT, "01_SOURCE", "puzzle_index.json")

REQUIRED_FAMILY_PARTS = ("definition", "intendedDifficulty",
                         "validationMethod", "exampleSketch")
LEAK_RANK = {"public": 0, "restricted": 1, "protected": 2}
# Çeşitlilik denetimi küçük kümelerde anlamsızdır: 3 kayıtta "%35 pay"
# matematiksel olarak sağlanamaz. Eşik bilerek düşük tutuldu.
DIVERSITY_MIN_POPULATION = 10


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


def load(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None,
                    help="kabul edilir ve yok sayılır — bu kapı faz "
                         "seviyesinden bağımsızdır; ortak çağrı biçimi korunur")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    print("=" * 74)
    print("  MEKANİZMA ÇEŞİTLİLİĞİ")
    print("=" * 74)

    rep = Report(args.verbose)

    for p in (FAMILIES, GATE_INDEX, PUZZLE_INDEX):
        if not os.path.exists(p):
            print("\n  ⊘ %s yok — Faz 1 teslimatı" % os.path.relpath(p, ROOT))
            print("=" * 74)
            return 0

    cfg = load(CONFIG)
    fams = {f["id"]: f for f in load(FAMILIES).get("families", [])}
    gates = {g["id"]: g for g in load(GATE_INDEX).get("gates", [])}
    puzzles = load(PUZZLE_INDEX).get("puzzles", [])
    tx = cfg.get("taxonomy", {})

    # ── ① aile tanımları eksiksiz ───────────────────────────────────────
    print("\n── ① aile tanımları ──")
    incomplete = [fid for fid, f in fams.items()
                  if any(not f.get(k) for k in REQUIRED_FAMILY_PARTS)]
    rep.check(not incomplete,
              "her ailenin dört parçası tam (tanım · zorluk · doğrulama · örnek)"
              + ("" if not incomplete else " — EKSİK: %s" % incomplete[:5]))
    rep.facts["familiesDefined"] = len(fams)

    used = collections.Counter(p.get("mechanismFamily") for p in puzzles)
    unknown = sorted(set(used) - set(fams))
    rep.check(not unknown, "her bulmaca tanımlı bir aileye ait"
              + ("" if not unknown else " — TANIMSIZ: %s" % unknown[:5]))

    # ── ② ölü aile ──────────────────────────────────────────────────────
    print("\n── ② ölü aile ──")
    dead = sorted(set(fams) - set(used))
    rep.check(not dead, "her tanımlı aile en az bir kez kullanılıyor"
              + ("" if not dead else " — ÖLÜ AİLE: %s" % dead))
    rep.facts["familiesUsed"] = len([f for f in used if f in fams])

    # ── ③ kapı izinleri ─────────────────────────────────────────────────
    print("\n── ③ kapı izinleri ──")
    not_allowed = []
    for p in puzzles:
        g = gates.get(p.get("gate"))
        if not g:
            continue
        allowed = g.get("allowedFamilies", [])
        if allowed and p.get("mechanismFamily") not in allowed:
            not_allowed.append("%s: %s ∉ %s"
                               % (p.get("puzzleId"), p.get("mechanismFamily"),
                                  p.get("gate")))
    rep.check(not not_allowed, "her bulmaca kapısının izin verdiği bir ailede"
              + ("" if not not_allowed else " — İHLAL: %s" % not_allowed[:5]))

    # ── ④ zorluk bandı ──────────────────────────────────────────────────
    print("\n── ④ zorluk bandı ──")
    bad_diff, bad_type = [], []
    for p in puzzles:
        f = fams.get(p.get("mechanismFamily"))
        if not f:
            continue
        lo, hi = f["intendedDifficulty"]
        d = p.get("difficulty")
        if d is not None and not (lo <= d <= hi):
            bad_diff.append("%s: zorluk %s ∉ [%d,%d]" % (p["puzzleId"], d, lo, hi))
        if p.get("type") != f.get("type"):
            bad_type.append("%s: tip %s ≠ aile tipi %s"
                            % (p["puzzleId"], p.get("type"), f.get("type")))
    rep.check(not bad_diff, "zorluk ailenin bandında"
              + ("" if not bad_diff else " — AŞIM: %s" % bad_diff[:5]))
    rep.check(not bad_type, "bulmaca tipi ailenin tipiyle tutarlı"
              + ("" if not bad_type else " — ÇELİŞKİ: %s" % bad_type[:5]))

    # Bir kapının zorluğunu AŞAN bulmaca, zorluk eğrisini içeriden kırar.
    over_gate = []
    for p in puzzles:
        g = gates.get(p.get("gate"))
        if g and p.get("difficulty") is not None:
            if p["difficulty"] > g.get("difficulty", 3):
                over_gate.append("%s (%d > kapı %d)"
                                 % (p["puzzleId"], p["difficulty"],
                                    g.get("difficulty")))
    rep.check(not over_gate, "hiçbir bulmaca kapısının zorluğunu aşmıyor"
              + ("" if not over_gate else " — AŞIM: %s" % over_gate[:5]))

    # ── ⑤ ⭑ ÇEŞİTLİLİK ⭑ ────────────────────────────────────────────────
    print("\n── ⑤ ⭑ ÇEŞİTLİLİK ⭑ ──")
    max_share = tx.get("maxFamilyShareWithinGatePct", 100)
    min_distinct = tx.get("minDistinctFamiliesPerGate", 1)
    max_run = tx.get("maxConsecutiveSameFamily", 99)
    per_gate = {}

    for gid, g in gates.items():
        pool = [p for p in puzzles if p.get("gate") == gid
                and p.get("status") != "dropped"]
        slotted = sorted([p for p in pool if "slot" in p],
                         key=lambda x: x["slot"])
        # Okurun gördüğü küme slotlanmış kümedir; yoksa aday havuzu ölçülür.
        measured = slotted or pool
        counts = collections.Counter(p.get("mechanismFamily") for p in measured)
        per_gate[gid] = {"population": len(measured),
                         "slotted": len(slotted),
                         "candidates": len(pool),
                         "families": dict(counts)}

        rep.check(len(pool) >= g.get("candidateMin", 0),
                  "kapı '%s' aday sayısı ≥%d (ölçülen %d)"
                  % (gid, g.get("candidateMin", 0), len(pool)))

        if g.get("metaGate") or len(measured) < DIVERSITY_MIN_POPULATION:
            continue

        top, n = counts.most_common(1)[0]
        share = n / len(measured) * 100
        per_gate[gid]["topFamilyPct"] = round(share, 1)
        rep.check(share <= max_share,
                  "kapı '%s' tek aile payı ≤%%%d (en yüksek: %s %%%.1f)"
                  % (gid, max_share, top, share))
        rep.check(len(counts) >= min_distinct,
                  "kapı '%s' ≥%d ayrı aile taşıyor (ölçülen %d)"
                  % (gid, min_distinct, len(counts)))

        if slotted:
            run = best = 1
            for a, b in zip(slotted, slotted[1:]):
                run = run + 1 if a["mechanismFamily"] == b["mechanismFamily"] else 1
                best = max(best, run)
            per_gate[gid]["longestRun"] = best
            rep.check(best <= max_run,
                      "kapı '%s' ardışık aynı aile ≤%d (ölçülen %d)"
                      % (gid, max_run, best))

    rep.facts["perGate"] = per_gate
    total_distinct = len([f for f in used if f in fams])
    rep.check(total_distinct >= tx.get("minDistinctFamiliesTotal", 1),
              "kitap genelinde ≥%d ayrı mekanizma (ölçülen %d)"
              % (tx.get("minDistinctFamiliesTotal", 1), total_distinct))

    # ── ⑥ künye zorunluluğu ─────────────────────────────────────────────
    print("\n── ⑥ künye zorunluluğu ──")
    missing_src = [p["puzzleId"] for p in puzzles
                   if fams.get(p.get("mechanismFamily"), {}).get("requiresSourcing")
                   and not p.get("sourceRefs")]
    rep.check(not missing_src,
              "künye gerektiren her bulmaca kaynak anahtarı taşıyor"
              + ("" if not missing_src else " — KAYNAKSIZ: %s" % missing_src[:5]))

    # ── ⑦ levha ve gizlilik sınıfı ──────────────────────────────────────
    print("\n── ⑦ levha ve gizlilik sınıfı ──")
    missing_plate, weak_leak, bad_carry = [], [], []
    for p in puzzles:
        f = fams.get(p.get("mechanismFamily"))
        if not f:
            continue
        if f.get("requiresPlate") and not p.get("plateId"):
            missing_plate.append(p["puzzleId"])
        if f.get("plateCarriesData") and not p.get("plateCarriesData"):
            bad_carry.append(p["puzzleId"])
        want = LEAK_RANK.get(f.get("defaultLeakClass", "protected"), 2)
        have = LEAK_RANK.get(p.get("leakClass", "protected"), 2)
        if have < want:
            weak_leak.append("%s: %s < %s" % (p["puzzleId"], p.get("leakClass"),
                                              f.get("defaultLeakClass")))
    rep.check(not missing_plate, "levha gerektiren her bulmaca levha kimliği taşıyor"
              + ("" if not missing_plate else " — EKSİK: %s" % missing_plate[:5]))
    rep.check(not bad_carry,
              "veri taşıyan levhalar plateCarriesData ile işaretli "
              "(POD baskı testi bunlara koşar)"
              + ("" if not bad_carry else " — İŞARETSİZ: %s" % bad_carry[:5]))
    rep.check(not weak_leak,
              "hiçbir bulmaca ailesinin gizlilik sınıfını ZAYIFLATMIYOR"
              + ("" if not weak_leak else " — ZAYIFLATMA: %s" % weak_leak[:5]))

    # ── ⑧ cevap biçimi ──────────────────────────────────────────────────
    print("\n── ⑧ cevap biçimi ──")
    no_fmt, wrong_fmt = [], []
    for p in puzzles:
        f = fams.get(p.get("mechanismFamily"))
        if not f:
            continue
        if not p.get("answerFormat"):
            no_fmt.append(p["puzzleId"])
        elif f.get("answerFormat") and p["answerFormat"] != f["answerFormat"]:
            wrong_fmt.append("%s: %s ≠ %s" % (p["puzzleId"], p["answerFormat"],
                                              f["answerFormat"]))
    rep.check(not no_fmt,
              "her bulmaca cevap biçimi taşıyor (okur ne YAZACAĞINI bilecek)"
              + ("" if not no_fmt else " — BİÇİMSİZ: %s" % no_fmt[:5]))
    rep.check(not wrong_fmt, "cevap biçimi ailesiyle tutarlı"
              + ("" if not wrong_fmt else " — ÇELİŞKİ: %s" % wrong_fmt[:5]))

    # ── ⑨ metne bağlı bulmacalar ────────────────────────────────────────
    print("\n── ⑨ metne bağlı bulmacalar ──")
    # narrative-embedded · back-reference · book-structure aileleri METNE
    # bağlıdır ve Faz 5'in LINE EDITOR alt-ajanı tam olarak o metni
    # düzeltmekle görevlidir. Karma olmadan bir düzeltme bulmacayı SESSİZCE
    # kırar: hiçbir test metne bağlı olmadığı için hiçbir test kırmızı yanmaz.
    unbound = [p["puzzleId"] for p in puzzles
               if fams.get(p.get("mechanismFamily"), {}).get("textBound")
               and p.get("status") in ("drafted", "validated", "written")
               and not p.get("boundToTextHash")]
    rep.check(not unbound,
              "⭑ metne bağlı her yazılmış bulmaca metin karması taşıyor ⭑"
              + ("" if not unbound else " — ⛔ BAĞSIZ: %s" % unbound[:5]))
    rep.facts["textBoundCandidates"] = sum(
        1 for p in puzzles
        if fams.get(p.get("mechanismFamily"), {}).get("textBound"))

    # ── ⑩ yedek havuz ───────────────────────────────────────────────────
    print("\n── ⑩ yedek havuz ──")
    rr = load(GATE_INDEX).get("reserveRules", {})
    min_gs = rr.get("minGateSynthesisCandidatesPerGate", 1)
    min_res_fams = rr.get("minReserveFamiliesPerGate", 1)
    thin_gs, thin_res = [], []
    for gid, g in gates.items():
        if g.get("metaGate"):
            continue
        gs = [p for p in puzzles if p.get("gate") == gid
              and p.get("mechanismFamily") == "gate-synthesis"
              and p.get("status") != "dropped"]
        if len(gs) < min_gs:
            thin_gs.append("%s (%d)" % (gid, len(gs)))
        reserve = [p for p in puzzles if p.get("gate") == gid
                   and "slot" not in p and p.get("status") != "dropped"]
        rf = {p.get("mechanismFamily") for p in reserve}
        if len(rf) < min_res_fams:
            thin_res.append("%s (%d aile)" % (gid, len(rf)))
    rep.check(not thin_gs,
              "her kapıda ≥%d kapı bulmacası adayı var "
              "(en yüksek bağımlılıklı bulmacanın yedeği)" % min_gs
              + ("" if not thin_gs else " — YEDEKSİZ: %s" % thin_gs))
    rep.check(not thin_res,
              "her kapının yedek havuzu ≥%d ayrı aileden" % min_res_fams
              + ("" if not thin_res else " — TEK AİLELİ: %s" % thin_res))
    if rr.get("requireCrossFamilyReserve"):
        bad_sub = []
        for p in puzzles:
            for target in p.get("substitutableFor", []) or []:
                t = next((q for q in puzzles if q["puzzleId"] == target), None)
                if t and t.get("mechanismFamily") == p.get("mechanismFamily") \
                        and p.get("mechanismFamily") != "gate-synthesis":
                    bad_sub.append("%s → %s (aynı aile)" % (p["puzzleId"], target))
        rep.check(not bad_sub,
                  "yedekler ÇAPRAZ AİLEDEN (aynı aileden yedek, aile "
                  "çöktüğünde işe yaramaz)"
                  + ("" if not bad_sub else " — AYNI AİLE: %s" % bad_sub[:5]))

    print("\n── aile dağılımı ──")
    for fid, n in used.most_common():
        print("  %-24s %3d" % (fid, n))

    print("\n" + "=" * 74)
    if rep.warnings:
        print("  %d uyarı" % len(rep.warnings))
    if rep.errors:
        print("  ⛔ %d/%d DENETİM KIRMIZI" % (len(rep.errors), rep.checks))
        for e in rep.errors:
            print("     · %s" % e)
        status = "fail"
    else:
        print("  ✅ %d denetim yeşil · %d aile · %d bulmaca"
              % (rep.checks, total_distinct, len(puzzles)))
        status = "pass"
    print("=" * 74)

    if args.json:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"status": status, "checks": rep.checks,
                       "errors": rep.errors, "warnings": rep.warnings,
                       "facts": rep.facts}, fh, ensure_ascii=False, indent=2)

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
